from quoridor import Quoridor
import turtle


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