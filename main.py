"""Jeu Quoridor

Ce programme permet de joueur au jeu Quoridor.
"""

from api import appliquer_un_coup, créer_une_partie, récupérer_une_partie
from quoridor import Quoridor, interpréter_la_ligne_de_commande

# Mettre ici votre IDUL comme clé et votre Jeton comme secret.
JETONS = {
    "ralem59": "37a12da5-c506-411b-8c4e-2979dec6249b",
}



if __name__ == "__main__":
    args = interpréter_la_ligne_de_commande()
    AUTOMATIQUE = args.automatique
    secret = JETONS[args.idul]
    id_partie, état = créer_une_partie(args.idul, secret)
    quoridor = Quoridor(état["joueurs"], état["murs"], état["tour"])
    while True:
        # Afficher la partie
        print(quoridor)
        # Demander au joueur de choisir son prochain coup
        if AUTOMATIQUE:
            # Choisir automatiquement le prochain coup
            coup, position = quoridor.jouer_un_coup(quoridor.état_partie()["joueurs"][0]["nom"])
        else:
            # Laisser le joueur choisir son prochain coup
            coup, position = quoridor.sélectionner_un_coup(
                quoridor.état_partie()["joueurs"][0]["nom"]
            )

            # Appliquer le coup dans votre jeu
            coup, position = quoridor.appliquer_un_coup(
                quoridor.état_partie()["joueurs"][0]["nom"],
                coup,
                position,
            )
        try:
            # Envoyer le coup au serveur
            coup, position = appliquer_un_coup(
                id_partie,
                coup,
                position,
                args.idul,
                secret,
            )

            # Appliquer le coup de l'adversaire dans votre jeu
            coup, position = quoridor.appliquer_un_coup(
                quoridor.état_partie()["joueurs"][1]["nom"],
                coup,
                position,
            )
        except StopIteration as erreur:
            # Si le jeu est terminé
            # Récupérer la partie finale
            id_partie, état = récupérer_une_partie(
                id_partie,
                args.idul,
                secret,
            )
            # Afficher la partie finale
            quoridor = Quoridor(état["joueurs"], état["murs"], état["tour"])
            print(quoridor)
            # Afficher le gagnant
            print(f"Le gagnant est {erreur}")
            # Sortir de la boucle
            break
