import sys

from langchain_mcp_adapters.client import MultiServerMCPClient

from config.settings import get_settings


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
                "mcp_server.server",
            ],
        }
    }

    if include_tavily:
        if not settings.tavily_api_key:
            raise ValueError(
                "Configura TAVILY_API_KEY en .env"
            )

        connections["tavily"] = {
            "transport": "streamable_http",
            "url": settings.tavily_mcp_url,
            "headers": {
                "Authorization": (
                    "Bearer "
                    + settings.tavily_api_key.get_secret_value()
                )
            },
        }

    return MultiServerMCPClient(connections)


async def get_mcp_tools(
    include_tavily: bool = True,
):
    client = build_mcp_client(
        include_tavily=include_tavily
    )

    return await client.get_tools()
