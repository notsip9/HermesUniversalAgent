import asyncio,sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    params=StdioServerParameters(command=sys.executable,args=["-m","hermes_universal_agent.server"])
    async with stdio_client(params) as (read,write):
        async with ClientSession(read,write) as session:
            await session.initialize()
            result=await session.list_tools()
            names=[tool.name for tool in result.tools]
            print("TOOLS",len(names),names)
            status=await session.call_tool("agent_status",{})
            print("STATUS",status.content[0].text[:500])

if __name__=="__main__": asyncio.run(main())
