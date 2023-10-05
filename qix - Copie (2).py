from fltk import *

### FENETRE ###
largeur_fenetre = 400
hauteur_fenetre = 600

cree_fenetre(largeur_fenetre, hauteur_fenetre)

couleur_fenetre = "black"
couleur_elements = "white"

rectangle(0, 0, largeur_fenetre, hauteur_fenetre, remplissage=couleur_fenetre)

### TERRAIN ###
largeur_terrain = largeur_fenetre*0.9
hauteur_terrain = hauteur_fenetre*0.9

gauche_terrain = largeur_fenetre - largeur_terrain
haut_terrain = hauteur_fenetre - hauteur_terrain
droite_terrain = largeur_terrain
bas_terrain = hauteur_terrain

rectangle(gauche_terrain, haut_terrain, droite_terrain, bas_terrain, couleur=couleur_elements)

aire_restante = largeur_terrain * hauteur_terrain

### JOUEUR ###
rayon = 5
x_joueur = largeur_fenetre/2
y_joueur = hauteur_terrain
pas = 5
mode = 'déplacement'
vies = 3
numero_trace_temp = ''
perdu = False
points = 0
niveau = 1

# ON INITIALISE DANS LIGNES LES BORDS DU TERRAIN, LE JOUEUR NE POURRA SE DEPLACER QUE SUR CELLES-CI EN MODE DEPLACEMENT
lignes = [((gauche_terrain, haut_terrain),(droite_terrain, haut_terrain)), # HAUT
          ((gauche_terrain, bas_terrain),(droite_terrain, bas_terrain)), # BAS
          ((gauche_terrain, haut_terrain),(gauche_terrain, bas_terrain)), # GAUCHE
          ((droite_terrain, haut_terrain),(droite_terrain, bas_terrain)) # DROITE
          ]

lignes_temporaires = [] # LES LIGNES FAITES EN MODE TRACAGE

zones = [] # LES ZONES DU JOUEUR

### FONCTIONS AUXILIARES DE JEU ###

def joueur(x_joueur, y_joueur, rayon):
    '''
    Dessine le cercle représentant le joueur.
    '''
    cercle(x_joueur, y_joueur, rayon, couleur=couleur_elements, remplissage=couleur_elements, tag='joueur')

def texte_mode_joueur():
    '''
    Affiche le mode dans lequel est le joueur.
    '''
    texte(droite_terrain, hauteur_terrain + hauteur_fenetre*0.025, 'Mode : '+mode, taille=12, couleur=couleur_elements, ancrage='e', tag='mode_joueur')

def texte_niveau():
    '''
    Affiche le niveau du joueur.
    '''
    texte(droite_terrain, hauteur_terrain + hauteur_fenetre*0.075, 'Niveau : '+str(niveau), couleur=couleur_elements, taille=12, ancrage='e', tag='niveau')

def texte_points():
    '''
    Affiche les points du joueur.
    '''
    texte(gauche_terrain, hauteur_terrain + hauteur_fenetre*0.025, 'Points : '+str(points), couleur=couleur_elements, taille=12, ancrage='w', tag='points')

def texte_vies_restantes():
    '''
    Affiche les vies restantes du joueur.
    '''
    texte(gauche_terrain, hauteur_terrain + hauteur_fenetre*0.075, 'Vies restantes : '+str(vies)+' / 3', couleur=couleur_elements, taille=12, ancrage='w', tag='vies_restantes')

def touche_une_ligne_tracee():
    '''
    Quand le joueur touche une ligne tracée, met à jour le mode du joueur et passe les lignes de la liste lignes_temporaires dans la liste ligne.
    '''
    efface('mode_joueur')
    texte_mode_joueur()
    lignes.extend(lignes_temporaires)

def touche_une_ligne_temporaire():
    '''
    Quand le joueur touche une ligne temporaire, met à jour les vies restantes, le mode du joueur et efface les lignes temporaires.
    '''
    efface('vies_restantes')
    texte_vies_restantes()
    efface('mode_joueur')
    texte_mode_joueur()
    efface(numero_trace_temp)
    
def dessine_ligne(x_temp_debut, y_temp_debut, x_joueur, y_joueur, numero_trace_temp):
    '''
    Dessine la ligne temporaire quand elle est validée.
    '''
    ligne(x_temp_debut, y_temp_debut, x_joueur, y_joueur, couleur=couleur_elements, tag=numero_trace_temp)

