Qix par Nathanel Erik et Andrei-Ionut Achirecesei

Lancer qix.py pour jouer.

### PREMIER RENDU ###

Lancer le fichier qix.py en faisant attention à ce que tous les modules et images soient dans le même répertoire.

Commandes:
	- Flèches pour se déplacer
	- Entrée pour changer de mode
	- P pour afficher les informations sur les variables de jeu et pour se rendre invincible

1) Organisation du programme

Le programme est divisé en trois parties séparées en différents modules:
	a) Une partie avec les initialisations des variables globales, variables.py
	b) Une partie avec les fonctions d’affichage des textes et des dessins, affichage.py
	c) Une partie avec la boucle de jeu et les fonctions auxiliaires de jeu, qix.py

2) Hypothèses considérées et choix techniques

a) Normes utilisées

La zone de jeu est centrée et remplit 80% de la fenêtre. Par défault, la fenêtre a une largeur de 400 pixels et une hauteur de 600 pixels. Cette taille est modifiable, la zone de jeu s'adaptera automatiquement à celle-ci.

Le pas correspond à l'unité de déplacement des entités du jeu (joueur, sparx, qix). Par défault, nous avons choisi un pas de 4 car c'est un nombre pair, afin de nous faciliter certains aspects, et parceque la largeur et la hauteur du terrain doivent être divisible par le pas. Le pas est modifiable à condition de respecter ces contraintes.

Les couleurs utilisées dans le programme (fenêtre, lignes, zones) sont définies dans la partie a), elles sont modifiables à conditions qu'elles soient reconnues par fltk.

Le joueur est caractérisé par ses coordonnées x_joueur et _joueur, la fonction joueur représente le joueur par un cercle d'un rayon de pas, de même pour le qix (x_qix, y_qix) et les deux sparx (x_sparx_1, y_sparx_1, x_sparx_2, y_sparx_2).

Les lignes sont sépararées en deux catégories : Les lignes tracées et les lignes temporaires.

Toutes les lignes sont représentées d'une façon standardisée : un tuple constitué de deux tuples, eux mêmes constitués des coordonnées x et y. Exemple : ((1, 2), (3, 2))

Les lignes tracées sont les lignes sur lesquelles le joueur peut se déplacer et sur lesquelles le qix rebondit, elles sont plus déssinées plus épaisses que les autres.

Les lignes temporaires sont les lignes que le joueur fait en mode traçage, elles servent à detecter quand le joueur perd une vie, après s'être fait une auto-intersection ou après s'être fait toucher par le qix.

b) Explication du fonctionnement global du jeu

