import pygame
import random

# Constantes
ANCHO_PANTALLA = 600
ALTO_PANTALLA = 800
TAMANIO_CUADRADO = 30
ANCHO_TABLERO = 10
ALTO_TABLERO = 20
COLOR_FONDO = (0, 0, 0)
COLOR_LINEA = (255, 255, 255)
COLOR_PIEZA = (255, 0, 0)  # Rojo para la pieza

# Formas de las piezas de Tetris
formas = {
    'I': [[(0, 1), (0, 2), (0, 3), (0, 4)]],
    'O': [[(1, 1), (1, 2), (2, 1), (2, 2)]],
    'T': [[(1, 0), (1, 1), (1, 2), (0, 1)],
          [(0, 1), (1, 1), (2, 1), (1, 2)],
          [(1, 0), (1, 1), (1, 2), (2, 1)],
          [(0, 1), (1, 1), (2, 1), (1, 0)]],
    'L': [[(0, 0), (0, 1), (0, 2), (1, 2)],
          [(1, 0), (2, 0), (1, 1), (1, 2)],
          [(0, 1), (1, 1), (2, 1), (2, 2)],
          [(0, 0), (1, 0), (1, 1), (1, 2)]],
    'J': [[(0, 2), (0, 1), (0, 0), (1, 0)],
          [(1, 0), (1, 1), (1, 2), (2, 2)],
          [(0, 0), (1, 0), (2, 0), (2, 1)],
          [(2, 0), (2, 1), (2, 2), (1, 2)]],
    'S': [[(0, 1), (0, 2), (1, 0), (1, 1)],
          [(1, 1), (2, 1), (1, 2), (2, 2)],
          [(0, 1), (0, 2), (1, 0), (1, 1)],
          [(1, 1), (2, 1), (1, 2), (2, 2)]],
    'Z': [[(0, 0), (0, 1), (1, 1), (1, 2)],
          [(1, 0), (2, 0), (1, 1), (2, 1)],
          [(0, 0), (0, 1), (1, 1), (1, 2)],
          [(1, 0), (2, 0), (1, 1), (2, 1)]]
}

# Inicializa Pygame
pygame.init()
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Tetris")

# Crea la fuente para el puntaje
fuente = pygame.font.Font(None, 36)

# Crea el tablero
tablero = [[0 for _ in range(ANCHO_TABLERO)] for _ in range(ALTO_TABLERO)]

# Crea la pieza
def crear_pieza():
    """Crea una nueva pieza aleatoria."""
    tipo_pieza = random.choice(list(formas.keys()))
    rotacion = random.randint(0, len(formas[tipo_pieza]) - 1)
    x = int(ANCHO_TABLERO / 2 - len(formas[tipo_pieza][rotacion][0]) / 2)
    y = 0
    return {
        'tipo': tipo_pieza,
        'rotacion': rotacion,
        'x': x,
        'y': y
    }

# Dibuja la pieza
def dibujar_pieza(pieza):
    """Dibuja la pieza actual en la pantalla."""
    for fila, columna in formas[pieza['tipo']][pieza['rotacion']]:
        x = pieza['x'] + fila
        y = pieza['y'] + columna
        if 0 <= x < ANCHO_TABLERO and 0 <= y < ALTO_TABLERO:
            pygame.draw.rect(pantalla, COLOR_PIEZA,
                             pygame.Rect(x * TAMANIO_CUADRADO, y * TAMANIO_CUADRADO,
                                         TAMANIO_CUADRADO, TAMANIO_CUADRADO))

# Dibuja el tablero
def dibujar_tablero():
    """Dibuja el tablero de juego en la pantalla."""
    for fila in range(ALTO_TABLERO):
        for columna in range(ANCHO_TABLERO):
            if tablero[fila][columna] == 1:
                pygame.draw.rect(pantalla, COLOR_PIEZA,
                                 pygame.Rect(columna * TAMANIO_CUADRADO, fila * TAMANIO_CUADRADO,
                                             TAMANIO_CUADRADO, TAMANIO_CUADRADO))
    # Dibuja las lineas del tablero
    for x in range(ANCHO_TABLERO + 1):
        pygame.draw.line(pantalla, COLOR_LINEA,
                         (x * TAMANIO_CUADRADO, 0), (x * TAMANIO_CUADRADO, ALTO_TABLERO * TAMANIO_CUADRADO))
    for y in range(ALTO_TABLERO + 1):
        pygame.draw.line(pantalla, COLOR_LINEA,
                         (0, y * TAMANIO_CUADRADO), (ANCHO_TABLERO * TAMANIO_CUADRADO, y * TAMANIO_CUADRADO))

