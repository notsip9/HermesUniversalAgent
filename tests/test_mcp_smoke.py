from __future__ import annotations

import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def test_stdio_server_initializes_and_exposes_tools():
    async def exercise():
        params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "hermes_universal_agent.server"],
        )
        async with (
            stdio_client(params) as (read_stream, write_stream),
            ClientSession(read_stream, write_stream) as session,
        ):
            await session.initialize()
            result = await session.list_tools()
            names = {tool.name for tool in result.tools}
            expected = {
                "agent_status",
                "workspace_list",
                "workspace_read",
                "workspace_write",
                "memory_save",
                "memory_search",
                "system_info",
                "desktop_windows_list",
                "desktop_window_focus",
                "desktop_screen_capture",
                "desktop_mouse_click",
                "desktop_keyboard_type",
                "desktop_keyboard_hotkey",
            }
            assert expected.issubset(names)

    asyncio.run(exercise())
