import asyncio,sys
from pathlib import Path
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    exe=Path(__file__).resolve().parents[1]/"dist"/"HermesUniversalAgentMCP.exe"
    params=StdioServerParameters(command=str(exe),args=[])
    async with stdio_client(params) as (read,write):
        async with ClientSession(read,write) as session:
            await session.initialize()
            listed=await session.list_tools()
            names=[t.name for t in listed.tools]
            assert len(names)==12, names
            print("PACKAGED_TOOLS",len(names),names)
            status=await session.call_tool("agent_status",{})
            assert not status.isError
            print("PACKAGED_STATUS_OK",status.content[0].text[:350])
            denied=await session.call_tool("desktop_screenshot",{"confirm":True})
            assert denied.isError, "Screenshot unexpectedly bypassed the default-deny local permission."
            print("SCREEN_CAPTURE_DEFAULT_DENY_OK")
            denied_click=await session.call_tool("desktop_click",{"x":5,"y":5,"confirm":True})
            assert denied_click.isError, "Desktop click unexpectedly bypassed the default-deny local permission."
            print("DESKTOP_CONTROL_DEFAULT_DENY_OK")

if __name__=="__main__": asyncio.run(main())
