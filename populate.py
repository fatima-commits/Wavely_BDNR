import os
import csv
from datetime import datetime
from bson.objectid import ObjectId
from connect import get_mongo_connection
from Mongo.MongoQueries import create_mongo_indexes

def populate_mongodb():
    db = get_mongo_connection()

    # Limpiar colecciones previas para evitar errores
    db.songs.delete_many({})
    db.artists.delete_many({})
    db.albums.delete_many({})
    db.playlists.delete_many({})

    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "data", "mongo_data.csv")

    songs_dict = {}
    artists_dict = {}
    albums_dict = {}
    playlists_dict = {}

    with open(csv_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            song_oid = ObjectId(row["song_id"])
            artist_oid = ObjectId(row["artist_id"])
            album_oid = ObjectId(row["album_id"])
            playlist_oid = ObjectId(row["playlist_id"])

            # Documento para colección songs
            if song_oid not in songs_dict:
                songs_dict[song_oid] = {
                    "_id": song_oid,
                    "title": row["song_title"],
                    "duration_ms": int(row["duration_ms"]),
                    "release_date": datetime.strptime(row["song_release_date"], "%Y-%m-%d"),
                    "genre": row["genre"],
                    "artist": {
                        "artist_id": artist_oid,
                        "name": row["artist_name"]
                    },
                    "album": {
                        "album_id": album_oid,
                        "name": row["album_title"],
                        "cover_url": row["cover_url"]
                    }
                }

            # Documento para colección artists
            if artist_oid not in artists_dict:
                artists_dict[artist_oid] = {
                    "_id": artist_oid,
                    "name": row["artist_name"],
                    "biography": row["biography"],
                    "monthly_listeners": int(row["monthly_listeners"]),
                    "social_links": row["social_links"].split("|")
                }

            # Documento para colección albums
            if album_oid not in albums_dict:
                albums_dict[album_oid] = {
                    "_id": album_oid,
                    "title": row["album_title"],
                    "artist_id": artist_oid,
                    "artist_name": row["artist_name"],
                    "release_date": datetime.strptime(row["album_release_date"], "%Y-%m-%d"),
                    "album_type": row["album_type"],
                    "genre": row["genre"],
                    "cover_url": row["cover_url"]
                }

            # Documento para colección playlists (agrupando arreglo tracks)
            if playlist_oid not in playlists_dict:
                playlists_dict[playlist_oid] = {
                    "_id": playlist_oid,
                    "name": row["playlist_name"],
                    "description": row["playlist_desc"],
                    "owner_id": ObjectId(row["owner_id"]),
                    "is_public": row["is_public"].lower() == "true",
                    "tracks": []
                }

            playlists_dict[playlist_oid]["tracks"].append({
                "song_id": song_oid,
                "title": row["song_title"],
                "artist_name": row["artist_name"],
                "date_added": datetime.strptime(row["date_added"], "%Y-%m-%d")
            })

    # Inserción en MongoDB
    if songs_dict:
        db.songs.insert_many(list(songs_dict.values()))
    if artists_dict:
        db.artists.insert_many(list(artists_dict.values()))
    if albums_dict:
        db.albums.insert_many(list(albums_dict.values()))
    if playlists_dict:
        db.playlists.insert_many(list(playlists_dict.values()))

    # Creación de los índices definidos en el reporte
    create_mongo_indexes(db)
    print("Datos e índices de MongoDB cargados correctamente.")

def populate_cassandra():
    """Responsabilidad del equipo"""
    # Paso 1: Leer los archivos CSV de logs de actividad e historial de usuario
    # Paso 2: Ejecutar inserciones batch (execute_batch) en las distintas tablas creadas por requerimiento
    pass

def populate_dgraph():

    """Responsabilidad de Nicole: carga de datos en Dgraph"""
    # Paso 1: Conectarse a Dgraph usando get_dgraph_connection() de connect.py

    # Paso 2: Borrar los datos que ya existan en Dgraph para no duplicar
    #         información si se vuelve a correr el script

    # Paso 3: Crear el schema (tipos de nodo, atributos e índices) con la
    #         función create_dgraph_schema() de Dgraph/DgraphQueries.py

    # Paso 4: Leer los CSV de la carpeta data/dgraph que tienen los nodos:
    #         users.csv, artists.csv, songs.csv, genres.csv y playlists.csv
    #         y convertir cada fila en un nodo con su tipo y sus atributos

    # Paso 5: Leer relations.csv, donde cada fila dice qué nodo se conecta
    #         con cuál y con qué relación (por ejemplo: user_10 follows user_1),
    #         y agregar esas conexiones a los nodos

    # Paso 6: En las colaboraciones entre artistas (collaborated_with),
    #         guardar también cuántas canciones hicieron juntos (num_canciones)

    # Paso 7: Enviar todos los nodos y relaciones a Dgraph en una sola
    #         transacción y confirmarla para que se guarden
    pass

if __name__ == "__main__":
    print("Iniciando scripts de población...")
    populate_mongodb()
    # populate_cassandra()
    # populate_dgraph()