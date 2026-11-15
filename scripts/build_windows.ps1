$ErrorActionPreference = "Stop"
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m pytest -q
python -m PyInstaller --noconfirm --clean --onefile --name HermesUniversalAgentMCP --collect-submodules mcp.server --collect-submodules mcp.shared --collect-data mcp --hidden-import mcp.server.fastmcp.utilities.types scripts/run_server.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m PyInstaller --noconfirm --clean --onefile --windowed --name HermesUniversalAgentSettings scripts/run_settings.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Build complete. Executables are in dist\"
