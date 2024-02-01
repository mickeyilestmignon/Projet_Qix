"""Module qui contient toutes les variables et initialisations"""
from random import randrange

###############
### FENETRE ###
###############

config = open('config.txt', 'r')

#Dimension de la fenetre-----------------------------------------------------------

largeur_fenetre = int(config.readline().strip())
hauteur_fenetre = int(config.readline().strip())

###############
### COULEUR ###
###############

#Couleur des objets-----------------------------------------------------------------
couleur_fenetre = config.readline().strip()
couleur_elements = config.readline().strip()
couleur_zones = config.readline().strip()

###############
### TERRAIN ###
###############

#Dimensions du terrain--------------------------------------------------------------
largeur_terrain = largeur_fenetre*0.8
hauteur_terrain = hauteur_fenetre*0.8


gauche_terrain = int(largeur_fenetre - largeur_fenetre*0.9)
haut_terrain = int(hauteur_fenetre - hauteur_fenetre*0.9)
droite_terrain = int(largeur_fenetre*0.9)
bas_terrain = int(hauteur_fenetre*0.9)

nombre_obstacles = 3
taille_obstacle = 60
liste_obstacles = [] # Les obstacles sont des carrés de taille_obstacle*taille_obstacle pixels, ils sont représentés par les coordonnées de leur coin supérieur gauche.
    
nombre_pommes = 3
liste_pommes = [] # Les pommes sont des points, elles sont représentées par leurs coordonnées.

###############
### Vitesse ###
###############


#Vitesse par défaut du joueur----------------------------------------
pas = int(config.readline().strip())
diviseur_difficulte = pas
cpt_ticks = 0
vitesse = int(config.readline().strip())

assert largeur_terrain % pas == 0 and hauteur_terrain % pas == 0, print('La largeur et la hauteur du terrain ne sont pas divisibles par le pas !')
assert pas % 2 == 0, print('Le pas doit être pair !')

################
#### JOUEUR ####
################


rayon = pas
x_joueur = largeur_fenetre/2
y_joueur = bas_terrain
mode = 'déplacement'
zones_joueur = []
invincible = False
timer_invincible = 0

################
#### OPTION ####
################

vies = int(config.readline().strip())
zone_conquise = 0
points = 0
niveau = 1

config.close()

###############
##### QIX #####
###############

x_qix = largeur_fenetre//2
y_qix = hauteur_fenetre//2

taille_qix = pas*8 # Uniquement la taille affichée
a_trajectoire = True
pas_qix_x = randrange(-pas, 2*pas, pas)
pas_qix_y = randrange(-pas, 2*pas, pas)
longueur_trajectoire = randrange(10, 31)
trajectoire_parcourue = 0


#############
### SPARX ###
#############

x_sparx_1 = largeur_fenetre//2
y_sparx_1 = haut_terrain
pas_sparx_1_x = -2
pas_sparx_1_y = 0
direction_sparx_1 = 'gauche'
mouvements_sparx_1 = []

x_sparx_2 = largeur_fenetre//2
y_sparx_2 = haut_terrain
pas_sparx_2_x = 2
pas_sparx_2_y = 0
direction_sparx_2 = 'droite'
mouvements_sparx_2 = []

taille_sparx = pas*8

##############
### LIGNES ###
##############

#Cadre dans lequel évolueront joueur, Qix et Sparx-------------------------------------------------------------------------------------

lignes_tracees = [ # ON INITIALISE DANS LES LIGNES TRACEES LES BORDS DU TERRAIN. LE JOUEUR NE POURRA SE DEPLACER QUE SUR CELLES-CI EN MODE DEPLACEMENT
                ((gauche_terrain, haut_terrain),(droite_terrain, haut_terrain)), # HAUT
                ((gauche_terrain, bas_terrain),(droite_terrain, bas_terrain)), # BAS
                ((gauche_terrain, haut_terrain),(gauche_terrain, bas_terrain)), # GAUCHE
                ((droite_terrain, haut_terrain),(droite_terrain, bas_terrain)) # DROITE
          ]

#Lignes qui seront tracée par le joueur tant que sa figure n'est pas fermé--------------------------------------------------------------
lignes_temporaires = [] # LES LIGNES FAITES EN MODE TRACAGE

#tag de ligne temporaires qui permet d'effacer le numero du tracer temporaire-----------------------------------------------------------
numero_trace_temp = '' 

#Contient tout les points tracé par le joueur sans que l'on compléte par la partie du cadre manquante-----------------------------------
points_polygone = [] 

#Contient tout les points tracée par le joueur, complété par les partie du cadre qui permette d'avoir un polygone-----------------------
points_polygone_ferme = [] # Optimisable




