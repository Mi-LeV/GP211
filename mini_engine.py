import mini_render as mr
from random import randint
from time import sleep

SIZE = 100

def horizontal_line(x,y,size,color):
    for i in range(size):
        mr.pixel(x+i,y,color)

def draw_sprite(l,m,x,y):
    for i in range(len(l)):
        for j in range(len(l[i])):
            if m[i][j]:
                mr.pixel(x + i ,y + j , l[i][j])

def draw_game_object(g_o):
    draw_sprite(g_o['sprite'],g_o['mask'],g_o['x'],g_o['y'])

def erase_game_objet(g_o):
    draw_sprite(g_o['erase'],g_o['mask'],g_o['x'],g_o['y'])

def draw_scene(scene):
    for go in scene:
        draw_game_object(go)

def erase_scene(scene):
    for go in scene:
        erase_game_objet(go)

def move_game_object(g_o ,x, y):
    g_o['x'] = x
    g_o['y'] = y

def move_scene(scene):
   for go in scene:
        ai_random_move(go)

def ai_random_move(g_o):
    x,y = randint(-1,1),randint(-1,1)
    if g_o['x']+x < 0 or g_o['x']+x+len(g_o['sprite']) > SIZE:
        x = 1
    if g_o['y']+y < 0 or g_o['y']+y+len(g_o['sprite'][0]) > SIZE:
        y = 1
    move_game_object(g_o,x,y)

def game_loop(scene,b_c,n):
    mr.set_background(b_c)
    for i in range(n):
        scene[0]['x'],scene[0]['y'] = 0,0
        for i in range(100):
            draw_scene(scene)
            sleep(0.1)
            erase_scene(scene)
            move_scene(scene)