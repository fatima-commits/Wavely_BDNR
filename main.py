# Menú consultas de Wavely
CONSULTAS = [
    "Historial de reproducción por sesión",
    "Canciones escuchadas por usuario en una sesión",
    "Usuarios que escucharon una canción específica",
    "Historial de reproducción de un usuario por día",
    "Reproducciones diarias de un artista",
    "Historial de búsquedas de un usuario",
    "Canciones saltadas por un usuario en un mes",
    "Top canciones más escuchadas de un usuario en un período",
    "Detalles de una canción específica",
    "Perfil de un artista",
    "Contenido de una playlist",
    "Álbumes de un artista ordenados por fecha",
    "Búsqueda de canciones por texto",
    "Duración total de un álbum",
    "Resumen del catálogo de un artista",
    "Lanzamientos más recientes por género",
    "Artistas recomendados por mi red",
    "Canciones de artistas relacionados",
    "Grados de separación entre artistas",
    "Usuarios con gustos similares",
    "Playlists de mi red con un artista",
    "Red de colaboraciones de un artista",
    "Amigos mutuos que siguen a un artista",
    "Conciertos dentro de cierta zona"
]


def main():
    while True:
        print("\n========== WAVELY ==========")
        for i, consulta in enumerate(CONSULTAS, start=1):
            print(f"{i}. {consulta}")
        print("0. Salir")

        opcion = input("Elige una consulta: ")

        if opcion == "0":
            print("Hasta luego.")
            break
        elif opcion.isdigit() and 1 <= int(opcion) <= len(CONSULTAS):
            print(f"\nConsulta seleccionada: {CONSULTAS[int(opcion) - 1]}")
            print("(Pendiente de implementar)")
        else:
            print("Opción no válida, intenta de nuevo.")


if __name__ == "__main__":
    main()