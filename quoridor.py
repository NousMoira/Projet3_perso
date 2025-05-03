"""Module de la classe Quoridor

Classes:
    * Quoridor - Classe pour encapsuler le jeu Quoridor.
    * interpréter_la_ligne_de_commande - Génère un interpréteur de commande.
"""

import argparse
import turtle

import networkx as nx


from copy import deepcopy
from quoridor_error import QuoridorError
from graphe import construire_graphe
from api import récupérer_une_partie







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

        graphe = construire_graphe(
            [joueur["position"] for joueur in self.joueurs],
            self.murs["horizontaux"],
            self.murs["verticaux"]
        )
        if (x, y) not in graphe.successors((x_actuel, y_actuel)):
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
        

        if (
            (orientation == "MH" and (
                position in self.murs["horizontaux"] or
                [x + 1, y] in self.murs["horizontaux"] or
                [x - 1, y] in self.murs ["horizontaux"] or
                [x + 1, y - 1] in self.murs["verticaux"]
            )) or
            (orientation == "MV" and (
                position in self.murs["verticaux"] or
                [x, y + 1] in self.murs["verticaux"] or
                [x, y - 1] in self.murs["verticaux"] or
                [x - 1, y + 1] in self.murs["horizontaux"]
            ))
        ):
            raise QuoridorError("Un mur occupe déjà cette position.")

        #Déterminer la clés (orientation)
        cle_murs = "horizontaux" if orientation == "MH" else "verticaux"

        #Placer le mur
        murs_liste = self.murs[cle_murs]
        murs_liste.append(position)
        joueur_trouvé["murs"] -= 1

        graphe = construire_graphe(
            [joueur['position'] for joueur in self.joueurs],
            self.murs["horizontaux"],
            self.murs["verticaux"]
        )

        # Vérifier si le joueur 1 peut atteindre n'importe quelle position sur la ligne 9
        objectifs_joueur1 = [(x, 9) for x in range(1, 10)]
        chemin_joueur1 = any(nx.has_path(graphe, tuple(self.joueurs[0]["position"]), objectif) for objectif in objectifs_joueur1)

        # Vérifier si le joueur 2 peut atteindre n'importe quelle position sur la ligne 1
        objectifs_joueur2 = [(x, 1) for x in range(1, 10)]
        chemin_joueur2 = any(nx.has_path(graphe, tuple(self.joueurs[1]["position"]), objectif) for objectif in objectifs_joueur2)

        if not (chemin_joueur1 and chemin_joueur2):
            murs_liste.remove(position)
            joueur_trouvé["murs"] += 1
            raise QuoridorError("Vous ne pouvez pas enfermer un joueur.")


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
        elif coup in ["MH", "MV"]:
            self.placer_un_mur(joueur, position, coup)
        else:
            raise QuoridorError("Le type de coup est invalide.")
        
        if self.partie_terminée():
            raise QuoridorError("La partie est déjà terminée.")
        
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
        """Détermine le meilleur coup pour un joueur en utilisant l'algorithme Minimax.

        Cette méthode calcule le meilleur coup, l'applique à l'état local, et met à jour
        les attributs `self.joueurs` et `self.murs`.

        Args:
            joueur (str): le nom du joueur.
            id_partie (str): l'identifiant de la partie (non utilisé ici).
            idul (str): l'IDUL du joueur (non utilisé ici).
            secret (str): le secret pour l'authentification (non utilisé ici).

        Returns:
            tuple: Un tuple composé d'un type de coup et de la position.
        """
        if self.partie_terminée():
            return None
        def fonction_evaluation(etat, joueur_actuel):
            """Évalue la qualité d'un état du jeu."""
            graphe = construire_graphe(
                [joueur['position'] for joueur in etat.joueurs],
                etat.murs["horizontaux"],
                etat.murs["verticaux"]
            )
            position_joueur = tuple(etat.joueurs[0]["position"])
            position_adversaire = tuple(etat.joueurs[1]["position"])

            # Objectifs : toute la ligne 9 pour le joueur 1, toute la ligne 1 pour le joueur 2
            objectifs_joueur = [(x, 9) for x in range(1, 10)]
            objectifs_adversaire = [(x, 1) for x in range(1, 10)]

            # Trouver le chemin le plus court vers n'importe quelle position sur la ligne cible
            try:
                distance_joueur = min(
                    len(nx.shortest_path(graphe, position_joueur, objectif))
                    for objectif in objectifs_joueur
                    if nx.has_path(graphe, position_joueur, objectif)
                )
            except ValueError:
                # Aucun chemin trouvé pour le joueur
                distance_joueur = float('inf')

            try:
                distance_adversaire = min(
                    len(nx.shortest_path(graphe, position_adversaire, objectif))
                    for objectif in objectifs_adversaire
                    if nx.has_path(graphe, position_adversaire, objectif)
                )
            except ValueError:
                # Aucun chemin trouvé pour l'adversaire
                distance_adversaire = float('inf')

            # Plus la distance de l'adversaire est grande, mieux c'est
            return distance_adversaire - distance_joueur

        def minimax(etat, profondeur, alpha, beta, maximiser, joueur_actuel):
            """Implémente l'algorithme Minimax avec élagage alpha-beta."""
            if profondeur == 0 or etat.partie_terminée():
                return fonction_evaluation(etat, joueur_actuel), None

            if maximiser:
                meilleur_score = float('-inf')
                meilleur_coup = None

                for coup, position in generer_coups_possibles(etat, joueur_actuel):
                    etat_simulé = deepcopy(etat)
                    try:
                        # Vérifier si le coup est gagnant
                        if coup == "D" and position[1] == 9 and joueur_actuel == etat.joueurs[0]["nom"]:
                            return float('inf'), (coup, position)
                        if coup == "D" and position[1] == 1 and joueur_actuel == etat.joueurs[1]["nom"]:
                            return float('inf'), (coup, position)

                        etat_simulé.appliquer_un_coup(joueur_actuel, coup, position)
                        score, _ = minimax(etat_simulé, profondeur - 1, alpha, beta, False, joueur_actuel)
                        if score > meilleur_score:
                            meilleur_score = score
                            meilleur_coup = (coup, position)
                        alpha = max(alpha, score)
                        if beta <= alpha:
                            break
                    except QuoridorError as e:
                        print(f"Erreur lors de l'application du coup : {e}")
                        continue

                return meilleur_score, meilleur_coup
            else:
                meilleur_score = float('inf')
                meilleur_coup = None

                adversaire = self.joueurs[1]["nom"] if joueur_actuel == self.joueurs[0]["nom"] else self.joueurs[0]["nom"]
                for coup, position in generer_coups_possibles(etat, adversaire):
                    etat_simulé = deepcopy(etat)
                    try:
                        # Vérifier si le coup est gagnant pour l'adversaire
                        if coup == "D" and position[1] == 9 and adversaire == etat.joueurs[0]["nom"]:
                            return float('-inf'), (coup, position)
                        if coup == "D" and position[1] == 1 and adversaire == etat.joueurs[1]["nom"]:
                            return float('-inf'), (coup, position)

                        etat_simulé.appliquer_un_coup(adversaire, coup, position)
                        score, _ = minimax(etat_simulé, profondeur - 1, alpha, beta, True, joueur_actuel)
                        if score < meilleur_score:
                            meilleur_score = score
                            meilleur_coup = (coup, position)
                        beta = min(beta, score)
                        if beta <= alpha:
                            break
                    except QuoridorError as e:
                        print(f"Erreur lors de l'application du coup : {e}")
                        continue

                return meilleur_score, meilleur_coup

        def generer_coups_possibles(etat, joueur_actuel):
            """Génère tous les coups possibles pour un joueur."""
            coups = []

            # Ajouter les déplacements possibles
            position_actuelle = tuple(next(j for j in etat.joueurs if j["nom"] == joueur_actuel)["position"])
            graphe = construire_graphe(
                [joueur['position'] for joueur in etat.joueurs],
                etat.murs["horizontaux"],
                etat.murs["verticaux"]
            )

            if joueur_actuel == etat.joueurs [0]["nom"] and position_actuelle[1] == 8:
                for voisin in graphe.successors(position_actuelle):
                    if voisin[1] == 9:
                        coups.append(("D", list(voisin)))
                        return coups
                    
            for voisin in graphe.successors(position_actuelle):
                # Ignorer les destinations finales "B1" et "B2"
                if isinstance(voisin, str):  # Exclure "B1" et "B2"
                    continue
                if not (1 <= voisin[0] <= 9 and 1 <= voisin[1] <= 9):  # Vérifier les limites du damier
                    continue
                coups.append(("D", list(voisin)))

            # Ajouter les placements de murs possibles
            if next(j for j in etat.joueurs if j["nom"] == joueur_actuel)["murs"] > 0:
                for x in range(1, 9):
                    for y in range(2, 9):
                        for orientation in ["MH", "MV"]:
                            if orientation == "MV" and x == 1:  # Ignorer les murs verticaux à x=1
                                continue
                            position_mur = [x, y]
                            if position_mur not in etat.murs["horizontaux"] and position_mur not in etat.murs["verticaux"]:
                                try:
                                    etat_simulé = deepcopy(etat)
                                    etat_simulé.placer_un_mur(joueur_actuel, position_mur, orientation)
                                    coups.append((orientation, position_mur))
                                except QuoridorError:
                                    continue

            return coups

        # Appeler Minimax pour déterminer le meilleur coup
        _, meilleur_coup = minimax(self, profondeur=2, alpha=float('-inf'), beta=float('inf'), maximiser=True, joueur_actuel=joueur)
        
        if meilleur_coup is None:
            # 1) Reconstruire le graphe pour l'état actuel
            graphe = construire_graphe(
                [j['position'] for j in self.joueurs],
                self.murs["horizontaux"],
                self.murs["verticaux"]
            )
            # 2) Position actuelle et objectifs
            pos_actuelle = tuple(next(j for j in self.joueurs if j["nom"] == joueur)["position"])
            # On définit la ligne cible selon le joueur
            if joueur == self.joueurs[0]["nom"]:
                objectifs = [(x, 9) for x in range(1, 10)]
            else:
                objectifs = [(x, 1) for x in range(1, 10)]
            # 3) Trouver le plus court chemin vers la ligne cible
            chemins = []
            for obj in objectifs:
                if nx.has_path(graphe, pos_actuelle, obj):
                    chemins.append(nx.shortest_path(graphe, pos_actuelle, obj))
            if chemins:
                # on choisit le chemin le plus court
                chemin_min = min(chemins, key=len)
                # si on peut avancer d’au moins une case
                if len(chemin_min) >= 2:
                    # propose de se déplacer vers la deuxième case du chemin
                    prochain_pos = chemin_min[1]
                    meilleur_coup = ("D", list(prochain_pos))

        # Appliquer le coup calculé à l'état local
        coup, position = meilleur_coup
        if coup == "D":
            self.déplacer_un_joueur(joueur, position)
        elif coup in ["MH", "MV"]:
            self.placer_un_mur(joueur, position, coup)

        # Retourner le coup et la position
        return meilleur_coup
    