def sur_une_ligne(type, haut, bas, gauche, droite):
    """
    Prend en paramètre le type de ligne ('tracee' ou 'temp') et le pas du mouvement à l'emplacement correspondant à
    la direction souhaitée, renvoie True si l'emplacement du joueur/qix/starx après le
    mouvement appartient à une ligne du type choisi, False sinon.
    """
    if type == 'tracee':
        type_ligne = lignes
    elif type == 'temporaire':
        type_ligne = lignes_temporaires
    x_souhaite = x_joueur - gauche + droite
    y_souhaite = y_joueur - haut + bas
    for ligne in type_ligne:
        if (x_souhaite >= ligne[0][0] and x_souhaite <= ligne[1][0] and y_souhaite >= ligne[0][1] and y_souhaite <= ligne[1][1]) or (x_souhaite <= ligne[0][0] and x_souhaite >= ligne[1][0] and y_souhaite <= ligne[0][1] and y_souhaite >= ligne[1][1]):
            return True
    return False
    
### INITIALISATIONS ###

texte_mode_joueur()
texte_niveau()
texte_points()
texte_vies_restantes()
texte(largeur_fenetre/2, haut_terrain/2, 'Qix par Nathanel & Andrei', couleur=couleur_elements, taille=18, ancrage='center')
joueur(x_joueur, y_joueur, rayon)

### BOUCLE DE JEU ###