# Verifica si la pieza se puede mover
def puede_mover_pieza(pieza, dx, dy):
    """Verifica si la pieza se puede mover en la dirección especificada."""
    for fila, columna in formas[pieza['tipo']][pieza['rotacion']]:
        x = pieza['x'] + fila + dx
        y = pieza['y'] + columna + dy
        if 0 <= x < ANCHO_TABLERO and 0 <= y < ALTO_TABLERO:
            if tablero[y][x] == 1:
                return False
        else:
            return False
    return True

# Mueve la pieza
def mover_pieza(pieza, dx, dy):
    """Mueve la pieza en la dirección especificada."""
    if puede_mover_pieza(pieza, dx, dy):
        pieza['x'] += dx
        pieza['y'] += dy

# Rota la pieza
def rotar_pieza(pieza):
    """Rota la pieza actual."""
    nueva_rotacion = (pieza['rotacion'] + 1) % len(formas[pieza['tipo']])
    if puede_mover_pieza(pieza, 0, 0, nueva_rotacion):
        pieza['rotacion'] = nueva_rotacion

# Verifica si la pieza toca el fondo
def toca_fondo(pieza):
    """Verifica si la pieza toca el fondo del tablero."""
    for fila, columna in formas[pieza['tipo']][pieza['rotacion']]:
        y = pieza['y'] + columna + 1
        if y >= ALTO_TABLERO:
            return True
    return False

# Fija la pieza en el tablero
def fijar_pieza(pieza):
    """Fija la pieza actual en el tablero."""
    for fila, columna in formas[pieza['tipo']][pieza['rotacion']]:
        x = pieza['x'] + fila
        y = pieza['y'] + columna
        tablero[y][x] = 1

# Verifica si hay lineas completas
def verificar_lineas_completas():
    """Verifica si hay lineas completas en el tablero y las elimina."""
    lineas_completas = 0
    for fila in range(ALTO_TABLERO):
        if all(tablero[fila][columna] == 1 for columna in range(ANCHO_TABLERO)):
            tablero.pop(fila)
            tablero.insert(0, [0 for _ in range(ANCHO_TABLERO)])
            lineas_completas += 1
    return lineas_completas

# Dibuja el puntaje
def dibujar_puntaje(puntaje):
    """Dibuja el puntaje actual en la pantalla."""
    texto_puntaje = fuente.render("Puntaje: {}".format(puntaje), True, COLOR_LINEA)
    pantalla.blit(texto_puntaje, (10, 10))

# Main loop del juego
def main():
    """Ejecuta el juego."""
    pieza_actual = crear_pieza()
    puntaje = 0

    # Bucle del juego
    en_ejecucion = True
    while en_ejecucion:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                en_ejecucion = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    mover_pieza(pieza_actual, -1, 0)
                elif evento.key == pygame.K_RIGHT:
                    mover_pieza(pieza_actual, 1, 0)
                elif evento.key == pygame.K_DOWN:
                    mover_pieza(pieza_actual, 0, 1)
                elif evento.key == pygame.K_UP:
                    rotar_pieza(pieza_actual)

        # Mueve la pieza hacia abajo
        if puede_mover_pieza(pieza_actual, 0, 1):
            mover_pieza(pieza_actual, 0, 1)
        else:
            # Fija la pieza en el tablero
            fijar_pieza(pieza_actual)
            # Verifica las lineas completas
            lineas_completas = verificar_lineas_completas()
            # Actualiza el puntaje
            puntaje += lineas_completas * 100
            # Crea una nueva pieza
            pieza_actual = crear_pieza()

        # Dibuja la pantalla
        pantalla.fill(COLOR_FONDO)
        dibujar_tablero()
        dibujar_pieza(pieza_actual)
        dibujar_puntaje(puntaje)
        pygame.display.flip()

        # Ajusta la velocidad del juego
        pygame.time.delay(300)

    # Finaliza Pygame
    pygame.quit()

# Ejecuta el juego
if __name__ == "__main__":
    main()