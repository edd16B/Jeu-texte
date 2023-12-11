#🗺️
import curses #Documentation : https://docs.python.org/fr/3/howto/curses.html
import time
import random
import sys
sys.setrecursionlimit(1000000) #Augmentation de la limite de récursivité des fonctions

stdscr = curses.initscr()
#Définition des paires de couleurs pour l'affichage
curses.start_color() #Pour mettre de la couleur
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN) #Pour le perso
curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_CYAN) #Pour les objects
curses.init_pair(3, curses.COLOR_RED, curses.COLOR_CYAN) #Pour les monstres
curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_CYAN) #Pour les blocks
curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLUE) #Pour la sortie quand elle est visible
curses.noecho()
stdscr.timeout(1) #Temps d'attente pour les opérations de saisie [getkey()]
"""Variable test utilisé au début du projet
game_map = [[0,0,0,1,1],[0,0,0,0,1],[1,1,0,0,0],[0,0,0,0,0]]
dico ={0:' ',1:'█'}
"""


"""Fonctions de génération et de vérification d'accessibilité de la carte"""

def generate_random_game_map(size_map,proportion_wall): #Comme demandé 4.1
    game_map=[[0]*size_map[0] for i in range (size_map[1])]
    nombre_de_mur_total=round(proportion_wall*size_map[0]*size_map[1])
    game_map[random.randint(0,len(game_map)-1)][random.randint(0,len(game_map[0])-1)]=2 #Entrée
    game_map[random.randint(0,len(game_map)-1)][random.randint(0,len(game_map[0])-1)]=3 #Sortie
    nombre_de_mur=0
    while nombre_de_mur<nombre_de_mur_total:
        i=random.randint(0,len(game_map)-1)
        j=random.randint(0,len(game_map[0])-1)
        if game_map[i][j]==0:
            game_map[i][j]=1
            nombre_de_mur+=1
    return game_map

    #Ici, ce que je cherche à faire c'est impléménter des fonctions qui vont me permettre de vérifier si une carte est accessible ou non.

def visit(game_map,i,j,visited): #cette fonction se charge de parcourir la map à partir d'un cordonnée i,j tout en marquant true dans la matrice mirroir visited pour chaque case vide parcouru
    if (0<=i<=len(game_map)-1) and (0<=j<=len(game_map[0])-1) and not visited[i][j] :
        if game_map[i][j] != 1:
            visited[i][j]=True
            if (0<=i+1<=len(game_map)-1):visit(game_map,i+1,j,visited)
            if (0<=i-1<=len(game_map)-1):visit(game_map,i-1,j,visited)
            if (0<=j+1<=len(game_map[0])-1):visit(game_map,i,j+1,visited)
            if (0<=j-1<=len(game_map[0])-1):visit(game_map,i,j-1,visited)

def is_accessible(game_map): #Fonction qui vérifie si toutes les cases vides de ma map sont accessibles
    visited = [[False for j in range(len(game_map[0]))] for i in range (len(game_map))]
    for i in range (len(game_map)):
        for j in range(len(game_map[0])):  #A partir de la première case  vite trouvé, j'appelle ma fonction visit
            if game_map[i][j] !=1 and not visited[i][j]:
                visit(game_map,i,j,visited)
                break
        break
    for i in range (len(game_map)): #Si une seule case vide n'as pas été visité, alors la map n'est pas accessible
        for j in range(len(game_map[0])):
            if game_map[i][j] !=1 and not visited[i][j]:
                return False
    return True


"""Fonctions de création et de gestion de déplacement du personnage"""

def create_perso(couple): #Comme demandé au 2.2 question 1
    p={"char":"☻","x":couple[0],"y":couple[1],"score":0}
    return(p)

def update_p(letter,p,m): #Comme demandé au 2.3
    if letter in {"z","Z"} :
        if p["y"]>0 :
            if m[p["y"]-1][p["x"]] != 1 : p["y"]-=1
    elif letter in {"s","S"}:
        if p["y"]<(len(m)-1) :
            if m[p["y"]+1][p["x"]] != 1 : p["y"]+=1
    elif letter in {"q","Q"}:
        if p["x"]>0 :
            if m[p["y"]][p["x"]-1] != 1 : p["x"]-=1
    elif letter in {"d","D"}:
        if p["x"]<(len(m[0])-1) :
            if m[p["y"]][p["x"]+1] != 1 : p["x"]+=1
    #else : stdscr.addstr((len(m)+4),0, "Z = Haut    |S = Bas \nQ = Gauche  |D = Droite") Il s'agit de la manière de prévenir l'utilisateur de comment jouer mais devenu obsolète en raison de l'ajout des monstres


"""Fonctions de création et de mise à jour des objects et d'actualisation du score"""

