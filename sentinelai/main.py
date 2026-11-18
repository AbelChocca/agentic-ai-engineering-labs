import asyncio
import time
import json

from langchain.chat_models import init_chat_model

from sentinelai.agents.log_analyst import build_log_analyst
from sentinelai.agents.threat_researcher import build_threat_researcher
from sentinelai.agents.supervisor import build_supervisor

from sentinelai.tools.delegation import (
    create_log_delegation_tool,
    create_research_delegation_tool,
)

from sentinelai.config.settings import get_settings
from sentinelai.mcp_client import get_mcp_tools
from sentinelai.models.incident import IncidentReport
from sentinelai.repositories.incident_repository import (
    IncidentRepository,
)


def validate_incident_report(
    report: IncidentReport,
    scenario_id: str,
    events_path,
) -> None:
    """Comprueba las referencias del informe contra el dataset."""

    data = json.loads(
        events_path.read_text(encoding="utf-8")
    )

    valid_events = {
        event["event_id"]
        for event in data["events"]
        if event["scenario_id"] == scenario_id
    }

    valid_assets = {
        asset["asset_id"]
        for asset in data["assets"]
    }

    if report.scenario_id != scenario_id:
        raise ValueError(
            "El informe pertenece a otro escenario."
        )

    for finding in report.findings:
        invalid_ids = set(finding.event_ids) - valid_events

        if invalid_ids:
            raise ValueError(
                f"Eventos inválidos: {sorted(invalid_ids)}"
            )

    invalid_assets = set(report.affected_assets) - valid_assets

    if invalid_assets:
        raise ValueError(
            f"Activos inválidos: {sorted(invalid_assets)}"
        )


async def main():
    settings = get_settings()
    scenario_id = "INC-001"

    model = init_chat_model(
        settings.GEMINI_MODEL,
        model_provider="google_genai",
        api_key=settings.GOOGLE_API_KEY.get_secret_value(),
        timeout=120,
        max_retries=2,
    )

    # 1. Obtener herramientas MCP
    log_tools = await get_mcp_tools(
        include_tavily=False,
        server_name="sentinelai",
    )

    research_tools = await get_mcp_tools(
        include_tavily=True,
        server_name="tavily",
    )

    research_tools = [
        tool for tool in research_tools
        if tool.name in {"tavily_search", "tavily_extract"}
    ]

    # 2. Construir especialistas
    log_analyst = build_log_analyst(model, log_tools)
    researcher = build_threat_researcher(
        model, research_tools
    )

    # 3. Crear herramientas de delegación
    delegation_tools = [
        create_log_delegation_tool(log_analyst),
        create_research_delegation_tool(researcher),
    ]

    # 4. Construir Supervisor con respuesta estructurada
    supervisor = build_supervisor(
        model,
        delegation_tools=delegation_tools,
    )

    print("🛡️ Iniciando investigación...", flush=True)
    start = time.perf_counter()

    # 5. Ejecutar investigación
    result = await supervisor.ainvoke(
        {
            "messages": [{
                "role": "user",
                "content": (
                    f"Investiga el escenario {scenario_id}. "
                    "Consulta evidencias internas y, si corresponde, "
                    "fuentes externas. Genera el IncidentReport."
                ),
            }]
        },
        config={"recursion_limit": 25},
    )

    # 6. Recuperar y validar estructura Pydantic
    report = IncidentReport.model_validate(
        result["structured_response"]
    )

    print("✅ Estructura Pydantic válida")

    # 7. Validar referencias contra el dataset
    validate_incident_report(
        report=report,
        scenario_id=scenario_id,
        events_path=settings.events_path,
    )

    print("✅ Evidencias verificadas")

    # 8. Guardar en SQLite
    repository = IncidentRepository()
    report_id = repository.save(report)

    elapsed = time.perf_counter() - start

    print(f"\n✅ Informe guardado: {report_id}")
    print(f"⏱️ Tiempo: {elapsed:.1f}s")

    # 9. Mostrar resultado estructurado
    print("\n📋 INCIDENT REPORT:")
    print(report.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
