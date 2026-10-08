import pygame
from math import cos, sin, pi
from numpy import matrix
from time import sleep
from random import randint
from script import *
import pyglet

WHITE = (255, 255, 255)
WIDTH = 800
HEIGHT = 800

lista_figuri = []

class Figure:
    nr_figuri = 0
    def __init__(self,rap,WIDTH,HEIGHT):

        self.main = 0
        self.block_size = WIDTH * 0.02
        self.rap = rap
        self.x_point = WIDTH * 0.1 // rap
        self.y_point = HEIGHT * 0.2 // rap
        self.z_point = WIDTH * 0.1 // rap
        self.culori = (randint(0,255),randint(0,255),randint(0,255))
        self.small_points = []
        self.shadow_points = []

        self.points = (
            (self.x_point, self.y_point, self.z_point),
            (-self.x_point, self.y_point, self.z_point),
            (self.x_point, -self.y_point, self.z_point),
            (self.x_point, self.y_point, -self.z_point),
            (-self.x_point, self.y_point, -self.z_point),
            (self.x_point, -self.y_point, -self.z_point),
            (-self.x_point, -self.y_point, -self.z_point),
            (-self.x_point, -self.y_point, self.z_point),
        )

        Figure.nr_figuri += 1
        lista_figuri.append(self)

    def make_small_points(self):
        for i in self.points:
            lista = []
            for j in i:
                if j < 0:
                    lista.append(j + abs(j // 2))
                else:
                    lista.append(j - abs(j // 2))
            self.small_points.append(tuple(lista))
        self.small_points = tuple(self.small_points)

    def make_shadow(self):
        self.shadow_points = []
        for i in self.points:
            list = []
            for x,y,z in i:
                list.append(x)
                list.append(y)
                list.append(0)
            self.shadow_points.append(tuple(list))
        self.shadow_points = tuple(self.shadow_points)

    def get_points_matrix(self):
        return self.points,self.small_points

p1 = Figure(1,1200,1200)
p1.main = 1
#p1.make_small_points()

p2 = Figure(1,500,250)
#p2.make_small_points()

pygame.init()
display = pygame.display
surface = display.set_mode((WIDTH, HEIGHT))
display.set_caption("3D TETRIS")

points_offsets = [0,0,0]

done = False

RED = (255,0,0)

key_pressed = pygame.key.get_pressed()

rotation = [0, 0, 0]

idle_window_key_up = 1
idle_window_key_down = 0

def generate_x(theta):
    return matrix([
        [1, 0, 0],
        [0, cos(theta), -sin(theta)],
        [0, sin(theta), cos(theta)]
    ])
def generate_y(theta):
    return matrix([
        [cos(theta), 0, -sin(theta)],
        [0, 1, 0],
        [sin(theta), 0, cos(theta)]
    ])
def generate_z(theta):
    return matrix([
        [cos(theta), -sin(theta), 0],
        [sin(theta), cos(theta), 0],
        [0, 0, 1]
    ])

def render_block(matrice,culori):

    if matrice == None:
        return

    render_edges = [(0,1),(0,2),(0,3),(1,7),(1,4),(3,4),(3,5),(4,6),(5,6),(5,2),(2,7),(7,6)]

    r,g,b = culori
    global points_offsets
    render_points = []
    render_shadow_points = []
    for p in matrice:

        m = matrix([
            [p[0]],
            [p[1]],
            [p[2]]
        ])

        for method, angle in zip((generate_x, generate_y, generate_z), rotation):
            m = method(angle) * m

        x, y, z = map(lambda x: int(WIDTH / 2 - x), (m[0, 0], m[1, 0], m[2, 0]))
        shadow_x = x
        render_points.append((x, y))
        render_shadow_points.append((shadow_x,y+z//4))

    print(render_edges)
    for i,j in render_edges:
        pygame.draw.line(surface,culori, render_points[i], render_points[j])
        #if p.main != 0:
            #pygame.draw.line(surface,(255,255,255),render_shadow_points[i],render_shadow_points[j])

def render_shadow_projection(p):
    shadow = Figure(p.rap,p.x_point,0)
    return shadow

def main():
    global done
    global idle_window_key_up
    global idle_window_key_down
    global idle_window
    global key_pressed
    global render_points
    global render_points_small
    global rotation

    while not done:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                done = True
                break
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_i:
                    temp = idle_window_key_up
                    idle_window_key_up = idle_window_key_down
                    idle_window_key_down = temp


        if pygame.mouse.get_focused():
            if idle_window_key_down:
                if pygame.key.get_pressed()[pygame.K_DOWN]:
                    rotation[0] -= pi / randint(100, 400)
                if pygame.key.get_pressed()[pygame.K_UP]:
                    rotation[0] += pi / randint(100, 400)
                if pygame.key.get_pressed()[pygame.K_RIGHT]:
                    rotation[1] += pi / randint(100, 400)
                if pygame.key.get_pressed()[pygame.K_LEFT]:
                    rotation[1] -= pi / randint(100, 400)

            else:
                rotation[0] += pi / randint(100, 400)
                rotation[1] += pi / randint(100, 400)
            if pygame.key.get_pressed()[pygame.K_q]:
                done = True
                break

        pygame.draw.rect(surface, (1, 1, 1), pygame.Rect(0, 0, WIDTH, HEIGHT))
        pygame.draw.rect(surface,(1,0,0),pygame.Rect(0,0,WIDTH,HEIGHT))
        render_points = []
        render_points_small = []

        for p in lista_figuri:
            render_block(p.points,p.culori)
            #render_block(p.points,(255,0,0))
            if type(p.small_points)!=list:
                render_block(p.small_points,p.culori)


        display.flip()
        sleep(1/100)


def play_music():
    music = pyglet.media.load("muzica_cool_trimmed.wav")
    player = pyglet.media.Player()
    player.loop = True
    player.queue(music)
    player.play()
    pyglet.app.run()

thread = threading.Thread(target=play_music,daemon = True)
thread.start()

main()