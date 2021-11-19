import mini_engine as me
import mini_render as mr

from PIL import Image

im = Image.open('sprite.jfif')
width, height = im.size
pix = im.load()

rgb = []
a = []
b = []
for i in range(width):
    temp = []
    temp1 = []
    temp2  = []
    for j in range(height):
        temp.append(tuple(map(lambda x:x/256,pix[i,-j][0:3])))
        temp1.append(bool(pix[i,-j][3]))
        temp2.append((0,0,0))
    rgb.append(temp)
    a.append(temp1)
    b.append(temp2)


go1 = {'sprite':rgb,\
    'mask':a,'erase' : b, 'x':50, 'y':50}

scene = [go1]
SIZE = 100

def main():
    mr.init(SIZE, SIZE, 5)
    mr.set_speed(1)
    me.game_loop(scene,(0,0,0),70000000000)
    mr.end()

main()