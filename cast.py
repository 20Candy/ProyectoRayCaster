import pygame
from math import *

#WALLS___________________________________________________________________________
walls = {
    '1': pygame.image.load('./pared/pared1.png'),
    '2': pygame.image.load('./pared/pared2.png'),
    '3': pygame.image.load('./pared/pared3.png'),
    '4': pygame.image.load('./pared/pared4.png'),
}

#JUGADOR_________________________________________________________________________
varita = pygame.image.load('./personaje/varita.png')
ins = pygame.image.load('./instrucciones/ins.png')

#RAYCASTER_______________________________________________________________________
class Raycaster(object):
    def __init__(self, screen):
        _, _, self.width, self.height= screen.get_rect()
        self.screen = screen
        self.blocksize = 50
        self.player = {
            'x': int(self.blocksize + self.blocksize / 2),
            'y': int(self.blocksize + self.blocksize / 2),
            'fov': int(pi/3),
            'a': int(pi/3),
        }
        self.map = []
        self.clearZ()

    #CLEAR ZBUFFER________________________________________________________________
    def clearZ(self):
        self.zbuffer = [9999 for z in range(0,self.width)]

    #CLEAR  
    def clear(self):
        for x in range(self.width):
            for y in range(self.height):
                r = int((x/self.width)*255) if x/self.width < 1 else 1
                g = int((y/self.height)*255) if y/self.height < 1 else 1
                b = 0
                color = (r, g, b)
                self.point(x, y, color)

    #DRAW POINT ON SCREEN_________________________________________________________
    def point(self, x, y, c=(255,255,255)):
        self.screen.set_at((x,y),c)

    #RECTANGLE___________________________________________________________________
    def draw_rectangle(self, x, y, texture):
        for cx in range(x, x + 50):
            for cy in range(y, y + 50):
                tx = int((cx - x)*128 / 50)
                ty = int((cy - y)*128 / 50)
                c = texture.get_at((tx, ty))
                self.point(cx, cy, c)

    #LOAD MAP______________________________________________________________________
    def load_map(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))


    #DRAW RAY_____________________________________________________________________
    def cast_ray(self, a):
        d = 0

        while True:
            x = self.player["x"] + d*cos(a)
            y = self.player["y"] + d*sin(a)

            i = int(x/50)
            j = int(y/50)
        
            if self.map[j][i] != ' ':
                hitx = x - i*50
                hity = y - j*50

                if 1 < hitx < 49:
                    maxhit = hitx
                else:
                    maxhit = hity

                tx = int(maxhit * 128 / 50)
                return d, self.map[j][i], tx

            self.point(int(x/5),int(y/5))  #cambio de escala
            d += 1

    #STAKE_______________________________________________________________________
    def draw_stake(self,x,h,texture,tx):
        start = int(self.height/2 - h/2)
        end = int(self.height/2 + h/2)

        for y in range(start,end):
            ty = int((y-start) * 128 / (end - start))
            color = walls[texture].get_at((tx,ty))
            self.point(x,y,color)

    #DRAW SPRITE__________________________________________________________________
    def draw_sprite(self,sprite):
        sprite_a = atan2(sprite["y"] - self.player["y"], sprite["x"] - self.player["x"])   # why atan2? https://stackoverflow.com/a/12011762

        sprite_d = ((self.player["x"] - sprite["x"])**2 + (self.player["y"] - sprite["y"])**2)**0.5
        sprite_size = (500/sprite_d) * 70

        sprite_x = 500 + (sprite_a - self.player["a"])*500/self.player["fov"] + 250 - sprite_size/2
        sprite_y = 250 - sprite_size/2

        sprite_x = int(sprite_x)
        sprite_y = int(sprite_y)
        sprite_size = int(sprite_size)

        for x in range(sprite_x, sprite_x + sprite_size):
            for y in range(sprite_y, sprite_y + sprite_size):
                if 500 < x < 1000 and self.zbuffer[x - 500] >= sprite_d:
                    tx = int((x - sprite_x) * 128/sprite_size)
                    ty = int((y - sprite_y) * 128/sprite_size)
                    c = sprite["texture"].get_at((tx, ty))
                    if c != (152, 0, 136, 255):
                        self.point(x, y, c)
                    self.zbuffer[x - 500] = sprite_d

    #DRAW BLOCK FROM MAP__________________________________________________________
    def block(self, x,y, wall):
        for i in range(x,x + 10):
            for j in range(y,y + 10):
                tx = int((i - x) * 128 /10)
                ty = int((j - y) * 128 / 10)
                c = wall.get_at((tx,ty))
                self.point(i,j,c)

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
                if c != (152,0,136,255):
                    self.point(x,y,c)

    #DRAW PLAYER__________________________________________________________________
    def draw_player(self):
        self.point(int(self.player['x']/5),int(self.player['y']/5))

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
        margen = 100

        for i in range(0,int(size)):
            a = self.player['a'] - self.player['fov']/2 + self.player['fov'] * i/(size)
            d,c,tx = self.cast_ray(a)

            x = int(margen) + i
            h = self.height/(d * cos(a - self.player['a'])) * self.height /10

            if self.zbuffer[i] >= d:
                self.draw_stake(x,h,c,tx)
                self.zbuffer[i] = d

        self.draw_weapon(300,250)
        #self.draw_Ins(10,120)
    