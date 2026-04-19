# SALO MCP

SALO MCP is a minimal Model Context Protocol (MCP) server for Windows that manages and launches local applications for MCP-compatible AI clients.

## Features

- Register, list, and launch applications via a small MCP toolset
- Stores app registry in a local `apps.json` file
- Uses `subprocess.Popen` so launched apps remain running after the server stops

## Requirements

- Windows
- Python 3.10+

## Setup

1. Open a terminal in `C:\Projects\SALO MCP\`
2. Create and activate a venv:
   python -m venv .venv
   .venv\Scripts\activate
3. Install dependencies:
   pip install -r requirements.txt
4. Run the server (stdio mode):
   python server.py

## Connecting to an AI agent (example: Claude Desktop)

Add to `%APPDATA%\Claude\claude_desktop_config.json` under `mcpServers`:

```json
{
  "mcpServers": {
    "salo-mcp": {
      "command": "C:\\Projects\\SALO MCP\\.venv\\Scripts\\python.exe",
      "args": ["C:\\Projects\\SALO MCP\\server.py"]
    }
  }
}
```

Restart Claude Desktop after saving.

## apps.json schema

```json
{
  "apps": [
    {
      "name": "Notepad",
      "launch_string": "notepad.exe",
      "location": "C:\\Windows\\System32\\notepad.exe",
      "notes": "Built-in Windows text editor"
    }
  ]
}
```

- `name` must be unique (case-insensitive)
- `launch_string` is the command passed to the shell
- `location` and `notes` are informational

## Usage examples

- List apps: call `list_apps()` via MCP
- Add app: `add_app(name, launch_string, location, notes)`
- Launch app: `launch_app(name)`

## Security & Safety

- `launch_string` is executed with `shell=True`. Only add trusted commands to `apps.json` and avoid running this server exposed to untrusted users.

## Creator

Created by Mikhail Ostras

LinkedIn: https://www.linkedin.com/in/mikhail-ostras-a84a5823a/

## License

MIT License

---

Copyright (c) 2026 Mikhail Ostras
