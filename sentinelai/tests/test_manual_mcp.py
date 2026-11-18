
import asyncio

from sentinelai.mcp_client import get_mcp_tools


async def main():
    tools = await get_mcp_tools(
        include_tavily=True
    )

    print(f"\nTools encontradas: {len(tools)}")

    for tool in tools:
        print(f"- {tool.name}")


if __name__ == "__main__":
    asyncio.run(main())
