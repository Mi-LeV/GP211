from time import sleep
import mini_render as mr
from PIL import Image



#Fonctions:

def import_png(image_file,pos):
    """ouvre une image dans le cwd et la transforme
        en sprite, masque et position dans un dictionnaire qu'elle retourne
        Args:
            image_file:chemin relatif de l'image à ouvrir
            pos: tuple de coordonnées du go
        Return: 
            go:dictionnaire formé du sprite, mask, x, y
        """
    im = Image.open(image_file)
    im = im.convert('RGBA') # conversion to RGBA
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
            temp.append(tuple(map(lambda x:x/256,pix[i,j][0:3])))
            temp1.append(bool(pix[i,j][3]))
        rgb.append(temp)
        a.append(temp1)


    return {'sprite':rgb,\
    'mask':a,'x':pos[0], 'y':pos[1]}

def draw_sprite(sprite, x, y,mask):
    """affiche une liste de pixels de couleur à la position (x,y)
        et en tenant compte du masque
        Args:
            sprite: liste de liste de couleur
            x,y:coordonnées
            mask:masque de transparence"""
    for i in range(len(sprite)):
        for j in range (len(sprite[0])):
            if mask[i][j]:
                mr.pixel(x+j,y+i,sprite[i][j])


def draw_game_object(go):
    """Dessine le sprite de l'objet.
    Args:
        go: Le game_object dont il faut afficher le sprite"""
    draw_sprite(go.sprite['sprite'],go.sprite['x'],go.sprite['y'],go.sprite['mask'])

def draw_scene(scene):
    """
    Dessine les game_object contenus dans la liste de game_object scene.
    Args:
        scene: La liste de game_object.
    """
    for i in scene:
        draw_game_object(i)

def clear_scene(scene,color):
    """
    Efface les game_object contenus dans la liste de game_object scene avec la
    couleur color.
    Args:
        scene: La liste de game_object.
        color: La couleur pour effacer la scene (la couleur de fond).
    """
    for i in scene:
        erase_game_object(i,color)

def erase_game_object(go,color):
    """
    Efface le game_object go avec la couleur color.
    
    Args:
        go: Le game_object à déplacer.
        color: la couleur pour effacer
    """
    #s_temp : sprite temporel    
    s_temp = [[color]*len(go.sprite['sprite'][0])]*len(go.sprite['sprite'])
    
    draw_sprite(s_temp,go.sprite['x'],go.sprite['y'],go.sprite['mask'])

def move_game_object(go, x, y):
    """
    Donne aux valeurs associées aux clés x et y du dictionnaire sprite du go les
    valeurs des argument x et y.
    Args:
        go: Le game_object à déplacer.
        x: La nouvelle abscisse.
        y: La nouvelle ordonnée.
    """
    go['x']+=x
    go['y']+=y



