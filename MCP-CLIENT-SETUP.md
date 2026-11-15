# Connect an MCP-compatible client

Hermes runs a local MCP server over standard input/output (stdio). It does not require a public endpoint, tunnel client, port forwarding, bearer token, or scheduled task.

## ChatGPT Desktop

The intended ChatGPT Desktop experience is a desktop-only plugin that launches the local companion. This route requires OpenAI approval and allowlisting. The public Windows package or this repository does not itself grant access to that integration.

When the approved plugin is available, users should install it through the supported ChatGPT Desktop experience and follow the plugin's local setup instructions. Do not ask users to create a tunnel or manually register an MCP server for that approved plugin flow.

## Other MCP-compatible desktop clients

Other clients may support local stdio servers through their own configuration screens. Use the client's official instructions and the actual executable path. See mcp-config-example.json for a generic example; configuration schemas vary by client.

## Local setup

1. Extract the Windows package to a folder you control.
2. Run HermesUniversalAgentSettings.exe.
3. Choose an existing workspace directory.
4. Leave all permissions disabled initially.
5. Save settings.
6. Configure only the client integration you intend to use, following that client's documented process.

## Verify the connection

Ask the client to call agent_status, then workspace_list. Confirm that the reported workspace is the folder you selected.

## Permissions

Every sensitive operation requires local permission in Hermes Settings. File writes, screen capture, window focus, mouse clicks, keyboard typing, and keyboard shortcuts also require confirm=true on each individual tool call. Keep permissions disabled unless you have a clear need for them.
