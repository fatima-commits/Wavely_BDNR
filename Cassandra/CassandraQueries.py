# keyspace y  tablas de Cassandra

def create_cassandra_schema(session):
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS wavely
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
    """)
    session.set_keyspace("wavely")
 
    # Tabla 1 (Req 1): canción específica dentro de una sesión
    session.execute("""
        CREATE TABLE IF NOT EXISTS songs_by_session (
            session_id int,
            item_in_session int,
            artist_name text,
            song_title text,
            song_length float,
            PRIMARY KEY ((session_id), item_in_session)
        )
    """)
 
    # Tabla 2 (Req 2): canciones de un usuario en una sesión, en orden
    session.execute("""
        CREATE TABLE IF NOT EXISTS songs_by_user_session (
            user_id int,
            session_id int,
            item_in_session int,
            artist_name text,
            song_title text,
            PRIMARY KEY ((user_id, session_id), item_in_session)
        ) WITH CLUSTERING ORDER BY (item_in_session ASC)
    """)
 
    # Tabla 3 (Req 3): usuarios que escucharon una canción
    session.execute("""
        CREATE TABLE IF NOT EXISTS users_by_song (
            song_title text,
            user_id int,
            first_name text,
            last_name text,
            PRIMARY KEY ((song_title), user_id)
        )
    """)
 
    # Tabla 4 (Req 4): historial de un usuario en un día, más recientes primero
    session.execute("""
        CREATE TABLE IF NOT EXISTS plays_by_user_day (
            user_id int,
            play_date date,
            played_at timestamp,
            song_title text,
            artist_name text,
            PRIMARY KEY ((user_id, play_date), played_at)
        ) WITH CLUSTERING ORDER BY (played_at DESC)
    """)
 
    # Tabla 5 (Req 5): reproducciones diarias de un artista (columna counter)
    session.execute("""
        CREATE TABLE IF NOT EXISTS plays_by_artist_day (
            artist_id int,
            play_date date,
            play_count counter,
            PRIMARY KEY ((artist_id), play_date)
        ) WITH CLUSTERING ORDER BY (play_date ASC)
    """)
 
    # Tabla 6 (Req 6): últimas búsquedas de un usuario
    session.execute("""
        CREATE TABLE IF NOT EXISTS searches_by_user (
            user_id int,
            searched_at timestamp,
            search_query text,
            PRIMARY KEY ((user_id), searched_at)
        ) WITH CLUSTERING ORDER BY (searched_at DESC)
    """)
 
    # Tabla 7 (Req 7): canciones saltadas por un usuario en un mes
    session.execute("""
        CREATE TABLE IF NOT EXISTS skips_by_user_month (
            user_id int,
            year_month text,
            skipped_at timestamp,
            song_title text,
            artist_name text,
            seconds_played int,
            PRIMARY KEY ((user_id, year_month), skipped_at)
        ) WITH CLUSTERING ORDER BY (skipped_at DESC)
    """)
 
    # Tabla 8 (Req 8): top de canciones de un usuario en un mes
    session.execute("""
        CREATE TABLE IF NOT EXISTS top_songs_by_user_month (
            user_id int,
            year_month text,
            play_count int,
            song_title text,
            artist_name text,
            first_name text STATIC,
            last_name text STATIC,
            PRIMARY KEY ((user_id, year_month), play_count, song_title)
        ) WITH CLUSTERING ORDER BY (play_count DESC, song_title ASC)
    """)
 
    print("Keyspace y tablas de Cassandra creados correctamente.")