Le joueur alterne entre deux modes : en appuyant sur entrée quand il est en mode déplacement, il passe en mode traçage (à noter que le joueur peut revenir en mode déplacement quand il est en mode traçage en appuyant sur entrée, à condition qu'il n'ai pas encore fait de mouvement. Cela sert à éviter qu'il se bloque dans un coin de la zone par exemple). Quand le joueur touche une ligne tracée quand il est en mode traçage, il repasse en mode déplacement.

Quand le joueur est en mode traçage, il enregistre dans la variable points_polygone ses coordonées quand il appuye sur entrée, quand il change de direction, ainsi que quand il touche une ligne tracée. Ces points serviront à colorier la zone adéquate, qui ne contient pas le qix.

Quand le joueur touche une ligne tracée en mode traçage, le programme appelle la fonction touche_une_ligne_tracee, qui prend en paramètre les directions qu'il est possible de prendre à partir de là, sans faire demi-tour, grâce à la fonction directions_possibles. Ces directions serviront à trouver les deux zones possibles. Tout d'abord, afin d'ajouter à points_polygone les points qui serviront à fermer la zone, on utilise la fonction ferme_la_zone, qui, en partant d'une certaine direction initiale (dans la variable direction) va suivre les lignes tracées, enregistrer les points où il y a un changement de direction et les renvoyer quand elle arrive au point de départ (le point au moment où le joueur passe en mode traçage). Ensuite, afin de choisir la zone à colorier (celle où il n'y a pas le qix), on utilise la fonction point_dans_zone, qui prend en paramètre une liste de lignes, dans ce cas, les points de notre polygone qu'on aura transformé en lignes grâce la fonction points_en_ligne, ansi que des coordonées x et y, qui correspondent ici au coordonnées du qix (x_qix et y_qix), La fonction renvoie True si le point est dans la zone, False sinon. Son fonctionnement n'est pas parfait, voir plus d'explications dans la partie dédiée au problèmes rencontrés. Si le qix se trouve dans cette zone, on rappelle la fonction ferme_la_zone mais en partant cette fois-ci de la deuxième direction possible. Une fois qu'on a trouvé la bonne zone, on utilise l'ensemble des points pour colorier la zone, grâce à la fonction polygone de fltk.

La fonction point_dans_zone sert également à s'assurer que le joueur ne se déplace pas dans ses zones quand il est en mode traçage.

Une fois qu'on a colorié la bonne zone, il faut changer les lignes tracées afin de ne plus y inclure les lignes englouties dans la zone. Pour cela, on appelle la fonction nouvelles_lignes_tracees qui prend en paramètre une liste de lignes à enlever, appelée lignes_interdites, qu'on aura récupéré précédement. La fonction va d'abord enlever les lignes de lignes_tracees se trouvant entièrement dans lignes_interdites, en faisant attention aux lignes identiques dans un sens différent (voir problèmes rencontrés), puis va modifier les lignes qui doivent être fractionnées, en les parcourant point par point et en vérifiant si le point appartient à une ligne interdite.

Le qix est représenté par le point de son centre (x_qix, y_qix) et possède une hitbox, qui est constituée des huit points qui entoure son centre, on utilise la hitbox pour vérifier si il touche une ligne temporaire du joueur, afin de lui faire perde une vie. Les déplacements du qix sont définis par une direction choisie aléatoirement et une distance à parcourir également choisie aléatoirement. Le qix peut se déplacer de neuf façons différentes (entre -2, 0 et 2 sur l'axe x, de même sur l'axe y). On tire aléatoirement une distance (entre 10 et 30 par défault), quand le qix aura fini de parcourir cette disatance, on retire une nouvelle direction. Si le qix rencontre une ligne tracée avant d'avoir fini sa distance à parcourir, on retire une direction prématurément.

Les sparx sont conçus pour se déplacer sur les lignes tracées, lorsqu'ils souhaitent avancer dans une direction, il regardent si le point devant eux appartient à une ligne tracée, si oui, ils avancent, sinon il cherchent dans quelle autre direction ils peuvent aller, sans faire demi-tour, grâce à la fonciton directions_possibles. Dans le cas où le point-même du sparx ne se situe pas sur une ligne tracée, cela signifie qu'il a été englouti dans une zone du joueur, dans ce cas, on effectue les derniers mouvements que le sparx a fait dans l'ordre inverse, jusqu'à ce qu'il retombe sur une ligne tracée. Ces mouvements sont enregistrés dans la liste mouvements_sparx_1/2 à chaque tour de boucle. Si la position du sparx est égale à celle du joueur, cela signifie qu'il l'a touché, donc on enlève une vie au joueur.

c) Variante implémentée

Nous avons ajouté l'affichage des textes de jeu, avec le calcul du pourcentage de la zone conquise par le joueur, les points et le niveau qui passe automatiquement au suivant lorsque le joueur atteint 75 % de remplissage. Au niveau suivant, les sparx deviennent deux fois plus rapides (la difficulté s'arrête d'augmenter après le niveau 3).

3) Problèmes rencontrés

Au cours du processus de réfléxion et de développement, nous avons rencontrés divers problèmes :

Tout d'abord, l'un des premiers problèmes que nous avons eu est avec la fonction sur_une_ligne, comme vous pouvez le constater, elle effectue deux fois la même vérification pour savoir si un point est sur une ligne, simplement en inversant les points. Cela est dû au fait que une ligne ne commence pas toujours par son minimum pour finir par son maximum, en fonction de la manière dont elle a été tracée par le joueur. Ainsi, un point (0, 2) appartient à la ligne ((0, 1), (0, 3)) car 2 est plus grand que 1 et plus petit que 3, mais n'appartient pas à la ligne ((0, 3), (0, 1)) car 2 est n'est pas plus grand que 3 et n'est pas plus petit que 1 même si il s'agit techniquement de la même ligne, c'est pour cela qu'on utilise un OR, afin de tester si le point appratient à la même lignes mais dans l'ordre inverse. Note : on aurrait pu tester si le point appartient au range de la ligne, mais cela aurait été souvent moins efficace.

Ensuite, les fonctions qui ont été les plus dures à programmer ont été ferme_la_zone et nouvelles_lignes_tracees. Le principe de ferme_la_zone est d'ajouter récursivement les points nécéssaires à la fermeture du polygone à colorier. La fonction parcoure les lignes tracées en enregistrant les points aux changements de directions, et s'arrête une fois qu'elle arrive au point de départ de la nouvelle ligne faite par le joueur. Nous avions eu plusieurs hypothèses pour cette fonction, comme une fonction propager qui aurait ajouté récursivement les zones de pas*pas, à la manière d'une sorte d'innonation, cela s'est presque avéré fonctionnel mais on s'est rendus compte que le nombre de calculs à faire était très grand, et ralentissait donc considérablement le jeu, en plus de toujours avoir de nombreux bugs. Il arrive que la fonction ferme_la_zone plante occasionellement, on ne sait pas trop pourquoi.

Nous avons également remarqué que la limite de récursion maximale de python (1000 par défaut) était trop courte pour la fonction ferme_la_zone, nous l'avons donc augmenté à 10000 en utilisant la fonction setrecursionlimit de la bibliothèque sys.

