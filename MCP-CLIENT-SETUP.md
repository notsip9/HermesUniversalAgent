# MCP client setup

Hermes uses the Model Context Protocol over a local stdio process. Configure your MCP-compatible client to launch the packaged `HermesUniversalAgentMCP.exe`, or use `python -m hermes_universal_agent.server` in a development environment.

Example command configuration (adapt the schema to the client's documentation):

```json
{
  "mcpServers": {
    "hermes-universal-agent": {
      "command": "C:\\Tools\\HermesUniversalAgent\\HermesUniversalAgentMCP.exe"
    }
  }
}
```

Before connecting, run the settings application and choose the workspace. Keep file writes, desktop interaction, and screen capture disabled until each capability is intentionally needed. Restart the MCP client after changing settings or its server configuration.

The original ChatGPT Desktop local-plugin route remains separate and subject to OpenAI approval and allowlisting. A public GitHub release does not grant access to that route.
