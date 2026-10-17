"""Run the app against an embedded FalkorDB (no Docker): pip install falkordblite, then
python scripts/run_embedded.py   -> http://localhost:8000/login (demo auth)."""
import uvicorn
from redislite.falkordb_client import FalkorDB

from app.kg import connection

connection.set_client(FalkorDB("/tmp/wmd-embedded.rdb"))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000)
