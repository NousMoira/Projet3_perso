"""Module de la classe Quoridor

Classes:
    * Quoridor - Classe pour encapsuler le jeu Quoridor.
    * interpréter_la_ligne_de_commande - Génère un interpréteur de commande.
"""

import argparse
from copy import deepcopy

import networkx as nx

from quoridor_error import QuoridorError
from graphe import construire_graphe


class Quoridor:
    """Classe pour encapsuler le jeu Quoridor.

    Vous ne devez pas créer d'autre attributs pour votre classe.

    Attributes:
        joueurs (List): Un itérable de deux dictionnaires joueurs
            dont le premier est toujours celui qui débute la partie.
        murs (Dict): Un dictionnaire contenant une clé 'horizontaux' associée à
            la liste des positions [x, y] des murs horizontaux, et une clé 'verticaux'
            associée à la liste des positions [x, y] des murs verticaux.
        tour (int): Un entier positif représentant le tour du jeu (1 pour le premier tour).
    """

    def __init__(self, joueurs, murs=None, tour=1):
        """Constructeur de la classe Quoridor.

        Initialise une partie de Quoridor avec les joueurs, les murs et le tour spécifiés,
        en s'assurant de faire une copie profonde de tout ce qui a besoin d'être copié.

        Cette méthode ne devrait pas être modifiée.

        Args:
            joueurs (List): un itérable de deux dictionnaires joueurs
                dont le premier est toujours celui qui débute la partie.
            murs (Dict, optionnel): Un dictionnaire contenant une clé 'horizontaux' associée à
                la liste des positions [x, y] des murs horizontaux, et une clé 'verticaux'
                associée à la liste des positions [x, y] des murs verticaux.
            tour (int, optionnel): Un entier positif représentant le tour du jeu
            (1 pour le premier tour).
        """
        self.tour = tour
        self.joueurs = deepcopy(joueurs)
        self.murs = deepcopy(murs or {"horizontaux": [], "verticaux": []})

    def état_partie(self):
        """Produire l'état actuel du jeu.

        Cette méthode ne doit pas être modifiée.

        Returns:
            Dict: Une copie de l'état actuel du jeu sous la forme d'un dictionnaire.
                  Notez que les positions doivent être sous forme de liste [x, y] uniquement.
        """
        return deepcopy(
            {
                "tour": self.tour,
                "joueurs": self.joueurs,
                "murs": self.murs,
            }
        )

    def formater_entête(self):
        """Formater la représentation graphique de la légende.

        Returns:
            str: Chaîne de caractères représentant la légende.
        """
        légende = "Légende:\n"
        largeur_nom = max(len(joueur['nom']) for joueur in self.joueurs)
        for index, joueur in enumerate( self.joueurs):
            numéro = index + 1
            légende += (
            f"   {numéro}={joueur['nom'] + ',':<{largeur_nom + 1}} "
            f"murs={'|' * joueur['murs']}\n"
        )
        return légende


    def formater_le_damier(self):
        """Formater la représentation graphique du damier.

        Returns:
            str: Chaîne de caractères représentant le damier.
        """
        # Initialiser une grille vide
        damier = []
        damier_final = []

        for i in range(9):
            ligne = [" " if j % 4 != 0 else "." for j in range(33)]
            damier.append(ligne)

            # Création des lignes vides
            if i < 8:
                ligne = [' '] * 35
                for x, y in self.murs["horizontaux"]:
                    # Regarde si la création des lignes est rendue à la hauteur
                    # où se trouve un/des murs
                    if y == 9 - i:
                        # Remplace " " aux coordonnées voulues dans la liste par "-"
                        for j in range(max(0, (x * 4) - 4), min(35, (x * 4) + 3)):
                            ligne[j] = "-"
                damier.append(ligne)

        # Construction des murs verticaux
        for x, y in self.murs["verticaux"]:
            for i in range(3):
                if i == 1:
                    damier[(16 + i) - (y * 2)][(x * 4) - 5] = "|"
                else:
                    damier[(16 + i) - (y * 2)][(x * 4) - 6] = "|"

        # Placement des joueurs dans le damier
        for i, joueur in enumerate(self.joueurs):
            x, y = joueur["position"]
            damier[18 - (y * 2)][(x - 1) * 4] = str(i + 1)

        for i, ligne in enumerate(damier):
            if i % 2 == 0:
                damier_final.append(f"{9 - (i // 2)} | {''.join(ligne)} |")
            else:
                damier_final.append(f"  |{''.join(ligne)}|")

        damier_final.append("--|-----------------------------------")
        damier_final.append("  | 1   2   3   4   5   6   7   8   9\n")
        return '   ' + ('-' * 35) + '\n' + "\n".join(damier_final)


    def __str__(self):
        """Représentation en art ascii de l'état actuel de la partie.

        Cette représentation est la même que celle du projet précédent.

        Returns:
            str: La chaîne de caractères de la représentation.
        """
        entête = self.formater_entête()
        damier = self.formater_le_damier()
        return entête + damier


    def déplacer_un_joueur(self, joueur, position):
        """Déplace un jeton.

        Pour le joueur spécifié, déplacer son jeton à la position spécifiée.

        Args:
            joueur (str): le nom du joueur.
            position (List[int, int]): La liste [x, y] de la position du jeton (1<=x<=9 et 1<=y<=9).

        Raises:
            QuoridorError: Le joueur n'existe pas.
            QuoridorError: La position est invalide (en dehors du damier).
            QuoridorError: La position est invalide pour l'état actuel du jeu.
        """
        joueur_trouvé = None
        for player in self.joueurs:   #on cherche le joueur (player) dans la liste
            if player["nom"] == joueur:
                joueur_trouvé = player
                break
        else:
            raise QuoridorError("Le joueur n'existe pas.")
        x, y = position
        if not (1 <= x <= 9 and 1 <= y <= 9): #si le joueur est en dehors du damier
            raise QuoridorError("La position est invalide (en dehors du damier).")
        x_actuel, y_actuel = joueur_trouvé["position"] #position du joueur avant le coup
        if abs(x_actuel - x) + abs(y_actuel - y) != 1: #si le joueur ne bouge pas que d'une case
            raise QuoridorError("La position est invalide pour l'état actuel du jeu.")
        joueur_trouvé["position"] = [x, y] #on update la position du joueur


    def placer_un_mur(self, joueur, position, orientation):
        """Placer un mur.

        Pour le joueur spécifié, placer un mur à la position spécifiée.

        Args:
            joueur (str): le nom du joueur.
            position (List[int, int]): la liste [x, y] de la position du mur.
            orientation (str): l'orientation du mur ('MH' ou 'MV').

        Raises:
            QuoridorError: Le joueur n'existe pas.
            QuoridorError: Le joueur a déjà placé tous ses murs.
            QuoridorError: La position est invalide (en dehors du damier).
            QuoridorError: Un mur occupe déjà cette position.
            QuoridorError: Vous ne pouvez pas enfermer un joueur.
        """
        joueur_trouvé = next((j for j in self.joueurs if j["nom"] == joueur), None)
        if joueur_trouvé is None:
            raise QuoridorError("Le joueur n'existe pas.")
        if joueur_trouvé["murs"] == 0:
            raise QuoridorError("Le joueur a déjà placé tous ses murs.")

        x, y = position
        if not (1 <= x <= 9 and 1 <= y <= 9):
            raise QuoridorError("La position est invalide (en dehors du damier).")

        if orientation == "MH":
            murs_liste = self.murs["horizontaux"]
            conflits = [position, [x + 1, y], [x - 1, y]]
        elif orientation == "MV":
            murs_liste = self.murs["verticaux"]
            conflits = [position, [x, y + 1], [x, y - 1]]

        if any(mur in murs_liste for mur in conflits):
            raise QuoridorError("Un mur occupe déjà cette position.")

        murs_liste.append(position)
        joueur_trouvé["murs"] -= 1

        graphe = construire_graphe(
            [joueur['position'] for joueur in self.joueurs],
            self.murs["horizontaux"],
            self.murs["verticaux"]
        )
        if not all([
            nx.has_path(graphe, tuple(self.joueurs[0]["position"]), (5, 9)),
            nx.has_path(graphe, tuple(self.joueurs[1]["position"]), (5, 1))
        ]):
            murs_liste.remove(position)
            joueur_trouvé["murs"] += 1
            raise QuoridorError("Vous ne pouvez pas enfermer un joueur.")
        self.murs["horizontaux" if orientation == "MH" else "verticaux"] = murs_liste


    def appliquer_un_coup(self, joueur, coup, position):
        """Appliquer un coup

        Cette méthode permet d'appliquer un coup à l'état actuel du jeu.

        Si le coup appliqué provient du joueur 2, vous devez incrémenter le tour.

        Args:
            joueur (str): le nom du joueur.
            coup (str): Le type de coup
                'D' pour déplacer le jeton
                'MH' pour placer un mur horizontal
                'MV' pour placer un mur vertical
            position (List[int, int]): La liste [x, y] de la position du coup.

        Raises:
            QuoridorError: Le joueur n'existe pas.
            QuoridorError: Le type de coup est invalide.
            QuoridorError: La position est invalide (en dehors du damier).
            QuoridorError: La partie est déjà terminée.

        Returns:
            tuple: Un tuple composé d'un type de coup et de la position.
               Le type de coup est une chaîne de caractères.
               La position est une liste de 2 entier [x, y].
        """
        joueur_trouvé = next((j for j in self.joueurs if j["nom"] == joueur), None)
        if joueur_trouvé is None:
            raise QuoridorError("Le joueur n'existe pas.")
        if coup not in ["D", "MH", "MV"]:
            raise QuoridorError("Le type de coup est invalide.")
        if not (1 <= position[0] <= 9 and 1 <= position[1] <= 9):
            raise QuoridorError("La position est invalide (en dehors du damier).")
        if coup == "D":
            self.déplacer_un_joueur(joueur, position)
        if self.partie_terminée():
            raise QuoridorError("La partie est déjà terminée.")
        else:
            self.placer_un_mur(joueur, position, coup)
        if joueur == self.joueurs[1]["nom"]:
            self.tour += 1
        return coup, position

    def sélectionner_un_coup(self, joueur):
        """Récupérer le coup

        Notez que seul 2 questions devrait être posée à l'utilisateur.

        Notez aussi que cette méthode ne devrait pas modifier l'état du jeu.

        Args:
            joueur (str): le nom du joueur.

        Raises:
            QuoridorError: Le joueur n'existe pas.
            QuoridorError: Le type de coup est invalide.
            QuoridorError: La position est invalide (en dehors du damier).

        Returns:
            tuple: Un tuple composé d'un type de coup et de la position.
               Le type de coup est une chaîne de caractères.
               La position est une liste de 2 entier [x, y].
        """
        joueur_trouvé = None
        for player in self.joueurs:
            if player["nom"] == joueur:
                joueur_trouvé = player
                break
        if joueur_trouvé is None:
            raise QuoridorError("Le joueur n'existe pas.")
        coup = input("Quel coup voulez-vous jouer? ('D', 'MH', 'MV') : ").strip().upper()
        if coup not in ['D', 'MH', 'MV']:
            raise QuoridorError("Le type de coup est invalide.")
        position = input("Donnez la position du coup à jouer ('x, y') : ")
        position_ok = position.strip().replace(" ", "").split(",")
        x = int(position_ok[0])
        y = int(position_ok[1])
        if not (1 <= x <= 9 and 1 <= y <= 9):
            raise QuoridorError("La position est invalide (en dehors du damier).")
        return coup, [x, y]

    def partie_terminée(self):
        """Déterminer si la partie est terminée.

        Returns:
            str/bool: Le nom du gagnant si la partie est terminée; False autrement.
        """
        if self.joueurs[0]["position"][1] == 9:
            return self.joueurs[0]["nom"]
        if self.joueurs[1]["position"][1] == 1:
            return self.joueurs[1]["nom"]
        return False

    def jouer_un_coup(self, joueur):
        """Jouer un coup automatique pour un joueur.

        Pour le joueur spécifié, jouer automatiquement son meilleur coup pour l'état actuel
        de la partie. Ce coup est soit le déplacement de son jeton, soit le placement d'un
        mur horizontal ou vertical.

        Args:
            joueur (str): le nom du joueur.

        Raises:
            QuoridorError: Le joueur n'existe pas.
            QuoridorError: La partie est déjà terminée.

        Returns:
            tuple: Un tuple composé d'un type de coup et de la position.
               Le type de coup est une chaîne de caractères.
               La position est une liste de 2 entier [x, y].
        """
        jt = next((j for j in self.joueurs if j["nom"] == joueur), None)
        if jt is None:
            raise QuoridorError("Le joueur n'existe pas.")
        if self.partie_terminée():
            raise QuoridorError("La partie est déjà terminée.")
        graphe = construire_graphe(
            [joueur['position'] for joueur in self.joueurs],
            self.murs["horizontaux"],
            self.murs["verticaux"]
        )
        chemin = nx.shortest_path(graphe, tuple(jt["position"]),
                                  (jt["position"][0], 9) if joueur == self.joueurs[0]["nom"] else (
                                  jt["position"][0], 1))
        
        prochaine_position = list(chemin[1])

        self.déplacer_un_joueur(joueur, prochaine_position)

        return "D", prochaine_position


def interpréter_la_ligne_de_commande():
    """Génère un interpréteur de commande.

    Returns:
        Namespace: Un objet Namespace tel que retourné par parser.parse_args().
                   Cette objet aura l'attribut «idul» représentant l'idul du joueur.
    """
    parser = argparse.ArgumentParser(
        description="Quoridor"
    )
    parser.add_argument(
        "idul",
        type=str,
        help="IDUL du joueur"
    )
    return parser.parse_args()
