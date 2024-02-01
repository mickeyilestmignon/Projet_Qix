from fltk import *
from random import randrange
from sys import setrecursionlimit
from time import sleep, time
from Affichage import *
from Variables import *
import doctest

setrecursionlimit(10000)

###############
### FENETRE ###  ------------------------------------------------------------------------------------------------------------------
###############


cree_fenetre(largeur_fenetre, hauteur_fenetre)

rectangle(0, 0, largeur_fenetre, hauteur_fenetre, remplissage=couleur_fenetre)



###################################
### FONCTIONS AUXILIARES DE JEU ### ------------------------------------------------------------------------------------------------
###################################


def sur_une_ligne(liste_ligne, x, y):
    # Prend en paramètre une liste de lignes (lignes_tracees/lignes_temporaires) et des
    # coordonnées x et y, renvoie True si ces coordonnées appatiennent à une ligne de la liste, False sinon.
    """
    >>> sur_une_ligne([], 10, 5)
    False
    >>> sur_une_ligne([((1, 4), (1, 12))], 1, 6  )
    True
    >>> sur_une_ligne([((1, 4), (1,12))], 1, 12)
    True
    """

    for ligne in liste_ligne: # Verifie qu'on soit sur une ligne
        if ((x >= ligne[0][0] and x <= ligne[1][0] and y >= ligne[0][1] and y <= ligne[1][1]) or # SI AX >= BX ET AY >= BY
            (x <= ligne[0][0] and x >= ligne[1][0] and y <= ligne[0][1] and y >= ligne[1][1])): # SI AX <= BX ET AY <= BY
            return True
    
    return False

