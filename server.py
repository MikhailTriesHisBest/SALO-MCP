import json
import subprocess
import os
from typing import Dict, Any, List
from fastmcp import FastMCP

APPS_FILE = os.path.join(os.path.dirname(__file__), "apps.json")

mcp = FastMCP("SALO MCP")


def _load() -> Dict[str, Any]:
    if not os.path.exists(APPS_FILE):
        data = {"apps": []}
        # create parent directory if needed (should exist)
        with open(APPS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return data
    try:
        with open(APPS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise ValueError("apps.json is corrupted.")


def _save(data: Dict[str, Any]) -> None:
    with open(APPS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


@mcp.tool()
def list_apps() -> List[Dict[str, Any]]:
    data = _load()
    return data.get("apps", [])


@mcp.tool()
def add_app(name: str, launch_string: str, location: str, notes: str) -> Dict[str, Any]:
    name = (name or "").strip()
    launch_string = (launch_string or "").strip()
    if not name:
        return {"success": False, "error": "name must not be empty."}
    if not launch_string:
        return {"success": False, "error": "launch_string must not be empty."}

    data = _load()
    apps = data.setdefault("apps", [])
    for app in apps:
        if app.get("name", "").lower() == name.lower():
            return {"success": False, "error": f"App '{name}' already exists."}

    new_app = {
        "name": name,
        "launch_string": launch_string,
        "location": location or "",
        "notes": notes or "",
    }
    apps.append(new_app)
    _save(data)
    return {"success": True}


@mcp.tool()
def launch_app(name: str) -> Dict[str, Any]:
    name = (name or "").strip()
    if not name:
        return {"success": False, "error": "name must not be empty."}
    try:
        data = _load()
    except ValueError as e:
        return {"success": False, "error": str(e)}

    apps = data.get("apps", [])
    match = None
    for app in apps:
        if app.get("name", "").lower() == name.lower():
            match = app
            break
    if match is None:
        return {"success": False, "error": f"App '{name}' not found."}

    try:
        subprocess.Popen(
            match["launch_string"],
            shell=True,
            creationflags=(subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP),
            close_fds=True,
        )
    except Exception as e:
        return {"success": False, "error": str(e)}

    return {"success": True}


if __name__ == "__main__":
    mcp.run()
