from pymongo import MongoClient
from cassandra.cluster import Cluster
import pydgraph

def get_mongo_connection():
    """Conexión a MongoDB"""
    client = MongoClient("mongodb://localhost:27017/")
    return client["wavely"]

def get_cassandra_connection():
    """Conexión a Cassandra"""
    cluster = Cluster(['localhost'], port=9042)
    session = cluster.connect()
    return session

def get_dgraph_connection():
    """Conexión a Dgraph"""
    client_stub = pydgraph.DgraphClientStub('localhost:9080')
    return pydgraph.DgraphClient(client_stub)
