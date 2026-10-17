import pytest

from app.kg import connection
from app.kg.loader import ARTIFACTS_ROOT, load_all
from app.kg.parse import load_curriculum


def _client():
    """Embedded FalkorDB when available (Python 3.12+), else the Docker FalkorDB on localhost:6379."""
    try:
        from redislite.falkordb_client import FalkorDB
        return FalkorDB()
    except ImportError:
        from falkordb import FalkorDB
        return FalkorDB(host="localhost", port=6379)


@pytest.fixture(scope="session")
def db():
    client = _client()
    connection.set_client(client)
    report = load_all(ARTIFACTS_ROOT)
    assert not [k for k, v in report.items() if "error" in v], report
    yield client
    connection.set_client(None)


@pytest.fixture()
def uid(db):
    import secrets
    return "u-" + secrets.token_hex(4)
