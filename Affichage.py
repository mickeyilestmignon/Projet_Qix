from fltk import *
from Variables import *


"""Module qui contient toutes les fonctions qui ont pour objectifs d'afficher du texte ou un objet"""


def joueur(x_joueur, y_joueur, rayon):
    '''
    Dessine le cercle représentant le joueur. Prend en argument les coordonnées de départ (x,y)
    ainsi que le rayon'''
    efface('joueur')
    cercle(x_joueur, y_joueur, rayon, couleur='black', remplissage=couleur_elements, tag='joueur')
    
def qix(x_qix, y_qix):
    '''
    Affiche le dessin représentant le qix. Prend en argument x et y, les coordonnées du qix
    '''
    efface('qix')
    image(x_qix, y_qix, 'qix.png', largeur=taille_qix, hauteur=taille_qix, ancrage='center', tag='qix')
    
def sparx_1(x_sparx_1, y_sparx_1):
    """
    Affiche le dessin représentant le 1er sparx. Prend en argument x_sparx_1 et y_sparx_1, les coordonnées du 1er sparx
    """
    efface('sparx_1')
    image(x_sparx_1, y_sparx_1, 'sparx.png', largeur=taille_sparx, hauteur=taille_sparx, ancrage='center', tag='sparx_1')
    
def sparx_2(x_sparx_2, y_sparx_2):
    """
    Affiche le dessin représentant le 2eme sparx. Prend en argument x_sparx_2 et y_sparx_2, les coordonnées du 2eme sparx
    """
    efface('sparx_2')
    image(x_sparx_2, y_sparx_2, 'sparx.png', largeur=taille_sparx, hauteur=taille_sparx, ancrage='center', tag='sparx_2')

def texte_mode_joueur(mode):
    '''
    Affiche le mode dans lequel est le joueur.
    '''
    efface('mode_joueur')
    texte(droite_terrain, hauteur_fenetre*0.925, 'Mode : '+mode, taille=12, couleur=couleur_elements, ancrage='e', tag='mode_joueur')
    
def texte_vies_joueur(vies):
    """
    Affiche le nombre de vies du joueur
    """
    efface('vies_joueur')
    texte(droite_terrain, hauteur_fenetre*0.95, 'Vies : '+str(vies), taille=12, couleur=couleur_elements, ancrage='e', tag='vies_joueur')
    
def texte_vitesse_joueur(vitesse):
    """
    """
    efface('vitesse')
    if vitesse == 1:
        texte(droite_terrain, hauteur_fenetre*0.975, 'Vitesse : rapide', taille=12, couleur=couleur_elements, ancrage='e', tag='vitesse')
    else:
        texte(droite_terrain, hauteur_fenetre*0.975, 'Vitesse : lente', taille=12, couleur=couleur_elements, ancrage='e', tag='vitesse')
    
def texte_niveau(niveau):
    """
    Affiche le niveau du joueur
    """
    efface('niveau')
    texte(gauche_terrain, hauteur_fenetre*0.925, 'Niveau : '+str(niveau), taille=12, couleur=couleur_elements, ancrage='w', tag='niveau')

def texte_zone_conquise(zone_conquise):
    """
    Affiche le pourcentage du terrain conquis par le joueur
    """
    efface('zone_conquise')
    texte(gauche_terrain, hauteur_fenetre*0.95, str(round((zone_conquise*100)/(largeur_terrain*hauteur_terrain), 2))+' %', taille=12, couleur=couleur_elements, ancrage='w', tag='zone_conquise')

def texte_points(points):
    """
    Affiche les points du joueur
    """
    efface('points')
    texte(gauche_terrain, hauteur_fenetre*0.975, 'Points : '+str(points), taille=12, couleur=couleur_elements, ancrage='w', tag='points')
    
def dessine_ligne(x_ligne_debut, y_ligne_debut, x_joueur, y_joueur, type_tag):
    '''
    Prend en paramètre des positions et dessine la ligne correspondante avec son tag.
    '''
    ligne(x_ligne_debut, y_ligne_debut, x_joueur, y_joueur, couleur=couleur_elements, tag=(type_tag, 'lignes_dessines'))
