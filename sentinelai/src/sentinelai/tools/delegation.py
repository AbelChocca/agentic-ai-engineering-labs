
from langchain.tools import tool


def create_research_delegation_tool(threat_researcher):

    @tool
    async def ask_threat_researcher(
        task: str,
    ) -> str:
        """Investiga amenazas mediante fuentes públicas.

        Args:
            task: Pregunta técnica sobre CVE, técnicas,
                  software vulnerable o mitigaciones.
                  No incluir logs ni datos privados.
        """
        print("  [Threat Researcher] Iniciando...", flush=True)

        
        final_response = ""

        async for chunk in threat_researcher.astream(
            {
                "messages": [{
                    "role": "user",
                    "content": task,
                }]
            },
            stream_mode="updates",
            config={"recursion_limit": 12},
        ):
            for node, update in chunk.items():
                print(f"  [Threat Researcher] {node}", flush=True)

                if not isinstance(update, dict):
                    continue

                for message in update.get("messages", []):
                    if getattr(message, "tool_calls", None):
                        print(
                            "    🔎 Tools:",
                            [t["name"] for t in message.tool_calls],
                            flush=True,
                        )

                    if message.type == "ai" and not message.tool_calls:
                        final_response = message.text

        return final_response

    return ask_threat_researcher


def create_log_delegation_tool(log_analyst):

    @tool
    async def ask_log_analyst(
        scenario_id: str,
        task: str,
    ) -> str:
        """Delega la investigación de un escenario al Log Analyst."""

        final_response = ""

        async for chunk in log_analyst.astream(
            {
                "messages": [{
                    "role": "user",
                    "content": (
                        f"Escenario: {scenario_id}\n"
                        f"Investigación: {task}"
                    ),
                }]
            },
            stream_mode="updates",
            config={"recursion_limit": 12},
        ):
            for node, update in chunk.items():
                print(f"  [Log Analyst] {node}", flush=True)

                if not isinstance(update, dict):
                    continue

                for message in update.get("messages", []):
                    if getattr(message, "tool_calls", None):
                        print(
                            "    🔧",
                            [t["name"] for t in message.tool_calls],
                            flush=True,
                        )

                    if message.type == "ai" and not message.tool_calls:
                        final_response = message.text

        return final_response

    return ask_log_analyst