Enfin, l'une des dernières fonctions à nous avoir posé problème est la fonction point_dans_lignes. En effet, nous sommes passés par de nombreuses version qui avaient toutes un cas de figure où elle ne marchaient pas. Le principe est pourtant simple : on part de la droite du point rentré en paramètre et on compte combien d'intersections on touche, en faisant attention à ne pas toucher plusieurs fois les lignes horizontales. Le problème est que dans certains cas qui sont durs à comprendre, la fonction peut se tromper et soit, empêcher le joueur d'avancer dans une zone vide, ou l'autoriser à aller dans une zone coloriée. Dans la majorité des cas, la fonction fonctionne tout de même.

### SECOND RENDU ###

Pour ce rendu, nous n'avons pas pu terminer toutes, les variantes, nous avons uniquement les 4 premières.

Nous avions déjà fini le calcul du score, mais cette fois-ci, le score de se réinitialise pas quand on passe un niveau. De plus, nous avons ajouté la possibilité de passer en vitesse lente afin de gagner deux fois plus de points.

Nous avons passé beaucoup de temps avant de trouver la meilleure méthode pour ralentir le joueur, nous avons utilisé une variable cpt_ticks qui s'incrémente d'un à chaque tour de la boucle principale. Enfin nous avons placé une condition sur l'évenement touche qui est vraie uniquement quand cpt_ticks est divisible par la variable vitesse (1 pour rapide et 2 pour lent). Cette methode est celle qui respecte le mieux la consigne puisqu'elle ne ralentit pas l'intégralité du jeu, mais procure un effet saccadé. Nous n'avons pas trouvé de meilleure solution.

Nous avons contourné le problème que nous avions avec la fonction point_dans_lignes, en stockant les points qui se situent dans une zone coloriée par le joueur dans une liste, et en empêchant celui-ci de se trouver sur un de ces points. Cette solution est loin d'être la plus efficace, une matrice pourrait résoudre ce problème en temps constant, mais non n'avons pas réussi à la mettre en place.

Nous avons ajouté des obstacles sur l'aire de jeu, que le joueur ne peut pas traverser, ces obstacles sont des carrés tous de la même taille, et sont stockés dans liste_obstacles, ils sont représentés par les coordonnées de leur coin en haut à gauche. A noter que le qix peut toujours traverser ces obstacles, sinon le jeu aurait été plus facile. Ces obstacles deviennent de plus en plus nombreux au fur et a mesure des niveaux (maximum à 8).

Enfin, nous avons ajouté des pommes sur le terrain, quand le joueur en touche une, il devient invincible pendant 3 secondes, pour s'y faire nous avons utilisé la fonction time afin de chronometrer le temps et de l'afficher en haut de l'aire de jeu. Les pommes sont stockées dans liste_pommes et sont représentées par le couple de leurs coordonnées. Le niveau 1 commence avec 3 pommes, et une en moins à chaque niveau, il n'y en a plus à partir du niveau 4.
Afin que nous puissons effacer la bonne pomme quand le joueur en touche une, nous avons donné à leurs dessins un tag de type pomme_i où i est leur indice dans liste_pommes, cela facilite grandement leur suppression mais pour cela on ne doit pas modifier la taille de la liste en cours de jeu, au risque d'une index error. Quand une pomme est effacée, elle est changée en (None, None) pour éviter l'erreur.

Problèmes connus : 
- Quand les sparx sont à leur vitesse maximale, ils passent à travers les zones d'un pas de large ou de longeur.
- Quelques erreurs de remplissage, assez rares.
- Des fois, des pommes sont affichées mais elle n'existent pas.

### TROISIEME RENDU ###

J'ai ajouté la possibilité de charger un fichier contenant le nombre d'obstacles et leurs coordonnées. Pour utiliser les obstacles manuels, il suffit de mettre la première ligne du fichier obstacles.txt à 'True', pour la deuxième ligne, mettre la taille des obstacles, et pour le reste de lignes, préciser les coordonnées des obstacles de cette manière 'x y', par exemple :

True
60
100 100
200 200
250 180

A savoir que les obstacles ne fonctionneront que si ils rentrent dans l'aire de jeu, dans le cas où un obstacle ne respecte pas cette règle, le jeu fonctionnera normalement sans l'obstacle en question.

La même fonctionnalité existe également pour les pommes, avec le fichier pommes.txt, le fonctionnement est exactement le même sauf que les positions des pommes commencent à la deuxième ligne car il n'y a pas de taille à définir. On vérifie également que la pomme ne soit pas dans un obstacle pour l'afficher. Exemple:

True
127 294
66 89

Enfin, j'ai ajouté un fichier config.txt qui permet de configurer les principales variables du jeu, le fichier se présente tel :

largeur_fenetre
hauteur_fenetre
couleur_fenetre
couleur_elements
couleur_zones
pas
vitesse
vies

Exemple pour la configuration de base :

400
600
#000000
#FFFFFF
#027F7E
4
1
3
