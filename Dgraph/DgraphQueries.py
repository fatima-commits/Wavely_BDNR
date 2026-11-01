import pydgraph
 
# Creación del schema e índices
def create_dgraph_schema(client):
    schema = """
    # Atributos de User
    user_id: string @index(exact) .
    first_name: string .
    last_name: string .
    email: string .
    age: int .
    created_at: datetime .
 
    # Atributos de Artist
    artist_id: string @index(exact) .
    artist_name: string @index(exact, term) .
    country: string .
    listeners: int .
 
    # Atributos de Song
    song_id: string @index(exact) .
    song_title: string .
    duration: int .
    release_date: datetime .
 
    # Atributos de Genre
    genre_name: string .
 
    # Atributos de Playlist
    playlist_id: string @index(exact) .
    playlist_name: string .
    is_public: bool @index(bool) .
 
    # Atributos de Concert
    concert_id: string @index(exact) .
    concert_name: string .
    location: geo @index(geo) .
    concert_date: datetime @index(day) .
    price: int .
 
    # Relaciones
    follows: [uid] @reverse .
    follows_artist: [uid] @reverse .
    favorite_genre: [uid] .
    liked: [uid] .
    saved: [uid] .
    created: [uid] @reverse .
    contains: [uid] .
    performs: [uid] @reverse .
    has_genre: [uid] .
    collaborated_with: [uid] .
    performs_in: [uid] @reverse .
 
    # Tipos de nodo
    type User {
        user_id
        first_name
        last_name
        email
        age
        created_at
        follows
        follows_artist
        favorite_genre
        liked
        saved
        created
    }
 
    type Artist {
        artist_id
        artist_name
        country
        listeners
        performs
        collaborated_with
        performs_in
    }
 
    type Song {
        song_id
        song_title
        duration
        release_date
        has_genre
    }
 
    type Genre {
        genre_name
    }
 
    type Playlist {
        playlist_id
        playlist_name
        is_public
        created_at
        contains
    }
 
    type Concert {
        concert_id
        concert_name
        location
        concert_date
        country
        price
    }
    """
    client.alter(pydgraph.Operation(schema=schema))
    print("Schema de Dgraph creado correctamente.")