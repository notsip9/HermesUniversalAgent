# Connect an MCP-compatible client

Hermes uses the Model Context Protocol over a local standard-input/standard-output process. The exact settings screen differs by client; use that client's documentation for adding a local stdio MCP server.

## Example configuration

Replace the executable path with the actual path where you extracted Hermes. JSON backslashes must be escaped.

See mcp-config-example.json in this folder. Some MCP clients use a different configuration filename or schema. Keep the command pointed to the executable and use the client's documented format.

## Before connecting

1. Run HermesUniversalAgentSettings.exe.
2. Choose an existing workspace directory.
3. Leave file writes disabled initially.
4. Save settings.
5. Restart or refresh the MCP client after changing its server configuration.

## Verify the connection

Ask the client to call agent_status, then workspace_list. Confirm that the reported workspace is the folder you selected.

## Permissions

workspace_write is denied unless file writes are enabled in the local settings app and the individual tool request includes confirm=true. Keep this disabled unless you have a clear need for file creation or editing.
