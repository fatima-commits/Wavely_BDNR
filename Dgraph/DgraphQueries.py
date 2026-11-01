import pydgraph

# schema e índices
def create_dgraph_schema(client):
    schema = """
    # Atributos de User
    user_id: string @index(exact) .
    first_name: string .
    last_name: string .

    # Atributos de Artist
    artist_id: string @index(exact) .
    artist_name: string @index(exact, term) .

    # Atributos de Song
    song_id: string @index(exact) .
    song_title: string @index(term) .
    duration: int .

    # Atributos de Genre
    genre_name: string @index(exact) .

    # Atributos de Playlist
    playlist_id: string @index(exact) .
    playlist_name: string .
    is_public: bool @index(bool) .

    # Relaciones
    follows: [uid] @reverse @count .
    follows_artist: [uid] @reverse @count .
    likes: [uid] @reverse .
    favorite_genre: [uid] .
    created: [uid] @reverse .
    contains: [uid] @reverse .
    performed_by: [uid] @reverse .
    has_genre: [uid] @reverse .
    related_to: [uid] .
    collaborated_with: [uid] @reverse .

    # Tipos de nodo
    type User {
        user_id
        first_name
        last_name
        follows
        follows_artist
        likes
        favorite_genre
        created
    }

    type Artist {
        artist_id
        artist_name
        related_to
        collaborated_with
    }

    type Song {
        song_id
        song_title
        duration
        performed_by
        has_genre
    }

    type Genre {
        genre_name
    }

    type Playlist {
        playlist_id
        playlist_name
        is_public
        contains
    }
    """
    client.alter(pydgraph.Operation(schema=schema))
    print("Schema de Dgraph creado correctamente.")