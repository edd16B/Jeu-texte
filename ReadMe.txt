Projet de Jeu en Python avec curses

Ce projet consiste en un jeu simple en mode console réalisé en Python à l'aide de la bibliothèque curses. Le jeu est une sorte de labyrinthe où le joueur doit éviter des monstres, collecter des objets et atteindre la sortie.

Instructions pour l'exécution :

Assurez-vous d'avoir Python installé sur votre machine. Vous pouvez exécuter le jeu en utilisant la commande suivante :
python start.py

Assurez-vous également d'avoir la bibliothèque curses installée. Vous pouvez l'installer en utilisant la commande suivante :
pip install windows-curses

Contrôles du Jeu :

- Z : Déplacement vers le haut
- S : Déplacement vers le bas
- Q : Déplacement vers la gauche
- D : Déplacement vers la droite

Appuyez sur la barre d'espace (Ou n'importe quel touche) pour commencer le jeu.
A tout moment du jeu, Appuyez sur "P" pour déclarer forfait et quitter !

Fonctionnalités du Jeu :

- Génération aléatoire de la carte avec des murs, une entrée, et une sortie.
- Déplacement du personnage avec des contrôles simples.
- Apparition automatique d'objets à collecter.
- Présence de monstres qui se déplacent automatiquement.
- Niveaux qui deviennent plus difficiles à mesure que le joueur progresse.

Objectif du Jeu :

Le joueur doit collecter tous les objets et atteindre la sortie sans se faire attraper par les monstres. Chaque niveau augmente la difficulté en ajoutant plus d'objets puis, plus de monstres pour chaque 3 niveaux passés augmentant aussi leur vitesse.

Notes Techniques :

Le code utilise la bibliothèque curses pour l'interface utilisateur en mode console. Les couleurs sont utilisées pour rendre l'affichage plus attrayant. Le jeu inclut également des fonctionnalités de génération de carte, de vérification de l'accessibilité, et de déplacement automatique des monstres.

Licence :

Ce projet est distribué sous la licence MIT.

Auteur : Eddy BEDI |&| Annie TRUONG