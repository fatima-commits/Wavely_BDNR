import csv
from connect import get_mongo_connection

def populate_mongodb():
    """Lógica para poblar las colecciones de MongoDB usando el archivo CSV modelado[cite: 21]"""
    db = get_mongo_connection()
    
    # Paso 1: Leer el archivo data/songs.csv
    # Paso 2: Transformar los datos planos del CSV al modelo anidado requerido
    # Paso 3: Castear los tipos de datos en Python
    # Paso 4: Insertar masivamente en db.songs usando insert_many()
    
    # Paso 5: Repetir proceso para data/artists.csv insertando en db.artists
    # Paso 6: Repetir proceso para data/playlists.csv embebiendo el arreglo 'tracks'
    # Paso 7: Repetir proceso para data/albums.csv e insertar en db.albums
    
    print("Datos de MongoDB cargados y formateados.")

def populate_cassandra():
    """Responsabilidad del equipo"""
    # Paso 1: Leer los archivos CSV de logs de actividad e historial de usuario
    # Paso 2: Ejecutar inserciones batch (execute_batch) en las distintas tablas creadas por requerimiento
    pass

def populate_dgraph():
    """Responsabilidad del equipo (Pendiente en clase)"""
    # Paso 1: Leer los archivos CSV correspondientes a los nodos (User, Artist, Song, etc.)
    # Paso 2: Estructurar las mutaciones en formato JSON
    # Paso 3: Ejecutar las mutaciones en Dgraph usando pydgraph
    pass

if __name__ == "__main__":
    print("Iniciando scripts de población...")
    populate_mongodb()
    # populate_cassandra()
    # populate_dgraph()