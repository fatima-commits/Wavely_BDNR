# Proyecto BDNR
# Wavely

Wavely es una aplicación para consultar música al estilo de Spotify, que implementa funciones de catálogo musical y de historial de escucha para que el usuario tenga una experiencia 100% personalizada.

## Integrantes
| Nombre | Expediente |
|---|---|
| Fátima Vélez | 738493 |
| Nicole Armas | 757422 |
| Karlos Acosta | 757353 |

## Descripción de proyecto
Wavely combina tres bases de datos NoSQL, cada una usada para lo que mejor hace:

- **MongoDB (modelo documental):** catálogo musical; canciones, artistas, álbumes y playlists.
- **Cassandra (columnas amplias):** historial de actividad en el tiempo; reproducciones por sesión y por día, búsquedas, canciones saltadas y conteos de reproducciones.
- **Dgraph (grafos):** relaciones entre usuarios, artistas, canciones, géneros, playlists y conciertos; recomendaciones, colaboraciones y conciertos cercanos.

## Estructura
```
Wavely_BDNR/
├── Cassandra/        # Keyspace y tablas de Cassandra
├── Mongo/            # Índices y consultas de MongoDB
├── Dgraph/           # Schema, índices y consultas de Dgraph
├── data/             # Datos de prueba en CSV (mongo_data.csv y data/dgraph/)
├── connect.py        # Conexiones a MongoDB, Cassandra y Dgraph
├── populate.py       # Carga de datos en las tres bases
├── main.py           # Menú de consultas
└── README.md
```

## Flujo de trabajo

### Requisitos previos
1. Tener Docker instalado
2. Tener Python 3.8+ instalado

### 1. Levantar los contenedores
Para levantar MongoDB, Cassandra y Dgraph (incluyendo Ratel) al mismo tiempo, ejecuta desde la raíz del proyecto:
```bash
docker compose up -d
```
Ratel (interfaz de Dgraph) queda disponible en http://localhost:8000

### 2. Crear el entorno virtual e instalar dependencias
```bash
# Linux/MacOS
python3 -m venv ./venv
source ./venv/bin/activate

# Windows
python -m venv ./venv
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

### 3. Cargar los datos
Desde la raíz del proyecto:
```bash
python populate.py
```
Este script crea los esquemas e índices de cada base de datos y carga los datos de prueba de la carpeta `data/`.

### 4. Ejecutar las consultas
```bash
python main.py
```
Se muestra un menú con las 24 consultas del proyecto (8 por base de datos).