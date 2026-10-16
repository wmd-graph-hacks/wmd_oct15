"""Optional dense embeddings (LiteLLM). Off unless EMBEDDING_MODEL is set; retrieval then fuses BM25 and cosine."""
from __future__ import annotations

import os
from typing import Any, Awaitable, Callable

from app.kg.connection import kg_graph, rows

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "")
EmbedFn = Callable[[list[str]], Awaitable[list[list[float]]]]


async def litellm_embed(texts: list[str], model: str | None = None) -> list[list[float]]:
    from litellm import aembedding
    resp = await aembedding(model=model or EMBEDDING_MODEL, input=texts, timeout=30)
    return [d["embedding"] for d in resp["data"]]


async def embed_all_chunks(embed: EmbedFn | None = None, graph: Any | None = None, batch: int = 64) -> int:
    """Embed every Chunk missing a vector and store it on the node. Returns number embedded."""
    from app.rag import retrieve
    g = graph or kg_graph()
    embed = embed or litellm_embed
    todo = rows(g, "MATCH (c:Chunk) WHERE c.embedding IS NULL RETURN c.id, c.text")
    for i in range(0, len(todo), batch):
        part = todo[i:i + batch]
        vecs = await embed([t[1] for t in part])
        g.query("UNWIND $rows AS r MATCH (c:Chunk {id:r.id}) SET c.embedding = r.v",
                {"rows": [{"id": t[0], "v": v} for t, v in zip(part, vecs)]})
    retrieve.reset_index()
    return len(todo)


if __name__ == "__main__":
    import asyncio
    if not EMBEDDING_MODEL:
        raise SystemExit("Set EMBEDDING_MODEL (e.g. gemini/text-embedding-004) first")
    print("embedded", asyncio.run(embed_all_chunks()))
