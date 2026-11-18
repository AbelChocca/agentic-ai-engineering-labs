import json

from mcp.server.fastmcp import FastMCP
from sentinelai.config.settings import get_settings

mcp = FastMCP('SentinelAI Security Events')

def _dataset() -> dict:
    return json.loads(get_settings().events_path.read_text(encoding='utf-8'))

@mcp.tool()
def list_security_events(scenario_id: str, event_type: str | None = None, limit: int = 50) -> list[dict]:
    """Lista registros ficticios de un escenario, con filtro opcional por tipo."""
    if not 1 <= limit <= 100:
        raise ValueError('limit debe estar entre 1 y 100')
    events = [e for e in _dataset()['events'] if e['scenario_id'] == scenario_id]
    if event_type:
        events = [e for e in events if e['event_type'] == event_type]
    return events[:limit]


@mcp.tool()
def get_event_details(event_id: str) -> dict:
    """Obtiene un evento de seguridad por su identificador."""
    return next((e for e in _dataset()['events'] if e['event_id'] == event_id), {'error': 'Evento no encontrado'})


@mcp.tool()
def search_events(scenario_id: str, query: str) -> list[dict]:
    """Busca por IP, usuario, activo o cualquier texto del evento dentro de un escenario."""
    q = query.casefold()
    return [
        e for e in _dataset()['events']
        if e['scenario_id'] == scenario_id and q in json.dumps(e, ensure_ascii=False).casefold()
    ][:100]


@mcp.tool()
def get_asset_context(asset_id: str) -> dict:
    """Consulta inventario y contexto simulados de un activo."""
    return next((a for a in _dataset()['assets'] if a['asset_id'] == asset_id), {'error': 'Activo no encontrado'})

if __name__ == '__main__':
    mcp.run(transport='stdio')
