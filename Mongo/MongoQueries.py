from bson.objectid import ObjectId
from pymongo import ASCENDING, DESCENDING, TEXT

# Creación de índices
def create_mongo_indexes(db):
    # Índice para el req 5
    db.songs.create_index([("title", TEXT)], default_language="spanish")
    
    # Índices de los reqs 4 y 8
    db.albums.create_index([("artist_id", ASCENDING), ("release_date", DESCENDING)])
    db.albums.create_index([("genre", ASCENDING), ("release_date", DESCENDING)])
    
    # Índices de los 6 y 7
    db.songs.create_index([("album.album_id", ASCENDING)])
    db.songs.create_index([("artist.artist_id", ASCENDING)])

# Requerimiento 1
def get_song_details(db, song_id_str):
    """
    Requerimiento 1: Detalles de una canción específica.
    """
    try:
        song_id = ObjectId(song_id_str)
    except Exception:
        return {"error": "Formato de ID inválido"}

    filtro = {"_id": song_id}

    proyeccion = {
        "song_id": "$_id",
        "title": 1,
        "duration_ms": 1,
        "release_date": 1,
        "artist.artist_id": 1,
        "artist.name": 1,
        "album.album_id": 1,
        "album.name": 1,
        "_id": 0
    }

    cancion = db.songs.find_one(filtro, proyeccion)
    
    return cancion

def get_artist_profile(db, artist_id_str):
    #Req 2
    try:
        artist_id = ObjectId(artist_id_str)
    except Exception:
        return {"error": "Formato de ID inválido"}

    filtro = {"_id": artist_id}

    proyeccion = {
        "artist_id": "$_id",
        "name": 1,
        "biography": 1,
        "monthly_listeners": 1,
        "social_links": 1,
        "_id": 0
    }

    artista = db.artists.find_one(filtro, proyeccion)
    
    return artista

#req 3
def get_playlist_content(db, playlist_id_str):
    try:
        playlist_id = ObjectId(playlist_id_str)
    except Exception:
        return {"error": "Formato de ID inválido"}

    filtro = {"_id": playlist_id}

    proyeccion = {
        "playlist_id": "$_id",
        "name": 1,
        "description": 1,
        "owner_id": 1,
        "is_public": 1,
        "tracks.song_id": 1,
        "tracks.title": 1,
        "tracks.artist_name": 1,
        "tracks.date_added": 1,
        "_id": 0
    }

    playlist = db.playlists.find_one(filtro, proyeccion)
    return playlist


# req 4
def get_albums_by_artist(db, artist_id_str):
    try:
        artist_id = ObjectId(artist_id_str)
    except Exception:
        return {"error": "Formato de ID inválido"}

    filtro = {"artist_id": artist_id}

    proyeccion = {
        "album_id": "$_id",
        "title": 1,
        "release_date": 1,
        "album_type": 1,
        "_id": 0
    }

    cursor = db.albums.find(filtro, proyeccion).sort("release_date", DESCENDING)
    return list(cursor)


# Req 5
def search_songs_by_text(db, search_text):
    db.songs.create_index([("title", TEXT)], default_language="spanish")
    filtro = {
        "$text": {
            "$search": search_text
        }
    }

    proyeccion = {
        "song_id": "$_id",
        "title": 1,
        "artist_name": "$artist.name",
        "album_name": "$album.name",
        "_id": 0
    }

    cursor = db.songs.find(filtro, proyeccion).limit(20)
    return list(cursor)


# req 6
def get_album_duration_stats(db, album_id_str):
    try:
        album_id = ObjectId(album_id_str)
    except Exception:
        return {"error": "Formato de ID inválido"}

    pipeline = [
        {
            "$match": {
                "album.album_id": album_id
            }
        },
        {
            "$group": {
                "_id": "$album.album_id",
                "total_tracks": {"$sum": 1},
                "total_duration_ms": {"$sum": "$duration_ms"}
            }
        },
        {
            "$project": {
                "album_id": "$_id",
                "total_tracks": 1,
                "total_duration_ms": 1,
                "_id": 0
            }
        }
    ]

    resultado = list(db.songs.aggregate(pipeline))
    return resultado[0] if resultado else None


# req 7
def get_artist_catalog_summary(db, artist_id_str):
    try:
        artist_id = ObjectId(artist_id_str)
    except Exception:
        return {"error": "Formato de ID inválido"}

    pipeline = [
        {
            "$match": {
                "artist.artist_id": artist_id
            }
        },
        {
            "$group": {
                "_id": "$artist.artist_id",
                "total_songs_released": {"$sum": 1},
                "average_song_duration_ms": {"$avg": "$duration_ms"}
            }
        },
        {
            "$project": {
                "artist_id": "$_id",
                "total_songs_released": 1,
                "average_song_duration_ms": 1,
                "_id": 0
            }
        }
    ]

    resultado = list(db.songs.aggregate(pipeline))
    return resultado[0] if resultado else None

# req 8
def get_latest_releases_by_genre(db, genre):
    filtro = {"genre": genre}

    proyeccion = {
        "album_id": "$_id",
        "title": 1,
        "artist_name": 1,
        "release_date": 1,
        "_id": 0
    }

    cursor = db.albums.find(filtro, proyeccion).sort("release_date", DESCENDING)
    return list(cursor)