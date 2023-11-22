# Variables principales du jeu
cases = {}
pions = {"white": {}, "black": {}}
couleurs = [(0, 0, 0), (255, 255, 255)]
letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]    

# Cases du palais noir et blanc
palais_w = ["H4", "H5", "H6", "I4", "I5", "I6", "J4", "J5", "J6"]
palais_b = ["A4", "A5", "A6", "B4", "B5", "B6", "C4", "C5", "C6"]

# Case d'apparition des pions blancs et noirs
spawn = {
    "white": {
        "roi": ["J5"],
        "conseiller": ["J4", "J6"],
        "elephant": ["J3", "J7"],
        "cheval": ["J2", "J8"],
        "chariot": ["J1", "J9"],
        "canon": ["H1", "H9"],
        "soldat": ["G1", "G3", "G5", "G7", "G9"],
    },
    "black": {
        "roi": ["A5"],
        "conseiller": ["A4", "A6"],
        "elephant": ["A3", "A7"],
        "cheval": ["A2", "A8"],
        "chariot": ["A1", "A9"],
        "canon": ["C2", "C8"],
        "soldat": ["D1", "D3", "D5", "D7", "D9"],
    },
}

# Mouvements autorisé pour chaque pion
mouvs = {
    "帥": [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1),
    ],
}

# Les pions et leur nom en écriture chinoise
pion = {
    "roi": "帥",
    "conseiller": "仕",
    "elephant": "象",
    "cheval": "馬",
    "chariot": "車",
    "canon": "砲",
    "soldat": "兵",
}

# Position de chaque lettre (A,B,C,D etc)
positions = {
    "y": {
        "A": 75 - 36,
        "B": 148 - 36,
        "C": 221 - 36,
        "D": 294 - 36,
        "E": 367 - 36,
        "F": 440 - 36,
        "G": 513 - 36,
        "H": 586 - 36,
        "I": 659 - 36,
        "J": 732 - 36,
    },
    "x": {
        "1": 75 - 36,
        "2": 148 - 36,
        "4": 221 - 36,
        "4": 294 - 36,
        "5": 367 - 36,
        "6": 440 - 36,
        "7": 513 - 36,
        "8": 586 - 36,
        "9": 659 - 36,
    },
}

# Création des cases avec leur positions exactes ('A1' : '39-39' etc)
for k, v in positions["y"].items():
    for i, j in positions["x"].items():
        cases[k + i] = str(j) + "-" + str(v)