def create_objects(nb_objects,m): #Comme demandé au 3.4
    position_objects=set()
    while len(position_objects)<nb_objects:
        object_y=random.randint(0,len(m)-1)
        object_x=random.randint(0,len(m[0])-1)
        if m[object_y][object_x]==0: position_objects.add(tuple([object_x,object_y]))
    return position_objects

def update_objects(p,o): #Comme demandé au 3.5
        if ((p["x"],p["y"])) in o:
            o.remove((p["x"],p["y"]))
            p["score"]+=1

"""Fonction de création et de déplacement automatique des monstres"""

def point_de_depart(m):
    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j]==2:
                Entrée=(j,i)
                break
    while True:
        y=random.randint(0,len(m)-1)
        x=random.randint(0,len(m[0])-1)
        if abs(x-Entrée[0])>=3 or abs(y-Entrée[1])>=3:
            if m[y][x]==0:
                return [x,y]

def create_monster(nombre,m): #Crée une liste contenant x nombres de positions correspondant aux positions des monstres
    position_monster=[]
    for i in range(nombre):
        monster=point_de_depart(m)
        position_monster.append(monster)
    return(position_monster)

def deplacement_auto(position_monster,m): #Déplacement automatiquement et aléatoirement chaque monstre en s'assurant que leurs coordonnées ont bien changée
    for Monster in position_monster:
        déplacé=False
        while not déplacé:
            letter = random.choice(["s","q","z","d"])
            if letter == "z":
                if Monster[1]>0 :
                    if m[Monster[1]-1][Monster[0]] != 1 :
                        Monster[1]-=1
                        déplacé = True
            elif letter == "s":
                if Monster[1]<(len(m)-1) :
                    if m[Monster[1]+1][Monster[0]] != 1 :
                        Monster[1]+=1
                        déplacé = True
            elif letter == "q":
                if Monster[0]>0 :
                    if m[Monster[1]][Monster[0]-1] != 1 :
                        Monster[0]-=1
                        déplacé = True
            elif letter =="d":
                if Monster[0]<(len(m[0])-1) :
                    if m[Monster[1]][Monster[0]+1] != 1 :
                        Monster[0]+=1
                        déplacé = True





"""Fonction d'affichage du jeu"""

def display_map(m,d): #Comme demandé au 2.1 | Ici, pas besoin d'implémenter curse
    for lignes in m:
        for i in lignes:
            print(d[i],end="")
        print("")

def display_map_and_char(m,d,p):#     m: Matrice     d=dictionnaire     p=personnage est un DICTIONNAIRE
    for i in range(len(m)):
#On reprend le code source de display_math avec quelques modificaion
#On print avec les indices et aux indices correspondant  du personnage, on l'affiche lui au lieu de l'espace vide
        for j in range (len(m[i])):
            if (i,j)==(p["y"],p["x"]): #Contrairement à ce qui est logique de croire, i<=>y et j<=>x |Equivalence qui va être respecté tout au long du code.
                stdscr.addstr(i,j,p["char"])
            else:
                stdscr.addstr(i,j,d[m[i][j]])

def display_map_char_and_objects(m,p,o):#     m: Matrice     p=personnage est un DICTIONNAIRE    o=objects
#Ici, dico devient obsolète à cause de l'implémentation des couleurs. Nous avons donc choisi de nous en passer
    for i in range(len(m)):
        for j in range (len(m[i])):
            if (i,j)==(p["y"],p["x"]):
                stdscr.addstr(i,j,p["char"],curses.color_pair(1))
            elif (j,i) in o:
                stdscr.addstr(i,j,"*",curses.color_pair(2))
            elif m[i][j] in {0,2}:
                stdscr.addstr(i,j," ",curses.color_pair(1)) #Ici, peu importe la paire couleur utiliser ça revient au même tant que le background est cyan
            elif m[i][j] ==1:
                stdscr.addstr(i,j,"█",curses.color_pair(4))
            else:
                if len(o)!=0: stdscr.addstr(i,j," ",curses.color_pair(1)) #Tant qu'il y'as des objects, c'est un espace vide
                else:stdscr.addstr(i,j," ",curses.color_pair(5)) #Quand il n'y a plus d'objects, il devient visible
    stdscr.addstr((len(m)+3),0, "your score = %d"%p["score"])

