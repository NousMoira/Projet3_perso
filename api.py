"""Module d'API du jeu Quoridor

Attributes:
    URL (str): Constante représentant le début de l'url du serveur de jeu.

Functions:
    * créer_une_partie - Créer une nouvelle partie et retourne l'état de cette dernière.
    * récupérer_une_partie - Retrouver l'état d'une partie spécifique.
    * appliquer_un_coup - Exécute un coup et retourne le nouvel état de jeu.
"""

import requests

URL = "https://pax.ulaval.ca/quoridor/api/h25"


def créer_une_partie(idul, secret):
    """Créer une partie

    Args:
        idul (str): idul du joueur
        secret (str): secret récupéré depuis le site de PAX

    Raises:
        PermissionError: Erreur levée lorsque le serveur retourne un code 401.
        RuntimeError: Erreur levée lorsque le serveur retourne un code 406.
        ConnectionError: Erreur levée lorsque le serveur retourne un code autre que 200, 401 ou 406

    Returns:
        tuple: Tuple constitué de l'identifiant de la partie en cours
            et de l'état courant du jeu, après avoir décodé
            le JSON de sa réponse.
    """
    rep = requests.post(
        f"{URL}/parties",
        auth=(idul, secret)
    )

    if rep.status_code == 200:
        data = rep.json()
        return data["id"], data["état"]
    if rep.status_code == 401:
        raise PermissionError(rep.json().get("message"))
    if rep.status_code == 406:
        raise RuntimeError(rep.json().get("message"))
    raise ConnectionError()


def appliquer_un_coup(id_partie, coup, position, idul, secret):
    """Appliquer un coup

    Args:
        id_partie (str): Identifiant de la partie.
        coup (str): Type de coup du joueur :
                            'D' pour déplacer le jeton,
                            'MH' pour placer un mur horizontal,
                            'MV' pour placer un mur vertical;
        position (list): La position [x, y] du coup.
        idul (str): idul du joueur
        secret (str): secret récupéré depuis le site de PAX

    Raises:
        StopIteration: Erreur levée lorsqu'il y a un gagnant dans la réponse du serveur.
        PermissionError: Erreur levée lorsque le serveur retourne un code 401.
        ReferenceError: Erreur levée lorsque le serveur retourne un code 404.
        RuntimeError: Erreur levée lorsque le serveur retourne un code 406.
        ConnectionError: Erreur levée lorsque le serveur retourne un code autre que 200, 401 ou 406

    Returns:
        tuple: Tuple constitué du coup joué par le serveur et de la position du coup,
    """
    rep = requests.put(
        f"{URL}/parties/{id_partie}",
        auth=(idul, secret),
        json={
            "coup": coup,
            "position": position
        }
    )

    if rep.status_code == 200:
        data = rep.json()
        if data.get("partie") == "terminée":
            raise StopIteration(rep.json().get("gagnant"))
        return data["coup"], data["position"]
    if rep.status_code == 401:
        raise PermissionError(rep.json().get("message"))
    if rep.status_code == 404:
        raise ReferenceError(rep.json().get("message"))
    if rep.status_code == 406:
        raise RuntimeError(rep.json().get("message"))
    raise ConnectionError()


def récupérer_une_partie(id_partie, idul, secret):
    """Récupérer une partie

    Args:
        id_partie (str): identifiant de la partie à récupérer
        idul (str): idul du joueur
        secret (str): secret récupéré depuis le site de PAX

    Raises:
        PermissionError: Erreur levée lorsque le serveur retourne un code 401.
        ReferenceError: Erreur levée lorsque le serveur retourne un code 404.
        RuntimeError: Erreur levée lorsque le serveur retourne un code 406.
        ConnectionError: Erreur levée lorsque le serveur retourne un code autre que 200, 401 ou 406

    Returns:
        tuple: Tuple constitué de l'identifiant de la partie en cours
            et de l'état courant du jeu, après avoir décodé
            le JSON de sa réponse.
    """
    rep = requests.get(
        f"{URL}/parties/{id_partie}",
        auth=(idul, secret),
    )

    if rep.status_code == 200:
        data = rep.json()
        return data["id"], data["état"]
    if rep.status_code == 401:
        raise PermissionError(rep.json().get("message"))
    if rep.status_code == 404:
        raise ReferenceError(rep.json().get("message"))
    if rep.status_code == 406:
        raise RuntimeError(rep.json().get("message"))
    raise ConnectionError()
