
import mini_engine_1 as m

HEIGHT=100
WIDTH=100
PIXEL_SIZE=5

class Creature():
    def __init__(self,pos,image):
        self.sprite = m.import_png(image,pos) #retourne {'sprite':[[0,0],[0,0]],'mask':[[True,True],[True,True]],'x':0,'y':0}
        self.vitesse = 5

    def bouge_haut(self):
        m.move_game_object(self.sprite,0,self.vitesse)
    
    def bouge_bas(self):
        m.move_game_object(self.sprite,0,-self.vitesse)

    def bouge_gauche(self):
        m.move_game_object(self.sprite,-self.vitesse,0)

    def bouge_droite(self):
        m.move_game_object(self.sprite,self.vitesse,0)
    
    
class Fantome(Creature):
    def __init__(self,pos):
        self.direction = False
        super().__init__(pos,"poulpe.png")
    
class Laser(Creature):
    def __init__(self,pos):
        super().__init__(pos,"laser.png")

class Tireur(Creature):
    def __init__(self, pos):
        super().__init__(pos, "navion.png")
        self.vitesse = 3
    
    #on surcharge les méthodes de la mère pour mettre des limites au joueur

    def bouge_haut(self):
        if not self.sprite['y']+self.vitesse+len(self.sprite['sprite'])>HEIGHT:
            m.move_game_object(self.sprite,0,self.vitesse)
    
    def bouge_bas(self):
        if not self.sprite['y']+self.vitesse<0:
            m.move_game_object(self.sprite,0,-self.vitesse)

    def bouge_gauche(self):
        if not self.sprite['x']+self.vitesse<0 :
            m.move_game_object(self.sprite,-self.vitesse,0)

    def tirer(self,scene):
        scene.append(Laser((self.sprite['x'] + len(self.sprite['mask'][0])//2,self.sprite['y'] + len(self.sprite['mask']))))
        # crée un un objet Laser au centre-haut du sprite

class Explosion():
    
    def __init__(self,pos):
       self.sprite = m.import_png("explosion.png",pos)

class Game_over():
    def __init__(self):
       self.sprite = m.import_png("game_over.png",(0,0)) #retourne {'sprite':[[0,0],[0,0]],'mask':[[True,True],[True,True]],'x':0,'y':0}
       m.move_game_object(self.sprite,WIDTH//2-(len(self.sprite['mask'][0])//2),HEIGHT//2-(len(self.sprite['mask'])//2)) 
       # bouge au centre de l'écran



def key_events_logic(scene):
    """Récupère les caractères saisie et modifie les coordonnées d'un
    game_object
    Args:
        scene: la liste des game_object du jeu
    """
    key = m.mr.get_key_event()
    if key != '':
        go = scene[0]
        
        if key == 'd':
            go.bouge_droite()
        elif key == 'z':
            go.bouge_haut()
        elif key == 'q':
            go.bouge_gauche()
        elif key == 's':
            go.bouge_bas()
        elif key == ' ':
            go.tirer(scene)

def clear_old_explosions(scene):
    """on supprime toutes les explosions de la scene,  
    elles n'auront eu le temps d'exister que 1 tour de boucle
        Args:
            scene:liste de go"""
    del_list = []
    for go in scene:
        if type(go) == Explosion:
            del_list.append(go)
    for go in del_list:
        scene.remove(go)
    
def colliding_objects(scene):
    """on teste les collisions entre les objets de la scene
        (sauf pour un laser et un tireur),
        on supprime ceux qui se touchent,
        et on fait apparaitre une explosion à l'endroit des
        go supprimés (sauf pour le laser)
        Args:
            scene:liste de go
    """
    del_list = []
    for go in scene:
        for go1 in scene:
            if not go == go1 : # si ils ne sont pas les memes
                if not ((type(go) == Tireur and type(go1) == Laser) or (type(go) == Laser and type(go1) == Tireur)):
                    #si ils ne sont pas un tireur et un laser
                    if test_collision((go.sprite['x'],go.sprite['y']),go.sprite['mask'],\
                        (go1.sprite['x'],go1.sprite['y']),go1.sprite['mask']):
                        # test de collsion entre les 2

                        del_list.append(go)

    for go in del_list:
        if go in scene:
            scene.remove(go)
            #on les supprime de la scene
            if not type(go) == Laser:
                scene.append(Explosion((go.sprite['x'] + len(go.sprite['mask'][0])//2,\
                    go.sprite['y'] + len(go.sprite['mask']))))
                #et on fait apparaitre une explosion à la place de chaque go
                # sauf si c'est un laser

def fantome_logic(go):
    """
    Mouvement que suivent les fantomes : si il touche les bords de l'écran,
    il change de direction et descend d'un rang
                                    sinon il va sur le coté
    Args:
        go:game object du fantome
    """
    if go.sprite['x'] < 1 or go.sprite['x'] + len(go.sprite['mask'][0]) + go.vitesse >= WIDTH :
            # si il dépasse les limites
            go.direction = not go.direction
            #il change de direction horizontale
            go.bouge_bas()
            #et il va en bas

    if go.direction:
        go.bouge_droite()
    else:
        go.bouge_gauche()

def laser_logic(go,del_list):
    """Mouvement que suivent les lasers:
    si il ne dépasse pas les limites, il va en haut
    sinon on le supprime
    Args:
        go: game object du laser
        del_list: liste des game object à supprimer"""
    
    if go.sprite['y'] + len(go.sprite['mask'])+ go.vitesse< HEIGHT:
        #si il ne dépasse pas les limites
        go.bouge_haut()
        #il va vers le haut
    else:
        del_list.append(go)
        #sinon on le supprime

def objects_logic(scene):
    """Appelle fantome_logic et laser_logic et supprime les game object
    de la scene que ces fonctions suppriment
    Args:
        scene: liste des game objects"""
    del_list = []
    for go in scene[1:]:

        if type(go) == Fantome:
            fantome_logic(go)

        elif type(go) == Laser:
            laser_logic(go,del_list)

    for go in del_list:
        if go in scene:
            scene.remove(go)
            #on efface les lasers qui sortent des limites

def spawn_logic(scene,seuil):
    """
    Vérifie si le nb de Fantomes est inférieur au seuil,
    si oui vérifie si les coordonnées de spawn sont libres,
    si oui fait apparaitre un fantome en haut à gauche
    Args:
        scene:liste de go de la scene
        seuil:seuil de fantomes en desous duquel le spawn est possible
    """
    spawn = False
    if list(type(go)==Fantome for go in scene).count(True) < seuil:
        #si le nb de fantomes < seuil
        spawn = True
        #on active le spawn
        for go in scene:
            if type(go) == Fantome:
                if go.sprite['y'] >= 80:
                    spawn = False
                    # sauf si il y a un fantome au meme rang que le spawn
    if spawn:
        scene.append(Fantome((0,90)))
        #on cree un fantome au spawn

def game_logic(scene):
    """
    Regroupe toutes les fonctions de logique du jeu
    et retourne vrai si le joueur est mort
    Args:
        scene:liste des go
    Return:
        True: si le joueur est mort
        None:sinon
    """

    if not type(scene[0]) == Tireur:
        #si le joueur est mort
        return True

    key_events_logic(scene)
    clear_old_explosions(scene)
    colliding_objects(scene)
    objects_logic(scene)
    spawn_logic(scene,2)

def test_collision(pos,mask,pos1,mask1):
    """test de collision de 2 rectangles par leurs coordonnées
    retourne True si collision, false sinon
    explication détaillée : https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.geeksforgeeks.org%2Ffind-two-rectangles-overlap%2F&psig=AOvVaw2I33VllF3fsmhydJJrwxTn&ust=1639426748875000&source=images&cd=vfe&ved=0CAwQjhxqFwoTCKCIk9-K3_QCFQAAAAAdAAAAABAR
    Args:
        pos,pos1:coordonnées du point bas-gauche des rectangles
        mask,mask1:masques fesant la taille des rectangles
    Return:
        True:si les 2 rectangles se touchent
        False: sinon
"""
    x,y = pos
    x1,y1 = x + len(mask[0]), y + len(mask)
    a,b = pos1
    a1,b1 = a + len(mask1[0]), b + len(mask1)

    
    if(y1<b or x1<a):
        return False

    elif(x>a1 or y>b1):
        return False
    else:
        return True



 
def game_loop(scene, background_color, n):
    """
    Répète n fois:
        Dessine la scene.
        Efface la scène.
        Change les coordonnées des game_object (ai_xxx_move_game_object).
    
    Sauf si game_logic retourne vrai:
        on affiche Game_over et on arrete la boucle
    Args:
        n: le nombre de tour du moteur de jeu
    """
    for _ in range(n):

        m.draw_scene(scene)
        m.sleep(0.01)
        m.clear_scene(scene,background_color)
        if game_logic(scene):
            #si le joueur est mort
            scene = []
            scene.append(Game_over())
            m.draw_scene(scene)
            #on affiche le game over
            return
            #et on arrete la gameloop

    


def main():
    """Initialise les variables du mini_render,
    fait spawner le joueur et un fantome
    et commence le game_loop
    """
    
    background_color =(0,0,0)
    m.mr.init(HEIGHT,WIDTH,PIXEL_SIZE)
    
    m.mr.set_speed(20)
    m.mr.set_title('Space Invaders oué')
    m.mr.set_background(background_color)
    t = Tireur((50,0))
    scene = [t]
    scene.append(Fantome((0,80)))
    n = 1000
    game_loop(scene, background_color, n)

    m.mr.end()

if __name__ == '__main__':
    main()
