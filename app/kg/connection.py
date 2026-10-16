"""Connections to the global curriculum graph (wmd_kg) and the student graph."""
from __future__ import annotations

import os
from typing import Any

from app.config import settings

KG_GRAPH = os.getenv("KG_GRAPH", "wmd_kg")
_override: Any = None  # tests inject an embedded FalkorDB client


def set_client(client: Any) -> None:
    global _override
    _override = client


def _client() -> Any:
    if _override is not None:
        return _override
    from falkordb import FalkorDB
    return FalkorDB(host=settings.falkordb_host, port=settings.falkordb_port)


def kg_graph() -> Any:
    return _client().select_graph(KG_GRAPH)


def student_graph() -> Any:
    return _client().select_graph(settings.graph_name)


def rows(graph: Any, query: str, params: dict | None = None, *, write: bool = False) -> list[list]:
    fn = graph.query if write else getattr(graph, "ro_query", graph.query)
    try:
        return fn(query, params or {}).result_set
    except Exception as exc:  # reading a graph key that has not been created yet
        if not write and "empty key" in str(exc):
            return []
        raise
