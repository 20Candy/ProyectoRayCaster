import pygame
from math import *
from pygame import mixer
from cast import *
from temas.temasPygame import *
import pygame_menu

#COLORES_______________________________________________________________________
BLACK = (0,0,0)
WHITE = (255,255,255)
SKY = (8,27,69)
GROUND = (4,28,4)
TRANSPARENT = (152,0,136,0)

def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()


#RUNNING GAME_____________________________________________________________________________________________
def running(screen, map, musica, nivel):
    r = Raycaster(screen)
    #cargar el mapar
    r.load_map(map)

    #cargar la musica del nivel
    mixer.music.stop()
    mixer.music.load(musica)
    mixer.music.play(-1)
    mixer.music.set_volume(0.3)

    #cargar efecto incial
    effect = mixer.Sound('./efectos/open.mp3')
    effect.set_volume(0.2)
    effect.play()
       
    clock = pygame.time.Clock()

    #inicializacion variable running
    running = True

    #posicion inicial del jugador
    x = r.player['x']
    y = r.player['y']
    a = r.player['a']

    #movimiento
    movement = 5
    first_time = True

    while running:
        #si es la primera vez que entra al nivel, mostrar pantalla negra por 2 segundos y luego continuar
        if first_time:
            screen.fill(BLACK)

            message = "Tienes 1 minuto para encontrar el cáliz"
            message = (pygame.font.SysFont("Helvetica", 40)).render(message, 10, pygame.Color("white"))
            screen.blit(message, (30,200))

            pygame.display.flip()
            pygame.time.wait(2000)
            first_time = False
            continue

        #fondo
        screen.fill(BLACK,(0,0,100,r.height))
        screen.fill(SKY,(100,0,900,r.height/2))
        screen.fill(GROUND, (100,r.height/2,900,r.height/2))

        try:
            r.render()
            r.clearZ()
        except:
            r.player['x'] = x
            r.player['y'] = y

        #contador de fps en pantalla
        fps = str("FPS: "+str(int(clock.get_fps())))
        fps = (pygame.font.SysFont("Helvetica", 20)).render(fps, 10, pygame.Color("red"))
        screen.blit(fps, (525,10))
       
        if pygame.time.get_ticks() < 60000:
            message = "Tiempo restante: " + str(60 - pygame.time.get_ticks()//1000)
            message = (pygame.font.SysFont("Helvetica", 20)).render(message, 10, pygame.Color("white"))
            screen.blit(message, (110,10))
        else:
            running = False

        #Verificar si el jugador a alzanado el caliz
        x = r.player['x']
        y = r.player['y']

        if(nivel == 1):
            if 420 <= x <= 440 and 420 <= y <= 440:
                running = False
        elif(nivel == 2):
            if 340 <= x <= 360 and 420 <= y <= 440:
                running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running= False

            keys = pygame.key.get_pressed()

            if event.type == pygame.MOUSEMOTION:
                r.player['a'] += event.rel[0]/200

            if keys[pygame.K_a]:
                r.player['a'] -= pi/10
            if keys[pygame.K_d]:
                r.player['a'] += pi/10

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                r.player['x'] += cos(r.player['a']) * movement
                r.player['y'] += sin(r.player['a']) * movement
                
                #sonido de pasos
                effect = mixer.Sound('./efectos/step.mp3')
                effect.set_volume(0.2)
                effect.play()  

            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                r.player['x'] -= cos(r.player['a']) * movement
                r.player['y'] -= sin(r.player['a']) * movement

                #sonido de pasos
                effect = mixer.Sound('./efectos/step.mp3')
                effect.set_volume(0.2)
                effect.play()   

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                r.player['x'] -= cos(r.player['a'] + pi/2) * movement
                r.player['y'] -= sin(r.player['a'] + pi/2) * movement
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                r.player['x'] += cos(r.player['a'] + pi/2) * movement
                r.player['y'] += sin(r.player['a'] + pi/2) * movement

        clock.tick(60)
        pygame.display.update()
    
    #al regresar poner musica de inicio de nuevo
    mixer.music.stop()
    mixer.music.load('./musica/harry.mp3')
    mixer.music.play(-1)
    mixer.music.set_volume(0.3)

    first_time = True


#INICIO________________________________________________________________________
pygame.init()
screen = pygame.display.set_mode((600,500))

#pantalla de menu
h = harry()
menu = pygame_menu.Menu('Harry Potter Maze', 600, 500, theme=h)
menu.add.button('El torneo de los 3 magos', running, screen ,'./niveles/map.txt', './musica/level1.mp3', 1)
menu.add.button('Un encuentro tenebroso', running, screen, './niveles/map2.txt', './musica/level2.mp3', 2)
menu.add.button('Cerrar', pygame_menu.events.EXIT)

#musica de patanlla de inicio
mixer.music.stop()
mixer.music.load('./musica/harry.mp3')
mixer.music.play(-1)
mixer.music.set_volume(0.3)

menu.mainloop(screen, fps_limit=60.0)