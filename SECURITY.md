# Security

Hermes Universal Agent is a local-first Windows MCP companion. The MCP server uses stdio and does not expose a listening network service.

## Permission model

- Workspace access is confined to the configured workspace root, including resolved symlink targets.
- File writes are disabled by default and require local permission plus per-call `confirm=true`.
- Desktop interaction is disabled by default and requires local permission plus per-call `confirm=true` for each action.
- Screen capture is a separate permission, disabled by default, and each capture requires `confirm=true`.
- Text file operations are limited to 512,000 bytes. A single typing operation is limited to 500 characters.
- No arbitrary shell execution, unattended automation, or background screen monitoring is provided.

## Reporting vulnerabilities

Please use GitHub's private vulnerability reporting feature if enabled for this repository. If it is unavailable, do not publish exploitable details in a public issue; contact the publisher through the repository owner profile. Do not include passwords, API keys, private files, or personal data.
