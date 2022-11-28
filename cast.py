import pygame
from math import *
import pygame_menu
from pygame import mixer
from Raycaster import *

#COLORES_______________________________________________________________________
BLACK = (0,0,0)
WHITE = (255,255,255)
SKY = (8,27,69)
GROUND = (4,28,4)
TRANSPARENT = (152,0,136,0)

#MUSICA________________________________________________________________________
def music(music, opt=0):
    if opt == 0:
        mixer.music.stop()
        mixer.music.load(music)
        mixer.music.play(-1)
        mixer.music.set_volume(0.3)
    else:
        effect = mixer.Sound(music)
        effect.set_volume(0.2)
        effect.play()

#FPS___________________________________________________________________________
def FPS():
    fps = str("FPS: "+str(int((pygame.time.Clock()).get_fps())))
    fps = (pygame.font.SysFont("Arial", 20)).render(fps, 10, pygame.Color("white"))
    return fps

############################################################################################################
#RUNNING GAME_____________________________________________________________________________________________
def running(screen, map, musica):
    r = Raycaster(screen)
    #cargar el mapar
    r.load_map(map)

    #cargar la musica
    music(musica)
    music('./efectos/open.mp3',1)        
    clock = pygame.time.Clock()

    #inicializacion variable running
    running = True

    #posicion inicial del jugador
    x = r.player['x']
    y = r.player['y']
    a = r.player['a']

    #movimiento
    movement = 5


    while running:
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

        x = r.player['x']
        y = r.player['y']

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
                music('./efectos/foot.mp3',1)        
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                r.player['x'] -= cos(r.player['a']) * movement
                r.player['y'] -= sin(r.player['a']) * movement
                music('./efectos/foot.mp3',1)        
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                r.player['x'] -= cos(r.player['a'] + pi/2) * movement
                r.player['y'] -= sin(r.player['a'] + pi/2) * movement
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                r.player['x'] += cos(r.player['a'] + pi/2) * movement
                r.player['y'] += sin(r.player['a'] + pi/2) * movement

        clock.tick(60)
        pygame.display.update()
    
    music('./musica/harry.mp3')

pygame.init()
screen = pygame.display.set_mode((600,500))

myimage = pygame_menu.baseimage.BaseImage(
    image_path = './imagenes/caliz.jpg',
    drawing_mode = pygame_menu.baseimage.IMAGE_MODE_FILL,
)

Theme = pygame_menu.themes.Theme
harry = Theme(background_color = myimage,
                title_background_color = (102, 0, 0),
                title_font = pygame_menu.font.FONT_NEVIS,
                title_font_color = (255, 255, 255),
                title_font_size = 67,
                cursor_selection_color = (224, 156, 9),
                selection_color = (224, 156, 9),
                widget_font = pygame_menu.font.FONT_NEVIS,
                widget_alignment = pygame_menu.locals.ALIGN_CENTER,
                widget_font_color=(255, 255, 255),
                widget_background_color=(102, 0, 0),
                widget_padding = (10,20),
                widget_margin = (0,20))

                
menu = pygame_menu.Menu('Harry Potter Maze', 600, 500, theme=harry)

menu.add.button('Nivel 1', running, screen ,'./niveles/map.txt', './musica/level1.mp3')
menu.add.button('Nivel 2', running, screen, './niveles/map2.txt', './musica/level2.mp3')
menu.add.button('Cerrar', pygame_menu.events.EXIT)

music('./musica/harry.mp3')
menu.mainloop(screen, fps_limit=60.0)