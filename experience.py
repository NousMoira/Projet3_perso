from quoridor import Quoridor

# Contexte initial
joueurs = [{'nom': 'William', 'murs': 5, 'position': [1, 1]}, {'nom': 'Richard', 'murs': 5, 'position': [5, 5]}]
murs = {'horizontaux': [[1, 3], [1, 6], [4, 3], [4, 6], [7, 3]], 'verticaux': [[2, 4], [3, 4], [4, 4], [5, 4], [6, 1]]}
joueur = 'William'

# Création de l'instance Quoridor
quoridor = Quoridor(joueurs, murs)

# Afficher l'état initial du jeu
print("État initial du jeu :")
print(quoridor)

# Appeler la méthode jouer_un_coup
coup, position = quoridor.jouer_un_coup(joueur)
print(f"\nCoup joué par {joueur} : {coup}, Position : {position}")

# Afficher l'état du jeu après le coup
print("\nÉtat du jeu après le coup :")
print(quoridor)

