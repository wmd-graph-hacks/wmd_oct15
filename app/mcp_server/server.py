"""MCP server exposing the graph tools. One server instance is bound to one authenticated uid."""
from __future__ import annotations

import inspect
import json
import os
from typing import Annotated

from mcp.server.mcpserver import MCPServer
from pydantic import Field

from app.agent.tools import ToolError, Toolbox


def build_server(uid: str, subject: str | None = None, **toolbox_kwargs) -> MCPServer:
    box = Toolbox(uid, subject=subject, **toolbox_kwargs)
    server = MCPServer("wmd-study-graph")

    def register(name: str) -> None:
        spec = box.specs()[name]

        def tool(**kwargs) -> str:
            try:
                return json.dumps(box.call(name, kwargs))
            except ToolError as exc:
                return json.dumps({"error": str(exc)})

        params = [
            inspect.Parameter(
                fname, inspect.Parameter.KEYWORD_ONLY,
                default=inspect.Parameter.empty if f.is_required() else f.default,
                annotation=Annotated[f.annotation, Field(description=f.description)] if f.description else f.annotation)
            for fname, f in spec.args.model_fields.items()
        ]
        tool.__signature__ = inspect.Signature(params, return_annotation=str)  # type: ignore[attr-defined]
        tool.__annotations__ = {p.name: p.annotation for p in params} | {"return": str}
        tool.__name__ = name
        tool.__doc__ = spec.description
        server.add_tool(tool, name=name, description=spec.description)

    for n in box.specs():
        register(n)
    return server


def main() -> None:  # stdio: python -m app.mcp_server.server  (uid from MCP_UID, demo only)
    uid = os.environ.get("MCP_UID", "demo-student")
    build_server(uid, os.environ.get("MCP_SUBJECT") or None).run()


if __name__ == "__main__":
    main()