def ligne_inutile(ligne): #sert lorsque le joueur est en mode tracage, pour éviter qu'il se balade sur le cadre
    '''
    Renvoie True si la ligne en paramètre est inutile, c'est à dire qu'elle a une longeur de pas, et que son milieu appartient déjà à une ligne tracée, False sinon.
    Sert à éviter qu'un mouvement d'un pas en mode traçage sur une ligne tracée existante ne remplisse l'intégralité de la zone.
    '''
    return sur_une_ligne(lignes_tracees, (ligne[0][0] + ligne[1][0])//2, (ligne[0][1] + ligne[1][1])//2)

def point_dans_zone(liste_ligne, x, y):
    """
    Renvoie True si le point se trouve dans la zone définie par liste_lignes, False sinon.
    Si, en parcourant tous les points directement à droite du point, on recontre un nombre
    pair de fois une ligne verticale de liste_lignes, le point n'est pas dans la zone, si le nombre
    de rencontre est impair, le point est dans la zone.
    """
    nb_lignes_touches = 0
    
    if sur_une_ligne(liste_ligne, x, y):
        return True
    
    while x <= droite_terrain:
        if sur_une_ligne(liste_ligne, x, y):
            nb_lignes_touches += 1
            x += pas//2
            while x <= droite_terrain and sur_une_ligne(liste_ligne, x, y):
                x += pas
            x += pas//2
        else:
            x += pas
    return nb_lignes_touches % 2 != 0

def Point_en_Ligne(Liste):
    # Fonction qui prend une liste/tuple de point et qui renvoie un tuple de lignes
    # La liste ou le tuple de point doit au préalable être ordonnée car la fonction 
    # ne vérifie pas si les deux points sont alignées verticalement ou horizontalement
    """
    >>> Point_en_Ligne([[1,2], [3, 4], [5, 6]])
    [([1, 2], [3, 4]), ([3, 4], [5, 6]), ([5, 6], [1, 2])]
    """
    Tableau = []
    for i in range(0,len(Liste)-1):
        Tableau.append((Liste[i],Liste[i+1]))
    Tableau.append((Liste[len(Liste)-1],Liste[0]))
    return Tableau

def nouvelles_lignes_tracees(lignes_interdites): # permet d'update le cadre : 
    """
    Met à jour les lignes tracées en supprimant les lignes contenues entièrement dans lignes_interdites
    et en supprimant les portions de lignes contenues dans les lignes interdites.
    """
    global lignes_tracees
    
    # Enlève les lignes identiques
    for ligne in lignes_tracees:
        if ligne in lignes_interdites or ((ligne[0][1], ligne[0][0]), (ligne[1][1], ligne[1][0])) in lignes_interdites: # Si ligne dans l'autre sens
            lignes_tracees.remove(ligne)
    
    nouvelles_lignes = []
    
    # Modifie les deux lignes restantes
    for ligne in lignes_tracees:
        
        if ligne[0][0] == ligne[1][0]: # Si xa == xb (ligne verticale)
            
            y_debut = int(min(ligne[0][1], ligne[1][1]))
            y_fin = int(max(ligne[0][1], ligne[1][1]))
            x = ligne[0][0]
            
            ligne_en_cours = False
            y_nouveau_debut = None
            y_nouvelle_fin = None
            
            for y in range(y_debut, y_fin+pas, pas):
                
                if not sur_une_ligne(lignes_interdites, x, y+pas//2) and not ligne_en_cours: 
                    ligne_en_cours = True
                    y_nouveau_debut = y
                    
                elif sur_une_ligne(lignes_interdites, x, y) and ligne_en_cours:
                    ligne_en_cours = False
                    y_nouvelle_fin = y
                    nouvelles_lignes.append(((x, y_nouveau_debut), (x, y_nouvelle_fin)))
                    
                elif y_fin - y == 0 and ligne_en_cours:
                    y_nouvelle_fin = y
                    nouvelles_lignes.append(((x, y_nouveau_debut), (x, y_nouvelle_fin)))
        
        else: # Si ya == yb (ligne horizontale)
            
            x_debut = int(min(ligne[0][0], ligne[1][0]))
            x_fin = int(max(ligne[0][0], ligne[1][0]))
            y = ligne[0][1]
            
            ligne_en_cours = False
            x_nouveau_debut = None
            x_nouvelle_fin = None
            
            for x in range(x_debut, x_fin+pas, pas):
                
                if not sur_une_ligne(lignes_interdites, x+pas//2, y) and not ligne_en_cours:
                    ligne_en_cours = True
                    x_nouveau_debut = x
                    
                elif sur_une_ligne(lignes_interdites, x, y) and ligne_en_cours:
                    ligne_en_cours = False
                    x_nouvelle_fin = x
                    nouvelles_lignes.append(((x_nouveau_debut, y), (x_nouvelle_fin, y)))
                    
                elif x_fin - x == 0 and ligne_en_cours:
                    x_nouvelle_fin = x
                    nouvelles_lignes.append(((x_nouveau_debut, y), (x_nouvelle_fin, y)))
    
    lignes_tracees = nouvelles_lignes
    
    surligne_tracees()

def surligne_tracees(): # Augmente l'épaisseur du cadre
    """
    Surligne les lignes tracées actuelles.
    """
    efface('lignes_surlignes')
    for _ligne in lignes_tracees:
        rectangle(_ligne[0][0], _ligne[0][1], _ligne[1][0], _ligne[1][1], couleur=couleur_elements, epaisseur=pas//2,tag='lignes_surlignes')

def calcul_aire(liste_lignes):
    """
    Renvoie l'aire de la forme définie par liste_lignes, passe à True dans zones_joueur les cases conquises.
    """
    global haut_terrain, gauche_terrain, droite_terrain, bas_terrain, pas, points, zones_joueur

    aire = 0
    ajouter = False

    haut_terrain = int(haut_terrain)
    gauche_terrain = int(gauche_terrain)
    droite_terrain = int(droite_terrain)
    bas_terrain = int(bas_terrain)
    pas = int(pas)

    for y in range(haut_terrain + pas//2, bas_terrain, pas):
        for x in range(gauche_terrain, droite_terrain + 1, pas):
            if sur_une_ligne(liste_lignes, x, y):
                ajouter = not ajouter
            if ajouter:
                if not sur_une_ligne(liste_lignes, x, y - pas//2):
                    zones_joueur.append((x,y - pas//2))
                aire += pas*pas
                points += 1*vitesse
    
    return aire

def est_dans_zone(x_joueur, y_joueur):
    """
    Renvoie True si le joueur est dans une zone conquise, False sinon.
    """
    if gauche_terrain <= x_joueur <= droite_terrain and haut_terrain <= y_joueur <= bas_terrain:
        return (x_joueur, y_joueur) in zones_joueur
    return True

def touche_une_ligne_tracee(directions): # Evenement fin du tracage 
    '''
    Quand le joueur touche une ligne tracée, passe les lignes de la liste lignes_temporaires dans la liste lignes_tracees 
    et met à jour le mode du joueur.
    '''
    global lignes_temporaires, lignes_interdites, mode, points_polygone, points_polygone_ferme, zone_conquise
    
    lignes_tracees.extend(lignes_temporaires) # Met toutes les lignes temporaires dans les lignes tracées
    lignes_temporaires = []

    points_polygone.append((x_joueur, y_joueur)) # Point de depart pour la fonction fermer la zone

    mode = 'déplacement'
    texte_mode_joueur(mode)
    
    ### 1ère zone ###
    fermer_la_zone(directions[0], points_polygone[len(points_polygone)-1][0], points_polygone[len(points_polygone)-1][1]) # 1ere direction, x et y
    points_polygone_totaux = points_polygone + points_polygone_ferme # Tous les points de la forme
    lignes_polygone_totales = Point_en_Ligne(points_polygone_totaux) # Les lignes de la forme

    if not point_dans_zone(lignes_polygone_totales, x_qix, y_qix): # Si le qix n'est pas à l'interieur de la 1ère zone
        
        polygone(points_polygone_totaux, couleur=couleur_elements, remplissage=couleur_zones, tag='zones') # colorie la 1ere zone possible
        
        zone_conquise += calcul_aire(lignes_polygone_totales) # Ajoute l'aire la première zone

    ### 2ème zone ###
    else: # Si le qix est dans la 1ère zone
        
        points_polygone_ferme = []
        
        fermer_la_zone(directions[1], points_polygone[len(points_polygone)-1][0], points_polygone[len(points_polygone)-1][1]) # 2eme direction, x et y
        points_polygone_totaux = points_polygone + points_polygone_ferme
        lignes_polygone_totales = Point_en_Ligne(points_polygone_totaux)
        
        polygone(points_polygone_totaux, couleur=couleur_elements, remplissage=couleur_zones, tag='zones')# colorie la 2eme zone possible
        
        zone_conquise += calcul_aire(lignes_polygone_totales) # Ajoute l'aire de la 2eme zone
        
    texte_zone_conquise(zone_conquise)
    texte_points(points)
    
    ### Met à jour les lignes tracées ###
    lignes_interdites = Point_en_Ligne([points_polygone[len(points_polygone)-1]] + points_polygone_ferme + [points_polygone[0]])
    lignes_interdites.pop() # La fonction Point_en_Ligne ajoute à la fin une ligne entre le 1er et le dernier point, dans ce cas, on n'en a pas besoin donc on l'enlève
    nouvelles_lignes_tracees(lignes_interdites)

    points_polygone_ferme = []
    points_polygone = []

def touche_une_ligne_temporaire():
    '''
    Quand le joueur touche une ligne temporaire, efface les lignes temporaires, replace le joueur
    au milieu du côte bas du terrain, met à jour le mode du joueur, et réinitialise points_polygone.
    '''
    global lignes_temporaires, x_joueur, y_joueur, mode, points_polygone, vies
    
    lignes_temporaires = []
    efface(numero_trace_temp)
    efface('ligne_temporaire_en_cours')
    
    x_joueur = points_polygone[0][0]
    y_joueur = points_polygone[0][1]
    
    mode = 'déplacement'
    texte_mode_joueur(mode)
    
    vies -= 1
    texte_vies_joueur(vies)
    
    points_polygone = []

def changement_de_direction():
    '''
    Quand le joueur change de direction en mode traçage, les remplace
    par une ligne temporaire et met à jour les positions de début pour la prochaine ligne.
    '''
    global x_ligne_debut, y_ligne_debut
    
    efface('ligne_temporaire_en_cours')
    
    lignes_temporaires.append(((x_ligne_debut, y_ligne_debut),(x_joueur, y_joueur)))
    dessine_ligne(x_ligne_debut, y_ligne_debut, x_joueur, y_joueur, numero_trace_temp)
    
    points_polygone.append((x_joueur, y_joueur))
    
    x_ligne_debut = x_joueur
    y_ligne_debut = y_joueur


def directions_possibles(direction_initiale, x, y, liste_lignes):
    '''
    Prend en paramètre une direction et des coordonnées x et y et renvoie les directions qu'il est possible de prendre en restant sur une ligne tracée (sans faire demi-tour).
    '''
    directions = []
    
    if direction_initiale != 'bas' and sur_une_ligne(liste_lignes, x, y - pas//2):
         directions.append('haut')
    
    if direction_initiale != 'haut' and sur_une_ligne(liste_lignes, x, y + pas//2):
        directions.append('bas')
    
    if direction_initiale != 'droite' and sur_une_ligne(liste_lignes, x - pas//2, y):
        directions.append('gauche')
    
    if direction_initiale != 'gauche' and sur_une_ligne(liste_lignes, x + pas//2, y):
        directions.append('droite')
    
    return directions
    
def fermer_la_zone(direction, x_chercheur_pas, y_chercheur_pas):
    '''
    Permet de fermer la zone que le joueur a tracé en suivant les bordures de zones et en ajoutant les points dans le tracé.
    '''
    global points_polygone_ferme
    
    # La position du chercheur
    x_chercheur_debut = x_chercheur_pas
    y_chercheur_debut = y_chercheur_pas
    
    # La où le chercheur regarde
    if direction == 'haut':
        y_chercheur_pas -= pas//2
    elif direction == 'bas':
        y_chercheur_pas += pas//2
    elif direction == 'gauche':
        x_chercheur_pas -= pas//2
    elif direction == 'droite':
        x_chercheur_pas += pas//2
    
    if sur_une_ligne(lignes_tracees, x_chercheur_pas, y_chercheur_pas): # Devant soi, on est sur une ligne
        if x_chercheur_pas == points_polygone[0][0] and y_chercheur_pas == points_polygone[0][1]: # Verifie si on touche le point de départ
            return points_polygone_ferme
        else:
            fermer_la_zone(direction, x_chercheur_pas, y_chercheur_pas) # On continue d'aller dans la même direction 
    else: # On est à un changement de direction
        points_polygone_ferme.append((x_chercheur_debut, y_chercheur_debut)) # On ajoute le point dans la liste points_polygone
        fermer_la_zone(directions_possibles(direction, x_chercheur_debut, y_chercheur_debut, lignes_tracees)[0], x_chercheur_debut, y_chercheur_debut) # On continue dans la direction qu'il est possible de prendre (On prend [0] car normalement il est sensé n'y en avoir qu'une)

def init_obstacles(nombre_obstacles):
    """
    Initialise nombre_obstacles obstacles
    """
    global liste_obstacles
    
    liste_obstacles = []
    for _ in range(nombre_obstacles):
        liste_obstacles.append((randrange(int(gauche_terrain), int(droite_terrain-taille_obstacle)), randrange(int(haut_terrain), int(bas_terrain-taille_obstacle))))

def dessine_obstacle(liste_obstacles):
    """
    Dessine les obstacles sur la zone de jeu
    """
    efface('obstacle')
    for obstacle in liste_obstacles:
        image(obstacle[0], obstacle[1], 'obstacle.png', largeur=taille_obstacle, hauteur=taille_obstacle, ancrage='nw', tag='obstacle')

def est_dans_obstacle(x, y, liste_obstacles):
    """
    Renvoie True si le point de coordonnées x y est dans un obstacle, False sinon.
    """
    for obstacle in liste_obstacles:
        if obstacle[0] <= x <= obstacle[0]+taille_obstacle and obstacle[1] <= y <= obstacle[1]+taille_obstacle:
            return True
    return False

def init_pommes(nombre_pommes):
    """
    Initialise nombre_pommes pommes.
    """
    global liste_pommes
    
    liste_pommes = []
    for _ in range(nombre_pommes):
        x_pomme = randrange(int(gauche_terrain), int(droite_terrain), pas)
        y_pomme = randrange(int(haut_terrain), int(bas_terrain), pas)
        while est_dans_obstacle(x_pomme, y_pomme, liste_obstacles):
            x_pomme = randrange(int(gauche_terrain), int(droite_terrain), pas)
            y_pomme = randrange(int(haut_terrain), int(bas_terrain), pas)
        liste_pommes.append((x_pomme, y_pomme))
        
def dessine_pommes(liste_pommes):
    """
    Dessine les pommes.
    """
    for pomme in range(len(liste_pommes)):
        efface('pomme_'+str(pomme))
        image(liste_pommes[pomme][0], liste_pommes[pomme][1], 'pomme.png', largeur=pas*4, hauteur=pas*4, ancrage='center', tag='pomme_'+str(pomme))
        
def touche_pomme(liste_pommes):
    """
    Verifie si le joueur touche une pomme, si oui, efface la pomme touchée et rend le joueur invisible pendant 3 secondes.
    """
    global timer_invincible, invincible, couleur_joueur
    
    for pomme in range(len(liste_pommes)):
        if (x_joueur, y_joueur) == liste_pommes[pomme]:
            efface('pomme_'+str(pomme))
            liste_pommes[pomme] = (None, None)
            efface('logo_qix')
            invincible = True
            timer_invincible = time()
            break   

def reset():
    """
    Réinitialise le jeu et passe au niveau suivant.
    """
    global niveau, diviseur_difficulte, lignes_tracees, x_joueur, y_joueur, vies, zone_conquise, points, x_qix, y_qix, x_sparx_1, y_sparx_1, direction_sparx_1, mouvements_sparx_1, x_sparx_2, y_sparx_2, direction_sparx_2, mouvements_sparx_2, zones_joueur, liste_obstacles
    
    lignes_tracees = [
                ((gauche_terrain, haut_terrain),(droite_terrain, haut_terrain)),
                ((gauche_terrain, bas_terrain),(droite_terrain, bas_terrain)),
                ((gauche_terrain, haut_terrain),(gauche_terrain, bas_terrain)),
                ((droite_terrain, haut_terrain),(droite_terrain, bas_terrain))
                ]
    
    x_joueur = largeur_fenetre/2
    y_joueur = bas_terrain
    joueur(x_joueur, y_joueur, pas)
    
    vies = 3
    texte_vies_joueur(vies)
    zone_conquise = 0
    texte_zone_conquise(zone_conquise)
    
    x_qix = largeur_fenetre//2
    y_qix = hauteur_fenetre//2
    
    x_sparx_1 = largeur_fenetre//2
    y_sparx_1 = haut_terrain
    direction_sparx_1 = 'gauche'
    mouvements_sparx_1 = []
    
    x_sparx_2 = largeur_fenetre//2
    y_sparx_2 = haut_terrain
    direction_sparx_2 = 'droite'
    mouvements_sparx_2 = []
    
    surligne_tracees()
    efface('zones')
    efface('lignes_dessines')
    
    zones_joueur = []
    
    init_obstacles(nombre_obstacles)
    dessine_obstacle(liste_obstacles)
    
    init_pommes(nombre_pommes)
    dessine_pommes(liste_pommes)

#######################
### INITIALISATIONS ### ----------------------------------------------------------------------------------------------------------
#######################

image(largeur_fenetre/2, haut_terrain*0.5, 'qix_logo.png', ancrage='center', tag='logo_qix')

texte_niveau(niveau)
texte_zone_conquise(zone_conquise)
texte_points(points)

texte_mode_joueur(mode)
texte_vies_joueur(vies)
texte_vitesse_joueur(vitesse)

surligne_tracees()
joueur(x_joueur, y_joueur, rayon)

f = open('obstacles.txt', 'r')

ligne = f.readline().strip()
if ligne == 'True':
    taille_obstacle = int(f.readline().strip())
    ligne = f.readline()
    while ligne != '':
        x_obstacle = int(ligne.strip().split()[0])
        y_obstacle = int(ligne.strip().split()[1])
        #print(gauche_terrain, x_obstacle, droite_terrain-taille_obstacle, haut_terrain, y_obstacle, bas_terrain-taille_obstacle)
        if gauche_terrain <= x_obstacle <= droite_terrain-taille_obstacle and haut_terrain <= y_obstacle <= bas_terrain-taille_obstacle:
            liste_obstacles.append((x_obstacle, y_obstacle))
        ligne = f.readline().strip()
else:
    init_obstacles(nombre_obstacles)

f.close()

dessine_obstacle(liste_obstacles)

f = open('pommes.txt', 'r')

ligne = f.readline().strip()
if ligne == 'True':
    ligne = f.readline()
    while ligne != '':
        x_pomme = int(ligne.strip().split()[0])
        y_pomme = int(ligne.strip().split()[1])
        if gauche_terrain <= x_pomme <= droite_terrain and haut_terrain <= y_pomme <= bas_terrain and not est_dans_obstacle(x_pomme, y_pomme, liste_obstacles):
            liste_pommes.append((x_pomme, y_pomme))
        ligne = f.readline().strip()
else:
    init_pommes(nombre_pommes)

dessine_pommes(liste_pommes)

f.close()

#####################
### BOUCLE DE JEU ### -------------------------------------------------------------------------------------------------------------
#####################

if __name__ == '__main__':
    doctest.testmod()

    while True:
        evenement = donne_ev()
        type_evenement = type_ev(evenement)
        cpt_ticks += 1
        
        ###########
        ### QIX ###
        ###########
        """On détermine premierement la directions et enfin la distance que va parcourir le qix"""
            
        if not a_trajectoire:
            
            a_trajectoire = True
            pas_qix_x = randrange(-pas, 2*pas, pas)
            pas_qix_y = randrange(-pas, 2*pas, pas)
            longueur_trajectoire = randrange(10, 31)
            trajectoire_parcourue = 0
        
        if sur_une_ligne(lignes_temporaires, x_qix, y_qix) and not invincible: # Verifie si le qix touche le joueur
            
            touche_une_ligne_temporaire() # On le tue
            joueur(x_joueur, y_joueur, rayon)
        
        x_qix += pas_qix_x
        y_qix += pas_qix_y
        
        if sur_une_ligne(lignes_tracees, x_qix, y_qix) or trajectoire_parcourue == longueur_trajectoire: # Verifie si le qix touche une ligne tracée ou si il a fini de parcourir sa trajectoire
            
            x_qix -= pas_qix_x
            y_qix -= pas_qix_y
            a_trajectoire = False
        
        trajectoire_parcourue += 1
        qix(x_qix, y_qix)
    
    #############
    ### SPARX ###
    #############
    
        ### Sparx 1 ###
        
        if x_sparx_1 == x_joueur and y_sparx_1 == y_joueur and not invincible: # Enlève une vie au joueur
            
            vies -= 1
            texte_vies_joueur(vies)
        
        # En fonction de la direction actuelle du sparx, définit le déplacemnt correspondant
        
        if direction_sparx_1 == 'gauche':
            pas_sparx_1_x = -pas//diviseur_difficulte
            pas_sparx_1_y = 0
        elif direction_sparx_1 == 'droite':
            pas_sparx_1_x = pas//diviseur_difficulte
            pas_sparx_1_y = 0
        elif direction_sparx_1 == 'haut':
            pas_sparx_1_x = 0
            pas_sparx_1_y = -pas//diviseur_difficulte
        elif direction_sparx_1 == 'bas':
            pas_sparx_1_x = 0
            pas_sparx_1_y = pas//diviseur_difficulte
            
        if sur_une_ligne(lignes_tracees, x_sparx_1 + pas_sparx_1_x, y_sparx_1 + pas_sparx_1_y): # Si le sparx est sur une ligne devant soi, ajoute le déplacement
            
            x_sparx_1 += pas_sparx_1_x
            y_sparx_1 += pas_sparx_1_y
            
            sparx_1(x_sparx_1, y_sparx_1)
            
            mouvements_sparx_1.append((pas_sparx_1_x, pas_sparx_1_y))
        
        else: # Si il n'est pas sur une ligne devant soi
            
            if not sur_une_ligne(lignes_tracees, x_sparx_1, y_sparx_1): # Si le sparx lui-même n'est pas sur une ligne (enfermé dans une zone), parcoure tous les mouvements précédents jusqu'à revenir sur une ligne
                
                if len(mouvements_sparx_1) > 0:
                    
                    x_sparx_1 -= mouvements_sparx_1[-1][0]
                    y_sparx_1 -= mouvements_sparx_1[-1][1]
                    mouvements_sparx_1.pop()
                
                sparx_1(x_sparx_1, y_sparx_1)
                
            else:
                
                direction_sparx_1 = directions_possibles(direction_sparx_1, x_sparx_1, y_sparx_1, lignes_tracees)[0] # Trouve la nouvelle direction à prendre
                
                if direction_sparx_1 == 'gauche':
                    pas_sparx_1_x = -pas//diviseur_difficulte
                    pas_sparx_1_y = 0
                elif direction_sparx_1 == 'droite':
                    pas_sparx_1_x = pas//diviseur_difficulte
                    pas_sparx_1_y = 0
                elif direction_sparx_1 == 'haut':
                    pas_sparx_1_x = 0
                    pas_sparx_1_y = -pas//diviseur_difficulte
                elif direction_sparx_1 == 'bas':
                    pas_sparx_1_x = 0
                    pas_sparx_1_y = pas//diviseur_difficulte
                    
                x_sparx_1 += pas_sparx_1_x
                y_sparx_1 += pas_sparx_1_y
                
                sparx_1(x_sparx_1, y_sparx_1)
                
                mouvements_sparx_1.append((pas_sparx_1_x, pas_sparx_1_y))
        
        ### Sparx 2 ###
        
        if x_sparx_2 == x_joueur and y_sparx_2 == y_joueur and not invincible:
            
            vies -= 1
            texte_vies_joueur(vies)
            
        if direction_sparx_2 == 'gauche':
            pas_sparx_2_x = -pas//diviseur_difficulte
            pas_sparx_2_y = 0
        elif direction_sparx_2 == 'droite':
            pas_sparx_2_x = pas//diviseur_difficulte
            pas_sparx_2_y = 0
        elif direction_sparx_2 == 'haut':
            pas_sparx_2_x = 0
            pas_sparx_2_y = -pas//diviseur_difficulte
        elif direction_sparx_2 == 'bas':
            pas_sparx_2_x = 0
            pas_sparx_2_y = pas//diviseur_difficulte
            
        if sur_une_ligne(lignes_tracees, x_sparx_2 + pas_sparx_2_x, y_sparx_2 + pas_sparx_2_y):
            
            x_sparx_2 += pas_sparx_2_x
            y_sparx_2 += pas_sparx_2_y
            
            sparx_2(x_sparx_2, y_sparx_2)
            
            mouvements_sparx_2.append((pas_sparx_2_x, pas_sparx_2_y))
        
        else:
            
            if not sur_une_ligne(lignes_tracees, x_sparx_2, y_sparx_2):
                
                if len(mouvements_sparx_2) > 0:

                    x_sparx_2 -= mouvements_sparx_2[-1][0]
                    y_sparx_2 -= mouvements_sparx_2[-1][1]
                    mouvements_sparx_2.pop()
                
                sparx_2(x_sparx_2, y_sparx_2)
            
            else:

                direction_sparx_2 = directions_possibles(direction_sparx_2, x_sparx_2, y_sparx_2, lignes_tracees)[0]
                
                if direction_sparx_2 == 'gauche':
                    pas_sparx_2_x = -pas//diviseur_difficulte
                    pas_sparx_2_y = 0
                elif direction_sparx_2 == 'droite':
                    pas_sparx_2_x = pas//diviseur_difficulte
                    pas_sparx_2_y = 0
                elif direction_sparx_2 == 'haut':
                    pas_sparx_2_x = 0
                    pas_sparx_2_y = -pas//diviseur_difficulte
                elif direction_sparx_2 == 'bas':
                    pas_sparx_2_x = 0
                    pas_sparx_2_y = pas//diviseur_difficulte
                    
                x_sparx_2 += pas_sparx_2_x
                y_sparx_2 += pas_sparx_2_y
                
                sparx_2(x_sparx_2, y_sparx_2)
                
                mouvements_sparx_2.append((pas_sparx_2_x, pas_sparx_2_y))
            
        ##############
        ### JOUEUR ###
        ##############
            
        if zone_conquise >= largeur_terrain*hauteur_terrain*0.75: # SI LE JOUEUR GAGNE
            
            sleep(1)
            
            niveau += 1
            texte_niveau(niveau)
            
            if diviseur_difficulte > 1:
                diviseur_difficulte //= 2
            if nombre_pommes > 0:
                nombre_pommes -= 1
            if nombre_obstacles < 8:
                nombre_obstacles += 1
                
            reset()
            
        if type_evenement == 'Quitte': # QUITTER LE JEU
            break
        
        if vies <= 0: # SI LE JOUEUR PERD
            
            sleep(1)
            
            points = 0
            texte_points(points)
            
            niveau = 1
            texte_niveau(niveau)
            
            nombre_pommes = 3
            nombre_obstacles = 3
            diviseur_difficulte = pas
            
            reset()
            
        touche_pomme(liste_pommes)
        if invincible:
            efface('invincible')
            texte(largeur_fenetre//2, haut_terrain*0.5, 'Invincibilité : '+str(round(3-(time()-timer_invincible), 1)), taille=24, couleur=couleur_elements, ancrage='c', tag='invincible')
            if time() - timer_invincible >= 3:
                invincible = False
                efface('invincible')
                image(largeur_fenetre//2, haut_terrain*0.5, 'qix_logo.png', ancrage='center', tag='logo_qix')
        
        if type_evenement == 'Touche' and cpt_ticks % vitesse == 0: # ACTIONS DU JOUEUR, en fonction de la vitesse
            
            if touche(evenement) == 'p': # TEST DEBUG
                print('x :', x_joueur, 'y :', y_joueur)
                
                print('lignes_tracees :', lignes_tracees)
                print('nombre de lignes tracées :', len(lignes_tracees))
                
                print('lignes temporaires :', lignes_temporaires)
                print('nombre de lignes temporaires :', len(lignes_temporaires))
                
                print('zones joueur :', zones_joueur)
                
                vies = 10000
                texte_vies_joueur(vies)
            
            if mode == 'déplacement': # SE DEPLACER SUR LES LIGNES EXISTANTES
                
                ####################
                ### DEPLACEMENTS ###
                ####################
                
                if touche(evenement) == 'Up' and sur_une_ligne(lignes_tracees, x_joueur, y_joueur - pas//2) and not est_dans_obstacle(x_joueur, y_joueur - pas, liste_obstacles): # HAUT
                    y_joueur -= pas
                    joueur(x_joueur, y_joueur, rayon)
                    
                
                elif touche(evenement) == 'Down' and sur_une_ligne(lignes_tracees, x_joueur, y_joueur + pas//2) and not est_dans_obstacle(x_joueur, y_joueur + pas, liste_obstacles): # BAS
                    y_joueur += pas
                    joueur(x_joueur, y_joueur, rayon)
                    
                
                elif touche(evenement) == 'Left' and sur_une_ligne(lignes_tracees, x_joueur - pas//2, y_joueur) and not est_dans_obstacle(x_joueur - pas, y_joueur, liste_obstacles): # GAUCHE
                    x_joueur -= pas
                    joueur(x_joueur, y_joueur, rayon)
                    
                
                elif touche(evenement) == 'Right' and sur_une_ligne(lignes_tracees, x_joueur + pas//2, y_joueur) and not est_dans_obstacle(x_joueur + pas, y_joueur, liste_obstacles): # DROITE
                    x_joueur += pas
                    joueur(x_joueur, y_joueur, rayon)
                    
                #############################################
                ### AUTRES EVENEMENTS EN MODE DEPLACEMENT ###
                #############################################
                    
                elif touche(evenement) == 'Return': # PASSER EN MODE TRACAGE
                    
                    mode = 'traçage'
                    texte_mode_joueur(mode)
                    
                    x_ligne_debut = x_joueur
                    y_ligne_debut = y_joueur
                    
                    premiere_direction = None
                    numero_trace_temp += 'I'
                    
                    points_polygone.append((x_joueur, y_joueur))
                    
                if touche(evenement) == 'space': # Changer la vitesse
            
                    if vitesse == 1:
                        vitesse = 2
                    else:
                        vitesse = 1
                    texte_vitesse_joueur(vitesse)
                    
                
            elif mode == 'traçage': # CREER DE NOUVELLES LIGNES
                
                ###############
                ### TRACAGE ###
                ###############
                
                if touche(evenement) == 'Up' and not est_dans_zone(x_joueur, y_joueur - pas) and not est_dans_obstacle(x_joueur, y_joueur - pas, liste_obstacles):  # HAUT
                    
                    if not ligne_inutile(((x_ligne_debut, y_ligne_debut),(x_joueur, y_joueur - pas))): # POUR QUE LE PREMIER MOUVEMENT DU JOUEUR NE SOIT PAS SUR UNE LIGNE TRACEE
                        
                        if premiere_direction is None: # SI LE JOUEUR N'A PAS ENCORE FAIT DE MOUVEMENT : ON SAUVEGARDE LE PREMIER MOUVEMENT
                            
                            premiere_direction = 'Up'
                            
                        elif premiere_direction != 'Up': # SI LE MOUVEMENT DU JOUEUR EST DIFFERENT DU PREMIER MOUVEMENT
                            
                            changement_de_direction()
                            premiere_direction ='Up'
                        
                        if sur_une_ligne(lignes_temporaires, x_joueur, y_joueur - pas): # SI LE JOUEUR TOUCHE UNE DE SES LIGNES TEMPORAIRES
                            
                            touche_une_ligne_temporaire()
                        
                        elif sur_une_ligne(lignes_tracees, x_joueur, y_joueur - pas): # SI LE JOUEUR TOUCHE UNE LIGNE TRACEE
                            
                            if len(lignes_temporaires) != 0:
                                lignes_temporaires.pop()
                            lignes_temporaires.append(((x_ligne_debut, y_ligne_debut),(x_joueur, y_joueur - pas)))
                            dessine_ligne(x_ligne_debut, y_ligne_debut, x_joueur, y_joueur - pas, numero_trace_temp)
                            
                            y_joueur -= pas
                            
                            directions = directions_possibles('haut', x_joueur, y_joueur, lignes_tracees)
                            touche_une_ligne_tracee(directions)
                            
                        else: # SI LE JOUEUR FAIT LE MEME MOUVEMENT QUE LE PREMIER
                            
                            if len(lignes_temporaires) != 0:
                                lignes_temporaires.pop()
                            lignes_temporaires.append(((x_ligne_debut, y_ligne_debut), (x_joueur, y_joueur - pas)))
                            efface('ligne_temporaire_en_cours')
                            dessine_ligne(x_ligne_debut, y_ligne_debut, x_joueur, y_joueur - pas, 'ligne_temporaire_en_cours')
                            
                            y_joueur -= pas
                        
                        joueur(x_joueur, y_joueur, rayon)
                    
                
                elif touche(evenement) == 'Down' and not est_dans_zone(x_joueur, y_joueur + pas) and not est_dans_obstacle(x_joueur, y_joueur + pas, liste_obstacles): # BAS
                    
                    if not ligne_inutile(((x_ligne_debut, y_ligne_debut),(x_joueur, y_joueur + pas))):
                        
                        if premiere_direction is None:
                            
                            premiere_direction = 'Down'
                            
                        elif premiere_direction != 'Down':
                            
                            changement_de_direction()
                            premiere_direction ='Down'
                            
                        if sur_une_ligne(lignes_temporaires, x_joueur, y_joueur + pas):
                            
                            touche_une_ligne_temporaire()
                            
                        elif sur_une_ligne(lignes_tracees, x_joueur, y_joueur + pas):
                            
                            if len(lignes_temporaires) != 0:
                                lignes_temporaires.pop()
                            lignes_temporaires.append(((x_ligne_debut, y_ligne_debut),(x_joueur, y_joueur + pas)))
                            dessine_ligne(x_ligne_debut, y_ligne_debut, x_joueur, y_joueur + pas, numero_trace_temp)
                            
                            y_joueur += pas
                            
                            directions = directions_possibles('bas', x_joueur, y_joueur, lignes_tracees)
                            touche_une_ligne_tracee(directions)
                        
                        else:
                            
                            if len(lignes_temporaires) != 0:
                                lignes_temporaires.pop()
                            lignes_temporaires.append(((x_ligne_debut, y_ligne_debut), (x_joueur, y_joueur + pas)))
                            efface('ligne_temporaire_en_cours')
                            dessine_ligne(x_ligne_debut, y_ligne_debut, x_joueur, y_joueur + pas, 'ligne_temporaire_en_cours')
                            
                            y_joueur += pas
                        
                        joueur(x_joueur, y_joueur, rayon)
                    
                
                elif touche(evenement) == 'Left' and not est_dans_zone(x_joueur - pas, y_joueur) and not est_dans_obstacle(x_joueur - pas, y_joueur, liste_obstacles): # GAUCHE
                    
                    if not ligne_inutile(((x_ligne_debut, y_ligne_debut),(x_joueur - pas, y_joueur))):
                        
                        if premiere_direction is None:
                            
                            premiere_direction = 'Left'
                            
                        elif premiere_direction != 'Left':
                            
                            changement_de_direction()
                            premiere_direction ='Left'
                            
                        if sur_une_ligne(lignes_temporaires, x_joueur - pas, y_joueur):
                            
                            touche_une_ligne_temporaire()
                            
                        elif sur_une_ligne(lignes_tracees, x_joueur - pas, y_joueur):
                            
                            if len(lignes_temporaires) != 0:
                                lignes_temporaires.pop()
                            lignes_temporaires.append(((x_ligne_debut, y_ligne_debut),(x_joueur - pas, y_joueur)))
                            dessine_ligne(x_ligne_debut, y_ligne_debut, x_joueur - pas, y_joueur, numero_trace_temp)
                            
                            x_joueur -= pas
                            
                            directions = directions_possibles('gauche', x_joueur, y_joueur, lignes_tracees)
                            touche_une_ligne_tracee(directions)
                        
                        else:
                            
                            if len(lignes_temporaires) != 0:
                                lignes_temporaires.pop()
                            lignes_temporaires.append(((x_ligne_debut, y_ligne_debut), (x_joueur - pas, y_joueur)))
                            efface('ligne_temporaire_en_cours')
                            dessine_ligne(x_ligne_debut, y_ligne_debut, x_joueur - pas, y_joueur, 'ligne_temporaire_en_cours')
                            
                            x_joueur -= pas
                        
                        joueur(x_joueur, y_joueur, rayon)
                    
                
                elif touche(evenement) == 'Right' and not est_dans_zone(x_joueur + pas, y_joueur) and not est_dans_obstacle(x_joueur + pas, y_joueur, liste_obstacles): # DROITE
                    
                    if not ligne_inutile(((x_ligne_debut, y_ligne_debut),(x_joueur + pas, y_joueur))):
                        
                        if premiere_direction is None:
                            
                            premiere_direction = 'Right'
                            
                        elif premiere_direction != 'Right':
                            
                            changement_de_direction()
                            premiere_direction = 'Right'
                            
                        if sur_une_ligne(lignes_temporaires, x_joueur + pas, y_joueur):
                            
                            touche_une_ligne_temporaire()
                            
                        elif sur_une_ligne(lignes_tracees, x_joueur + pas, y_joueur):
                            
                            if len(lignes_temporaires) != 0:
                                lignes_temporaires.pop()
                            lignes_temporaires.append(((x_ligne_debut, y_ligne_debut),(x_joueur + pas, y_joueur)))
                            dessine_ligne(x_ligne_debut, y_ligne_debut, x_joueur + pas, y_joueur, numero_trace_temp)
                            
                            x_joueur += pas
                            
                            directions = directions_possibles('droite', x_joueur, y_joueur, lignes_tracees)
                            touche_une_ligne_tracee(directions)
                            
                        else:
                            
                            if len(lignes_temporaires) != 0:
                                lignes_temporaires.pop()
                            lignes_temporaires.append(((x_ligne_debut, y_ligne_debut), (x_joueur + pas, y_joueur)))
                            efface('ligne_temporaire_en_cours')
                            dessine_ligne(x_ligne_debut, y_ligne_debut, x_joueur + pas, y_joueur, 'ligne_temporaire_en_cours')
                            
                            x_joueur += pas
                        
                        joueur(x_joueur, y_joueur, rayon)
                
                #########################################
                ### AUTRES EVENEMENTS EN MODE TRACAGE ###
                #########################################
                    
                elif touche(evenement) == 'Return': # ANNULER LE MODE TRACAGE
                    
                    if sur_une_ligne(lignes_tracees, x_joueur, y_joueur):
                        mode = 'déplacement'
                        texte_mode_joueur(mode)
                        points_polygone = []
                    
                
        mise_a_jour()
        
    ferme_fenetre()