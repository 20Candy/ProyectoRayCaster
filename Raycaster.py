import pygame
from math import *

#COLORS__________________________________________________________________________
RED = (255,0,0)
WHITE = (255,255,255)
TRANSPARENT = (152,0,136,255)

#WALLS___________________________________________________________________________
walls = {
    '1': pygame.image.load('./pared/pared1.png'),
    '2': pygame.image.load('./pared/pared2.png'),
    '3': pygame.image.load('./pared/pared3.png'),
}

#ENEMIES_________________________________________________________________________
sprite1= pygame.image.load('./sprite/sprite1.png')
sprite2= pygame.image.load('./sprite/sprite2.png')
sprite3= pygame.image.load('./sprite/sprite3.png')
sprite4= pygame.image.load('./sprite/sprite4.png')

enemies = [
    {
        'x':100,
        'y':100,
        'sprite': sprite1,
    }
]

#JUGADOR_________________________________________________________________________
varita = pygame.image.load('./personaje/varita.png')
ins = pygame.image.load('./instrucciones/ins.png')

#RAYCASTER_______________________________________________________________________
class Raycaster(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height= screen.get_rect()

        self.minimap = 100
        
        self.blocksize = 50
        self.map = []
        self.player = {
            'x': int(self.blocksize + self.blocksize / 2),
            'y': int(self.blocksize + self.blocksize / 2),
            'fov': int(pi/3),
            'a': int(pi/3),
        }
        self.clearZ()

    #CLEAR ZBUFFER________________________________________________________________
    def clearZ(self):
        self.zbuffer = [9999 for z in range(0,self.width)]

    #DRAW POINT ON SCREEN_________________________________________________________
    def point(self, x, y, c=WHITE):
        self.screen.set_at((x,y),c)

    #DRAW BLOCK FROM MAP__________________________________________________________
    def block(self, x,y, wall):
        for i in range(x,x + 10):
            for j in range(y,y + 10):
                tx = int((i - x) * 128 /10)
                ty = int((j - y) * 128 / 10)
                c = wall.get_at((tx,ty))
                self.point(i,j,c)

    #LOAD MAP______________________________________________________________________
    def load_map(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))

    def draw_stake(self,x,h,c,tx):
        start_y = int(self.height/2 - h/2)
        end_y = int(self.height/2 + h/2)
        height = end_y - start_y

        for y in range(start_y,end_y):
            ty = int((y-start_y) * 128 / height)
            color = walls[c].get_at((tx,ty))
            self.point(x,y,color)

    #DRAW RAY_____________________________________________________________________
    def cast_ray(self, a):
        d = 0
        ox = self.player['x']
        oy = self.player['y']
        
        while True:
            x = int(ox + d * cos(a))
            y = int(oy + d * sin(a))

            i = int(x / self.blocksize)
            j = int(y / self.blocksize)

            if self.map[j][i] != ' ':
                hitx = x -i*self.blocksize
                hity = y -j*self.blocksize

                if 1 < hitx < self.blocksize - 1:
                    maxhit = hitx
                else:
                    maxhit = hity

                tx = int(maxhit * 128 / self.blocksize)
                return d, self.map[j][i], tx

            self.point(int(x/5),int(y/5))
            d += 1
    
    #DRAW MAP_____________________________________________________________________
    def draw_map(self):
        size = 10
        for x in range(0,100,size):
            for y in range(0,100,size):
                i = int(x / size)
                j = int(y / size)
                
                if self.map[j][i] != ' ':
                    if self.map[j][i] != '\n':
                        self.block(x,y, walls[self.map[j][i]])

    #DRAW WEAPON_________________________________________________________________

    def draw_weapon(self, xi, yi, w = 250, h = 250):
        for x in range(xi, xi + w):
            for y in range(yi, yi + h):
                tx = int((x - xi) * 128/w)
                ty = int((y - yi) * 128/h)
                c = varita.get_at((tx, ty))
                if c != TRANSPARENT:
                    self.point(x,y,c)

    #DRAW PLAYER__________________________________________________________________
    def draw_player(self):
        try:
            self.point(int(self.player['x']/5),int(self.player['y']/5),RED)
            self.point((int(self.player['x']/5)+1),int(self.player['y']/5),RED)
            self.point(int(self.player['x']/5),(int(self.player['y']/5)+1),RED)
            self.point((int(self.player['x']/5)-1),(int(self.player['y']/5)),RED)
            self.point(int(self.player['x']/5),(int(self.player['y']/5)-1),RED)
        except:
            pass

    #DRAW SPRITE__________________________________________________________________
    def draw_sprite(self,sprite):
        sprite_x = sprite['x']
        sprite_y = sprite['y']
        sprite_sprite = sprite['sprite']
        
        sprite_a = atan2(sprite_y - self.player['y'], sprite_x - self.player['x'])
        sprite_d = ((self.player['x'] - sprite_x) ** 2 + (self.player['y'] - sprite_y) ** 2) ** .5
        sprite_size = int(self.height / sprite_d * 50)
        sprite_x = int(self.width / 2 + (sprite_a - self.player['a']) * self.width / self.player['fov'] * 50)
        sprite_y = int(self.height / 2 - sprite_size / 2)
        for x in range(sprite_size):
            for y in range(sprite_size):
                tx = int(x * 128 / sprite_size)
                ty = int(y * 128 / sprite_size)
                c = sprite_sprite.get_at((tx,ty))
                self.point(sprite_x + x, sprite_y + y, c)

    #DRAW INSRUCTIONS_____________________________________________________________
    def draw_Ins(self,xi,yi, w = 200, h = 350):
        for x in range(xi, xi + w):
            for y in range(yi, yi + h):
                tx = int((x - xi) * 128/w)
                ty = int((y - yi) * 128/h)
                c = ins.get_at((tx, ty))
                self.point(x,y,c)

    ############################################################################################################
    #RENDER_____________________________________________________________________________________________________
    def render(self):
        self.draw_map()
        self.draw_player()

        size = 500
        size2 = 100

        for i in range(0,int(size)):
            a = self.player['a'] - self.player['fov']/2 + self.player['fov'] * i/(size)
            d,c,tx = self.cast_ray(a)

            x = int(size2) + i
            h = self.height/(d * cos(a - self.player['a'])) * self.height /10

            if self.zbuffer[i] >= d:
                self.draw_stake(x,h,c,tx)
                self.zbuffer[i] = d

        self.draw_weapon(300,250)
        # self.draw_Ins(10,120)
       
        for sprite in enemies:
            self.draw_sprite(sprite)   

        