if __name__ == '__main__':
    while True:
        evenement = donne_ev()
        type_evenement = type_ev(evenement)
        
        if type_evenement == 'Quitte': # QUITTER LE JEU
            break
        
        if vies == 0 and not perdu:
            texte(largeur_fenetre/2, hauteur_fenetre/2, 'Vous avez perdu !', couleur=couleur_elements, taille=24, ancrage='c', tag='perdu')
            efface('joueur')
            perdu = True

        if type_evenement == 'Touche' and not perdu: # ACTIONS DU JOUEUR
            
            if touche(evenement) == 'p': # TEST DEBUG
                print('x :', x_joueur, 'y :', y_joueur)
                print('lignes', lignes)
                print(len(lignes))
            
            if mode == 'déplacement': # SE DEPLACER SUR LES LIGNES EXISTANTES, VERIFIE QU'ON VEUILLE ALLER SUR UNE LIGNE
                
                
                if touche(evenement) == 'Up' and sur_une_ligne('tracee', pas/2, 0, 0, 0): # HAUT
                    efface('joueur')
                    y_joueur -= pas
                    joueur(x_joueur, y_joueur, rayon)
                    
                
                elif touche(evenement) == 'Down' and sur_une_ligne('tracee', 0, pas/2, 0, 0): # BAS
                    efface('joueur')
                    y_joueur += pas
                    joueur(x_joueur, y_joueur, rayon)
                    
                
                elif touche(evenement) == 'Left' and sur_une_ligne('tracee', 0, 0, pas/2, 0): # GAUCHE
                    efface('joueur')
                    x_joueur -= pas
                    joueur(x_joueur, y_joueur, rayon)
                    
                
                elif touche(evenement) == 'Right' and sur_une_ligne('tracee', 0, 0, 0, pas/2): # DROITE
                    efface('joueur')
                    x_joueur += pas
                    joueur(x_joueur, y_joueur, rayon)
                    
                
                elif touche(evenement) == 'Return': # PASSER EN MODE TRACAGE
                    mode = 'traçage'
                    efface('mode_joueur')
                    texte_mode_joueur()
                    x_temp_debut = x_joueur
                    y_temp_debut = y_joueur
                    premiere_touche = None # SERT A TRACER UNE LIGNE QUAND ON CHANGE DE DIRECTION
                    numero_trace_temp += '_'
                    
                
            elif mode == 'traçage': # CREER DE NOUVELLES LIGNES, VERIFIE QU'ON NE SORT PAS TU TERRAIN (ET QU'ON AVANCE PAS DANS SA ZONE), SI ON TOUCHE UNE LIGNE TRACEE, ON REPASSE EN MODE LIGNE, SINON ON TRACE UNE LIGNE TEMPORAIRE
                
                
                if touche(evenement) == 'Up':  # HAUT
                    
                    if premiere_touche is None:
                        premiere_touche = 'Up'
                        
                    elif premiere_touche != 'Up':
                        lignes_temporaires.append(((x_temp_debut, y_temp_debut),(x_joueur, y_joueur)))
                        dessine_ligne(x_temp_debut, y_temp_debut, x_joueur, y_joueur, numero_trace_temp)
                        x_temp_debut = x_joueur
                        y_temp_debut = y_joueur
                        premiere_touche ='Up'
                    
                    if sur_une_ligne('temporaire', pas, 0, 0, 0):
                        lignes_temporaires = []
                        x_joueur = largeur_fenetre/2
                        y_joueur = hauteur_terrain + pas
                        mode = 'déplacement'
                        vies -= 1
                        
                        touche_une_ligne_temporaire()
                    
                    elif sur_une_ligne('tracee', pas, 0, 0, 0):
                        lignes_temporaires.append(((x_temp_debut, y_temp_debut),(x_joueur, y_joueur - pas)))
                        dessine_ligne(x_temp_debut, y_temp_debut, x_joueur, y_joueur - pas, numero_trace_temp)
                        mode = 'déplacement'
                        touche_une_ligne_tracee()
                        lignes_temporaires = []
                        
                    efface('joueur')
                    y_joueur -= pas
                    joueur(x_joueur, y_joueur, rayon)
                    
                
                elif touche(evenement) == 'Down': # BAS
                    
                    if premiere_touche is None:
                        premiere_touche = 'Down'
                        
                    elif premiere_touche != 'Down':
                        lignes_temporaires.append(((x_temp_debut, y_temp_debut),(x_joueur, y_joueur)))
                        dessine_ligne(x_temp_debut, y_temp_debut, x_joueur, y_joueur, numero_trace_temp)
                        x_temp_debut = x_joueur
                        y_temp_debut = y_joueur
                        premiere_touche = 'Down'
                        
                    if sur_une_ligne('temporaire', 0, pas, 0, 0):
                        lignes_temporaires = []
                        x_joueur = largeur_fenetre/2
                        y_joueur = hauteur_terrain - pas
                        mode = 'déplacement'
                        vies -= 1
                        
                        touche_une_ligne_temporaire()
                        
                    elif sur_une_ligne('tracee', 0, pas, 0, 0): 
                        lignes_temporaires.append(((x_temp_debut, y_temp_debut),(x_joueur, y_joueur + pas)))
                        dessine_ligne(x_temp_debut, y_temp_debut, x_joueur, y_joueur + pas, numero_trace_temp)
                        mode = 'déplacement'
                        touche_une_ligne_tracee()
                        lignes_temporaires = []
                        
                    efface('joueur')
                    y_joueur += pas
                    joueur(x_joueur, y_joueur, rayon)
                    
                
                elif touche(evenement) == 'Left': # GAUCHE
                    
                    if premiere_touche is None:
                        premiere_touche = 'Left'
                        
                    elif premiere_touche != 'Left':
                        lignes_temporaires.append(((x_temp_debut, y_temp_debut),(x_joueur, y_joueur)))
                        dessine_ligne(x_temp_debut, y_temp_debut, x_joueur, y_joueur, numero_trace_temp)
                        x_temp_debut = x_joueur
                        y_temp_debut = y_joueur
                        premiere_touche = 'Left'
                        
                    if sur_une_ligne('temporaire', 0, 0, pas, 0):
                        lignes_temporaires = []
                        x_joueur = largeur_fenetre/2 + pas
                        y_joueur = hauteur_terrain
                        mode = 'déplacement'
                        vies -= 1
                        
                        touche_une_ligne_temporaire()
                        
                    elif sur_une_ligne('tracee', 0, 0, pas, 0):  
                        lignes_temporaires.append(((x_temp_debut, y_temp_debut),(x_joueur - pas, y_joueur)))
                        dessine_ligne(x_temp_debut, y_temp_debut, x_joueur - pas, y_joueur, numero_trace_temp)
                        mode = 'déplacement'
                        touche_une_ligne_tracee()
                        lignes_temporaires = []
                        
                    efface('joueur')
                    x_joueur -= pas
                    joueur(x_joueur, y_joueur, rayon)
                    
                
                elif touche(evenement) == 'Right': # DROITE
                    
                    if premiere_touche is None:
                        premiere_touche = 'Right'
                        
                    elif premiere_touche != 'Right':
                        lignes_temporaires.append(((x_temp_debut, y_temp_debut),(x_joueur, y_joueur)))
                        dessine_ligne(x_temp_debut, y_temp_debut, x_joueur, y_joueur, numero_trace_temp)
                        x_temp_debut = x_joueur
                        y_temp_debut = y_joueur
                        premiere_touche = 'Right'
                        
                    if sur_une_ligne('temporaire', 0, 0, 0, pas):
                        lignes_temporaires = []
                        x_joueur = largeur_fenetre/2 - pas
                        y_joueur = hauteur_terrain
                        mode = 'déplacement'
                        vies -= 1
                        
                        touche_une_ligne_temporaire()
                        
                    elif sur_une_ligne('tracee', 0, 0, 0, pas):    
                        lignes_temporaires.append(((x_temp_debut, y_temp_debut),(x_joueur + pas, y_joueur)))
                        dessine_ligne(x_temp_debut, y_temp_debut, x_joueur + pas, y_joueur, numero_trace_temp)
                        mode = 'déplacement'
                        touche_une_ligne_tracee()
                        lignes_temporaires = []
                        
                    efface('joueur')
                    x_joueur += pas
                    joueur(x_joueur, y_joueur, rayon)
                
                
        mise_a_jour()
        
    ferme_fenetre()