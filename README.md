# Hermes Universal Agent 0.3.0

**Windows x64 | Proprietary software | Portable release**

Hermes Universal Agent is a local-first MCP companion for Windows. It provides an MCP server and a small settings application for configuring a local workspace and file-write permissions.

## What this release does

- Lists files and folders inside one configured workspace.
- Reads UTF-8 text files inside that workspace (maximum 512 KB per file).
- Writes files only when local write permission is enabled and the MCP request explicitly confirms the write.
- Saves and searches private notes in a local SQLite database.
- Reports basic operating-system information.

## What it does not do

This release does **not** provide screen capture, mouse or keyboard control, arbitrary shell execution, or general control of Windows applications. It is not a standalone AI assistant. An MCP-compatible AI client is required to use the tools.

## Requirements

- Windows 10 or Windows 11, 64-bit.
- An MCP client that supports launching a local server over stdio.

## Quick start

1. Extract this ZIP to a folder that you control, for example C:\Tools\HermesUniversalAgent.
2. Run HermesUniversalAgentSettings.exe.
3. Choose the workspace folder and leave file writes disabled unless you intentionally need them. Save settings.
4. Configure your MCP-compatible client to launch server\HermesUniversalAgentMCP.exe. See MCP-CLIENT-SETUP.md.
5. In the AI client, start with read-only workspace operations. Enable writes only when necessary.

The settings and local memory database are stored under %LOCALAPPDATA%\HermesUniversalAgent. Removing the extracted program folder does not automatically remove this local data.

## MCP tools

- agent_status
- workspace_list
- workspace_read
- workspace_write
- memory_save
- memory_search
- system_info

## Security model

- Workspace access is confined to the configured workspace root.
- File writes are disabled by default.
- A write requires both the local setting to be enabled and confirm=true in the tool call.
- The MCP executable uses stdio; this release does not require a public server endpoint or tunnel.
- Review SECURITY.md.

## ChatGPT Desktop

The original ChatGPT Desktop local-plugin route is separate and remains subject to OpenAI's approval and allowlisting requirements. This public Windows package does not itself grant access to that route. For other MCP-compatible clients, follow their local stdio server configuration instructions.

## Licence and support

This is proprietary software. Use is governed by LICENSE.txt. No source code is included in this binary release.

Report security issues privately as described in SECURITY.md.
