# Proyecto BDNR
# Wavely

Wavely es una aplicación para consultar música al estilo de Spotify, que implementa funciones de catálogo musical y de historial de escucha para que el usuario tenga una experiencia 100% personalizada. 

## Integrantes
Por Fátima Vélez
Por Nicole Armas
Por Karlos Acosta

## Descripción de proyecto
Wavely es una aplicación para consultar música al estilo de Spotify, que implementa funciones de catálogo musical y de historial de escucha para que el usuario tenga una experiencia 100% personalizada. 

## Flujo de trabajo

### Requisitos previos
1. Tener Docker instalado
2. Tener Python 3.8+ instalado.

# Docker Compose
Para levantar los contenedores de MongoDB, Cassandra y Dgraph (incluyendo Ratel) simultáneamente, ejecuta desde la raíz del proyecto:
```bash
docker-compose up -d
```
### Setup a python virtual env with python mongodb installed
```
# If pip is not present in you system
sudo apt update
sudo apt install python3-pip

# Install and activate virtual env (Linux/MacOS)
python3 -m pip install virtualenv
python3 -m venv ./venv
source ./venv/bin/activate

# Install and activate virtual env (Windows)
python3 -m pip install virtualenv
python3 -m venv ./venv
.\venv\Scripts\Activate.ps1

# Install project python requirements
pip install -r requirements.txt
```

### To run the API service
```
python -m uvicorn main:app --reload
```

### To load data
Ensure you have a running every container instances
i.e.:
```
docker run --name mongodb -d -p 27017:27017 mongo
```
Once your API service is running (see step above), run the populate script
```
cd data/
python populate.py
```
