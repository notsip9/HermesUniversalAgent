# Security

Hermes Universal Agent 0.3.0 exposes workspace file listing, text reading, optional confirmed file writing, local note storage/search, and basic system information through a local stdio MCP process.

It does not expose arbitrary command execution, screen capture, mouse control, keyboard control, or general Windows application control.

## Safe defaults

- File writes are disabled by default.
- A write requires both the local setting and confirm=true.
- Workspace paths are resolved against the configured root.
- Text file reads and writes are limited to 512,000 bytes per operation.
- Local settings and memory are stored in %LOCALAPPDATA%\HermesUniversalAgent.

## Reporting a vulnerability

Do not publish exploitable vulnerability details in a public issue. Contact the project publisher through the support channel listed on the official project page and include the affected version, concise reproduction steps, and impact. Do not include passwords, API keys, private files, or personal data.