class QuoridorX(Quoridor):
    """
    Classe graphique héritant de Quoridor.
    Toute la logique de Quoridor (jouer_un_coup, appliquer_un_coup, etc.)
    est conservée via super(), et on y ajoute uniquement l'affichage Turtle.
    """
    

    def __init__(self, joueurs, murs=None, tour=1):
        # Appel au constructeur de la classe de base (logique)
        super().__init__(joueurs, murs, tour)

        # Configuration de la fenêtre Turtle
        self.screen = turtle.Screen()
        self.screen.title("Quoridor")
        self.screen.setup(width=600, height=600)
        self.screen.tracer(0, 0)

        # Turtle pour dessiner
        self.drawer = turtle.Turtle()
        self.drawer.hideturtle()
        self.drawer.speed(0)

        # Taille et origine du damier (9×9 cases)
        self.cell_size = 50
        half = self.cell_size * 4.5
        self.origin = (-half, -half)

        # Premier affichage
        self.afficher()

    def afficher(self):
        """
        Dessine le plateau, les murs et les pions en se basant
        sur l'état courant renvoyé par état_partie().
        """
        # Récupérer l'état actuel via la méthode de la classe parente
        state = self.état_partie()
        joueurs = state["joueurs"]
        murs = state["murs"]

        # Effacer tout dessin précédent
        self.drawer.clear()

        # 1) Quadrillage 9×9
        for i in range(10):
            # lignes horizontales
            x0 = self.origin[0]
            y = self.origin[1] + i * self.cell_size
            self.drawer.penup(); self.drawer.goto(x0, y); self.drawer.pendown()
            self.drawer.forward(self.cell_size * 9)

            # lignes verticales
            self.drawer.penup(); self.drawer.goto(self.origin[0] + i * self.cell_size, self.origin[1])
            self.drawer.pendown(); self.drawer.setheading(90)
            self.drawer.forward(self.cell_size * 9)
            self.drawer.setheading(0)

        # 2) Murs horizontaux hérités
        self.drawer.width(5)
        for x, y in murs["horizontaux"]:
            sx = self.origin[0] + (x-1) * self.cell_size
            sy = self.origin[1] + (y-2) * self.cell_size + self.cell_size
            self.drawer.penup(); self.drawer.goto(sx, sy); self.drawer.pendown()
            self.drawer.forward(self.cell_size * 2)

        # 3) Murs verticaux hérités
        for x, y in murs["verticaux"]:
            sx = self.origin[0] + (x-2) * self.cell_size + self.cell_size
            sy = self.origin[1] + (y - 1 + 2) * self.cell_size
            self.drawer.penup(); self.drawer.goto(sx, sy); self.drawer.pendown()
            self.drawer.setheading(270); self.drawer.forward(self.cell_size * 2)
            self.drawer.setheading(0)
        self.drawer.width(1)

        # 4) Pions des joueurs hérités
        couleurs = ["blue", "red"]
        for idx, joueur in enumerate(joueurs):
            x, y = joueur["position"]
            sx = self.origin[0] + (x-1) * self.cell_size + self.cell_size/2
            sy = self.origin[1] + (y-1) * self.cell_size + self.cell_size/2
            self.drawer.penup(); self.drawer.goto(sx, sy)
            self.drawer.dot(self.cell_size * 0.6, couleurs[idx])

        # Actualiser l'affichage
        self.screen.update()
    
    def __deepcopy__(self, memo):
    # Ne copie que la partie logique -> retourne un Quoridor pur
        return Quoridor(self.joueurs, self.murs, self.tour)
    
    


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
        help="IDUL du joueur",
    )
    parser.add_argument("-a", "--automatique",
                         help="Activer le mode automatique."
                         )
    parser.add_argument("-x","--graphique", 
                        help="Activer le mode graphique."
                        )
    return parser.parse_args()

# ---- Alias automatique de Quoridor vers QuoridorX si -x/--graphique ----

# On récupère les arguments déjà définis dans le module
_args = interpréter_la_ligne_de_commande()

# Si on a demandé le mode graphique, Quoridor devient QuoridorX
if _args.graphique:
    Quoridor = QuoridorX