def display_map_char_objects_and_monster(m,p,o,monsters): # Répétition de display_map_char_and_objects en rajoutant une vérification supplémentaire pour l'affichage des monstres
    for i in range(len(m)):
        for j in range (len(m[i])):
            if [j,i] in monsters:
                stdscr.addstr(i,j,"⛖",curses.color_pair(3))
            elif (i,j)==(p["y"],p["x"]):
                stdscr.addstr(i,j,p["char"],curses.color_pair(1))
            elif (j,i) in o:
                stdscr.addstr(i,j,"✷",curses.color_pair(2))
            elif m[i][j] in {0,2}:
                stdscr.addstr(i,j," ",curses.color_pair(1))
            elif m[i][j] ==1:
                stdscr.addstr(i,j,"█",curses.color_pair(4))
            else: #ici, m[i][j]==3
                if len(o)!=0: stdscr.addstr(i,j," ",curses.color_pair(1))
                else:stdscr.addstr(i,j," ",curses.color_pair(5))
    stdscr.addstr((len(m)+3),0, "Score = %d"%p["score"])


"""Fonction de mécanisme du jeu"""
def level_up():
    global size,nombre_object,proportion,nombre_monster,increase_monster,speed #Pourque les variables global puissent être modifiée à l'intérieur de la fonction
    if size[0]<104:
        size[0]=size[0]+4
        size[1]=size[1]+1
        nombre_object=nombre_object+1
    if proportion<0.18 : proportion*=1.04
    if increase_monster%2==0:
        nombre_monster+=1
        if speed>0.3:
            speed-=0.06

def create_new_level():
    global perso,game_map,objects,size,proportion,Monsters
    game_map = generate_random_game_map(size,proportion)
    while not (is_accessible(game_map)):
        game_map = generate_random_game_map(size,proportion)
    objects = create_objects(nombre_object,game_map)
    Monsters=create_monster(nombre_monster,game_map)
    for i in range(len(game_map)):
        for j in range(len(game_map[i])):
            if game_map[i][j]==2:
                perso["y"],perso["x"]=i,j
                break

def high_score(nom):
    c = open(nom,"r")
    return (int(c.read()))

def sauvegarde(meilleur_score):
    fichier="high_score.txt"
    c= open(fichier,"w")
    c.write(str(meilleur_score))


"""Valeur initial"""

Record=high_score("high_score.txt")
perso=create_perso((0,0))
size=[16,4]
proportion=0.10
nombre_object=2
nombre_monster=1
increase_monster=0
create_new_level()
speed=1 #en secondes
temps_depart = time.time()

"""Les boucles infinies qui exécutent le jeu"""
while True:
    #Utilisation des clauses try_except pour gérer les erreurs lié à la définition d'un temps d'attentes pour les opérartions de saisies (cf ligne 17)
    try: #Essayer ceci dans un premier temps en supposant que l'utilisateur ait appuyer sur une touche
        temps_actuel = time.time()
        temps_ecoule = temps_actuel - temps_depart
        d = stdscr.getkey()
        stdscr.erase()
        if temps_ecoule>=speed: #Pour déplacer automatiquement les monstres à des intervalles régulier de speed secondes
            deplacement_auto(Monsters,game_map)
            temps_depart=time.time()
        if d in {"p","P"}:break
        else: update_p(d,perso,game_map)
        update_objects(perso,objects)
        if perso["score"]>Record: #Actualisation et Sauvegarde du meilleur score
            Record=perso["score"]
            sauvegarde(Record)
        if [perso["x"],perso["y"]] in Monsters:
            break
        if game_map[perso["y"]][perso["x"]]==3 and len(objects)==0:
            increase_monster+=1
            level_up()
            create_new_level()
        display_map_char_objects_and_monster(game_map,perso,objects,Monsters)
        stdscr.addstr((len(game_map)+4),0, "High Score = %d"%Record) #Affichage du meilleur score
        stdscr.refresh()
    except curses.error as e: #Si l'utilisateur n'appuie sur rien, alors le code dans la clause try renverra un curse.error et dans ce cas, on exécutera ce bout de code qui ne prends pas en compte l'entrée de l'utilisateur
        temps_actuel = time.time()
        temps_ecoule = temps_actuel - temps_depart
        stdscr.erase()
        if temps_ecoule>=speed:
            deplacement_auto(Monsters,game_map)
            temps_depart=time.time()
        if [perso["x"],perso["y"]] in Monsters:
            break
        display_map_char_objects_and_monster(game_map,perso,objects,Monsters)
        stdscr.addstr((len(game_map)+4),0, "High Score = %d"%Record)
        stdscr.refresh()


#Affichage durant 5 secondes de l'écran gameOver
stdscr.erase()
stdscr.refresh()
temps_depart = time.time()
while True:
    temps_actuel = time.time()
    temps_ecoule = temps_actuel - temps_depart
    display_map_char_objects_and_monster(game_map,perso,objects,Monsters)
    stdscr.addstr((len(game_map)+2),0, "GAME OVER !")
    stdscr.addstr((len(game_map)+4),0, "High Score = %d"%Record)
    stdscr.refresh()
    if temps_ecoule>=5:
        break

