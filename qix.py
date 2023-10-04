from fltk import *

### FENETRE ###
largeur_fenetre = 600
hauteur_fenetre = 600

cree_fenetre(largeur_fenetre, hauteur_fenetre)

### TERRAIN ###
largeur_terrain = largeur_fenetre*0.9
hauteur_terrain = hauteur_fenetre*0.9

gauche_terrain = largeur_fenetre - largeur_terrain
haut_terrain = hauteur_fenetre - hauteur_terrain
droite_terrain = largeur_terrain
bas_terrain = hauteur_terrain

rectangle(gauche_terrain, haut_terrain, droite_terrain, bas_terrain)

aire_restante = largeur_terrain * hauteur_terrain

### JOUEUR ###
rayon = 5
x_joueur = largeur_fenetre/2
y_joueur = hauteur_terrain
pas = 5
mode = 'ligne'

lignes = [((gauche_terrain, haut_terrain),(droite_terrain, haut_terrain)), # HAUT
          ((gauche_terrain, bas_terrain),(droite_terrain, bas_terrain)), # BAS
          ((gauche_terrain, haut_terrain),(gauche_terrain, bas_terrain)), # GAUCHE
          ((droite_terrain, haut_terrain),(droite_terrain, bas_terrain)) # DROITE
          ]

lignes_temp = [] # LES LIGNES FAITES EN MODE TRACAGE

### FONCTIONS JEU ###

def joueur(x_joueur, y_joueur, rayon):
    cercle(x_joueur, y_joueur, rayon, remplissage='black', tag='joueur')

def texte_mode_joueur():
    texte(droite_terrain, hauteur_terrain + hauteur_fenetre*0.05, 'Mode = '+mode, taille=12, ancrage='e', tag='mode_joueur')

def texte_aire_comblee():
    texte(gauche_terrain, hauteur_terrain + hauteur_fenetre*0.05, 'Aire comblée = 0 % / 75 %', taille=12, ancrage='w', tag='aire_comblee')

### FONCTIONS VERIFICATION DEPLACEMENT ###

def sur_une_ligne(haut, bas, gauche, droite):
    """
    Prend en paramètre le pas du mouvement à l'emplacement correspondant à
    la direction souhaitée, renvoie True si l'emplacement du joueur après le
    mouvement appartient à une ligne tracée, False sinon.
    """
    x_souhaite = x_joueur - gauche + droite
    y_souhaite = y_joueur - haut + bas
    for ligne in lignes:
        if x_souhaite >= ligne[0][0] and x_souhaite <= ligne[1][0] and y_souhaite >= ligne[0][1] and y_souhaite <= ligne[1][1]:
            return True
    return False

### FONCTIONS SPARX ###

### FONCTIONS QIX ###

### FONCTIONS COLLISIONS ###
    
### INITIALISATIONS ###

texte_mode_joueur()
texte_aire_comblee()
texte(largeur_fenetre/2, haut_terrain/2, 'Qix par Nathanel & Andrei', taille=18, ancrage='center')
joueur(x_joueur, y_joueur, rayon)

### BOUCLE DE JEU ###

if __name__ == '__main__':
    while True:
        evenement = donne_ev()
        type_evenement = type_ev(evenement)
        
        if type_evenement == 'Quitte':
            ferme_fenetre()

        if type_evenement == 'Touche':
            if mode == 'ligne': # SE DEPLACER SUR LES LIGNES EXISTANTES
                
                if touche(evenement) == 'Up' and y_joueur + rayon/2 > haut_terrain and sur_une_ligne(pas, 0, 0, 0): # VERIFIE QU'ON NE DEPASSE PAS LE TERRAIN ET QU'OJ VEUILLE ALLER SUR UNE LIGNE
                    efface('joueur')
                    y_joueur -= pas
                    joueur(x_joueur, y_joueur, rayon)
                
                elif touche(evenement) == 'Down' and y_joueur < bas_terrain - rayon/2 and sur_une_ligne(0, pas, 0, 0):
                    efface('joueur')
                    y_joueur += pas
                    joueur(x_joueur, y_joueur, rayon)
                
                elif touche(evenement) == 'Left' and x_joueur + rayon/2 > gauche_terrain and sur_une_ligne(0, 0, pas, 0):
                    efface('joueur')
                    x_joueur -= pas
                    joueur(x_joueur, y_joueur, rayon)
                
                elif touche(evenement) == 'Right' and x_joueur < bas_terrain - rayon/2 and sur_une_ligne(0, 0, 0, pas):
                    efface('joueur')
                    x_joueur += pas
                    joueur(x_joueur, y_joueur, rayon)
                
                elif touche(evenement) == 'Return': # PASSER EN MODE TRACAGE
                    mode = 'traçage'
                    efface('mode_joueur')
                    texte_mode_joueur()
                
            elif mode == 'traçage': # CREER DE NOUVELLES LIGNES
                
                if touche(evenement) == 'Up' and y_joueur + rayon/2 > haut_terrain:
                    
                    if sur_une_ligne(pas, 0, 0, 0): # ON TOUCHE UNE LIGNE DEJA FAITE, REPASSER EN MODE LIGNE ET VALIDER LES LIGNES TEMPORAIRES
                        mode = 'ligne'
                        efface('mode_joueur')
                        texte_mode_joueur()
                    else:
                        pass # ON EST DANS LE BLANC, TRACER LIGNE TEMPORAIRE
                    efface('joueur')
                    y_joueur -= pas
                    joueur(x_joueur, y_joueur, rayon)
                
                elif touche(evenement) == 'Down' and y_joueur < bas_terrain - rayon/2:
                    if sur_une_ligne(0, pas, 0, 0):
                        mode = 'ligne'
                        efface('mode_joueur')
                        texte_mode_joueur()
                    else:
                        pass
                    efface('joueur')
                    y_joueur += pas
                    joueur(x_joueur, y_joueur, rayon)
                
                elif touche(evenement) == 'Left' and x_joueur + rayon/2 > gauche_terrain:
                    if sur_une_ligne(0, 0, pas, 0):
                        mode = 'ligne'
                        efface('mode_joueur')
                        texte_mode_joueur()
                    else:
                        pass
                    efface('joueur')
                    x_joueur -= pas
                    joueur(x_joueur, y_joueur, rayon)
                
                elif touche(evenement) == 'Right' and x_joueur < bas_terrain - rayon/2:
                    if sur_une_ligne(0, 0, 0, pas):
                        mode = 'ligne'
                        efface('mode_joueur')
                        texte_mode_joueur()
                    else:
                        pass
                    efface('joueur')
                    x_joueur += pas
                    joueur(x_joueur, y_joueur, rayon)
                
        mise_a_jour()
        
    ferme_fenetre()