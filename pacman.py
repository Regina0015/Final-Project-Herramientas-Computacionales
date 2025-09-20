import pygame
import sys

def pantalla_inicio():
    # Inicializar Pygame
    pygame.init()

    # Pantalla principal
    ANCHO, ALTO = 600, 400
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Pac-Man - Pantalla de Inicio")

    NEGRO = (0, 0, 0)
    AMARILLO = (255, 255, 0)
    BLANCO = (255, 255, 255)

    titulo_fuente = pygame.font.SysFont("comicsansms", 60, bold=True)
    boton_fuente = pygame.font.SysFont("arial", 30, bold=True)

    titulo = titulo_fuente.render("PAC-MAN", True, AMARILLO)
    instrucciones = boton_fuente.render("Presiona ESPACIO para jugar", True, BLANCO)
    #Imágenes en este caso pacman para ser mas visual
    pacman_radio = 40
    pacman_pos = (ANCHO // 2, ALTO // 2 + 10)

    clock = pygame.time.Clock()

    def dibujar_pacman(pos):
        """Dibuja un Pac-Man simple."""
        x, y = pos
        pygame.draw.circle(pantalla, AMARILLO, (x, y), pacman_radio)
        pygame.draw.polygon(pantalla, NEGRO, [
            (x, y),
            (x + pacman_radio, y - pacman_radio // 2),
            (x + pacman_radio, y + pacman_radio // 2)
        ])

    # Loop de la pantalla de inicio
    while True:
        pantalla.fill(NEGRO)
        
        #Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return

        pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 40))
        dibujar_pacman(pacman_pos)
        pantalla.blit(instrucciones, (ANCHO // 2 - instrucciones.get_width() // 2, ALTO - 70))

        pygame.display.flip()
        clock.tick(30)

# Empezar con la pantalla
pantalla_inicio()
#Juego orginal de pacman a modificar

from random import choice
from turtle import *
from freegames import floor, vector

state = {'score': 0}
path = Turtle(visible=False)
writer = Turtle(visible=False)
aim = vector(10, 0)
pacman = vector(-40, -80)
ghosts = [
    [vector(-180, 160), vector(10, 0)],
    [vector(-180, -160), vector(0, 10)],
    [vector(100, 160), vector(0, -10)],
    [vector(100, -160), vector(-10, 0)],
    # Fantasmas extra
    [vector(0, 160), vector(10, 0)],
    [vector(0, -160), vector(0, 10)],
    [vector(-100, 80), vector(0, -10)],
    [vector(120, -80), vector(-10, 0)],
]


lives = {'n': 3}

def reset_round():
    """Reinicia posiciones de Pac-Man y fantasmas sin borrar score ni pellets."""
    global pacman, aim, ghosts
    pacman = vector(-40, -80)
    aim = vector(10, 0)
    ghosts[:] = [
        [vector(-180, 160), vector(10, 0)],
        [vector(-180, -160), vector(0, 10)],
        [vector(100, 160), vector(0, -10)],
        [vector(100, -160), vector(-10, 0)],
        [vector(0, 160), vector(10, 0)],
        [vector(0, -160), vector(0, 10)],
        [vector(-100, 80), vector(0, -10)],
        [vector(120, -80), vector(-10, 0)],
    ]

def draw_hud():
    """Dibuja HUD: Vidas con corazones (o puntos rojos si no hay soporte)."""
    up()
    goto(-200, 160)
    color('white')
    try:
        write(f"Vidas: {'❤' * lives['n']}", font=("Arial", 12, "normal"))
    except:
        write("Vidas:", font=("Arial", 12, "normal"))
        x0, y0 = -140, 168
        for i in range(lives['n']):
            up(); goto(x0 + i * 14, y0); dot(10, 'red')

# fmt: off
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]
# fmt: on

def square(x, y):
    """Draw square using path at (x, y)."""
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()
    for count in range(4):
        path.forward(20)
        path.left(90)
    path.end_fill()

def offset(point):
    """Return offset of point in tiles."""
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index

def valid(point):
    """Return True if point is valid in tiles."""
    index = offset(point)
    if tiles[index] == 0:
        return False
    index = offset(point + 19)
    if tiles[index] == 0:
        return False
    return point.x % 20 == 0 or point.y % 20 == 0

def world():
    """Draw world using path."""
    bgcolor('black')
    path.color('blue')
    for index in range(len(tiles)):
        tile = tiles[index]
        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)
            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')

def move():
    """Move pacman and all ghosts."""
    writer.undo()
    writer.write(state['score'])
    clear()


    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman)


    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)


    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')


    for point, course in ghosts:
        if valid(point + course):
            point.move(course)
        else:
            options = [vector(10, 0), vector(-10, 0), vector(0, 10), vector(0, -10)]
            plan = choice(options)
            course.x = plan.x
            course.y = plan.y

        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')


    draw_hud()
    update()


    for point, course in ghosts:
        if abs(pacman - point) < 20:
            lives['n'] -= 1
            if lives['n'] > 0:
                reset_round()
                ontimer(move, 400)
                return
            else:
                up(); goto(0, 0); color('red')
                write("GAME OVER", align="center", font=("Arial", 18, "bold"))
                update()
                return

    ontimer(move, 80)

def change(x, y):
    """Change pacman aim if valid."""
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y


setup(420, 420, 370, 0)
hideturtle()
tracer(False)
writer.up()
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])
listen()
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')
world()
move()
done()

