import sys

from langchain_mcp_adapters.client import MultiServerMCPClient

from sentinelai.config.settings import get_settings


def build_mcp_client(
    include_tavily: bool = True,
) -> MultiServerMCPClient:
    settings = get_settings()

    connections = {
        "sentinelai": {
            "transport": "stdio",
            "command": sys.executable,
            "args": [
                "-m",
                "sentinelai.mcp_server.server",
            ],
        }
    }

    if include_tavily:
        if not settings.TAVILY_API_KEY:
            raise ValueError(
                "Configura TAVILY_API_KEY en .env"
            )

        connections["tavily"] = {
            "transport": "streamable_http",
            "url": settings.TAVILY_MCP_URL,
            "headers": {
                "Authorization": (
                    "Bearer "
                    + settings.TAVILY_API_KEY.get_secret_value()
                )
            },
        }

    return MultiServerMCPClient(connections)



async def get_mcp_tools(
    include_tavily: bool = True,
    server_name: str | None = None,
):
    client = build_mcp_client(
        include_tavily=include_tavily
    )

    return await client.get_tools(
        server_name=server_name
    )

