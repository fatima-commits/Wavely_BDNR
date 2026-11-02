import os
import csv
from datetime import datetime
from bson.objectid import ObjectId
from connect import get_mongo_connection
from Mongo.MongoQueries import create_mongo_indexes

def populate_mongodb(): #Intento de carga de datos en MongoDB. No testeado aún. El flujo puede ser intuido.
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
    """Carga de datos en Cassandra"""
    # Paso 1: Conectarse a Cassandra usando get_cassandra_connection() de connect.py

    # Paso 2: Crear el keyspace "wavely" y las 8 tablas con la función
    #         create_cassandra_schema() de Cassandra/CassandraQueries.py

    # Paso 3: Leer los CSV de actividad de la carpeta data/ (reproducciones,
    #         búsquedas y canciones saltadas de cada usuario)

    # Paso 4: Insertar cada reproducción en las tablas que la necesitan
    #         (songs_by_session, songs_by_user_session, users_by_song y
    #         plays_by_user_day), porque en Cassandra se repite el dato en
    #         cada tabla según la consulta que va a responder

    # Paso 5: Por cada reproducción, aumentar en 1 el contador de
    #         plays_by_artist_day con UPDATE ... SET play_count = play_count + 1

    # Paso 6: Insertar las búsquedas en searches_by_user y las canciones
    #         saltadas en skips_by_user_month

    # Paso 7: Calcular cuántas veces escuchó cada usuario cada canción en el
    #         mes e insertar esos totales en top_songs_by_user_month

    # Paso 8: Usar inserciones por lotes (batch) para que la carga sea más rápida
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