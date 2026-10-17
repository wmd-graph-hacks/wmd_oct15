from falkordb import FalkorDB

from app.config import settings


def graph_connection():
    client = FalkorDB(host=settings.falkordb_host, port=settings.falkordb_port)
    return client.select_graph(settings.graph_name)
