import pygame as pg
from pygame.locals import *
from variables import *
from math import *
from functions import is_case_disponible, distance
import os

# Initialisation de certaines variables pour le jeu
screen = pg.display.set_mode((730, 900))
pg.display.set_caption("Xiangqi")
ic = 0


# Class Case qui permet de savoir où sont les cases
class Case:
    def __init__(self, pos, name):
        self.x, self.y = pos.split("-")
        self.name = name


# Class Players qui permet de créer les joueurs
class Player:
    def __init__(self, name, col):
        self.name = name
        self.gagne = False
        self.color = col


# Class Pion qui crée les pions du jeu avec leur nom etc
class Pion:
    def __init__(self, pos, fr, color, moves):
        self.fr = fr
        self.name = pion.get(self.fr)
        self.x, self.y = pos
        self.outed = False
        self.color = color
        self.case = None
        self.case_eat = []
        self.last_case = []
        for akk, c in cases.items():
            if c == str(self.x) + "-" + str(self.y):
                self.case = akk
        self.liste_actions = (self.case, None)
        self.movements = moves
        if self.color == 0 and self.fr == "soldat":
            self.movements = [(0, -1)]
        self.suivre_souris = False
        self.cases_available = []
        self.cases_dispo()

    def cases_dispo(self):
        self.cases_available = []
        for j in range(len(self.movements)):
            if len(self.movements[j]) >= 2:
                a, b = self.movements[j][0], self.movements[j][1]
                n_x, n_y = self.x + (a * 73), self.y + (b * 73)
            for k, v in cases.items():
                if is_case_disponible(self, k, entities, self.color):
                    if str(n_x) + "-" + str(n_y) == v:
                        if self.fr == "roi" or self.fr == "conseiller":
                            if k in palais[self.color]:
                                self.cases_available.append(k)
                        # elif self.fr == "elephant":
                        #     if k in zones[self.color]:
                        #         self.cases_available.append(k)
                        else:
                            if self.peut_sauter_autre_pion(k, entities):
                                continue
                            else:
                                self.cases_available.append(k)
        if self.fr == "cheval":
            res = self.cheval_check()
            if len(res) > 0:
                for ab in res:
                    if ab in self.cases_available:
                        self.cases_available.remove(ab)

    def peut_sauter_autre_pion(self, case_cible, autres_pions):
        # Séparer les composantes alphabétiques et numériques de la chaîne de la case cible
        cible_x, cible_y = ord(case_cible[0]) - ord("A") + 1, int(case_cible[1:])

        # Parcourir tous les autres pions sur le plateau
        for autre_pion in autres_pions:
            if autre_pion != self:
                # Convertir les coordonnées du pion en entiers
                pion_x, pion_y = autre_pion.x, autre_pion.y

                # Vérifier si le pion est situé sur la trajectoire du mouvement
                if (self.x + cible_x) // 2 == pion_x and (
                    self.y + cible_y
                ) // 2 == pion_y:
                    return (
                        True  # La case cible permet de sauter par-dessus un autre pion
                    )

        return False  # Aucun pion n'est sauté

    def cheval_check(self):
        pos = self.case
        board = [
            ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9"],
            ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9"],
            ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9"],
            ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9"],
            ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9"],
            ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9"],
            ["G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9"],
            ["H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9"],
            ["I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8", "I9"],
            ["J1", "J2", "J3", "J4", "J5", "J6", "J7", "J8", "J9"],
        ]

        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == pos:
                    index = (i, j)

        board[index[0]][index[1]] = "@"

        cases_f = {}
        if 0 <= index[0] - 1 < len(board) and 0 <= index[1] < len(board[index[0] - 1]):
            cases_f[index[0] - 1, index[1]] = board[index[0] - 1][index[1]]
        if 0 <= index[0] + 1 < len(board) and 0 <= index[1] < len(board[index[0] + 1]):
            cases_f[index[0] + 1, index[1]] = board[index[0] + 1][index[1]]
        if 0 <= index[0] < len(board) and 0 <= index[1] - 1 < len(board[index[0]]):
            cases_f[index[0], index[1] - 1] = board[index[0]][index[1] - 1]
        if 0 <= index[0] < len(board) and 0 <= index[1] + 1 < len(board[index[0]]):
            cases_f[index[0], index[1] + 1] = board[index[0]][index[1] + 1]
        cases_update = {}

        for ents in entities:
            for k, v in cases_f.items():
                if ents.case in v:
                    cases_update[k] = ents.case

        for ii in range(len(board)):
            for jj in range(len(board[ii])):
                if board[ii][jj] in cases_update.values():
                    board[ii][jj] = "CU"
                elif board[ii][jj] in cases_f.values():
                    board[ii][jj] = "CF"

        cases_to_update = []
        n_index_1 = None  # initialisation en dehors des conditions
        n_index_2 = None  # initialisation en dehors des conditions

        for a, b in cases_update.items():
            if a[0] > index[0]:
                if 0 <= index[0] + 2 < 10 and 0 <= index[1] - 1 < 9:
                    n_index_1 = (index[0] + 2, index[1] - 1)
                if 0 <= index[0] + 2 < 10 and 0 <= index[1] + 1 < 9:
                    n_index_2 = (index[0] + 2, index[1] + 1)
            elif a[0] < index[0]:  # changed from "if" to "elif"
                if 0 <= index[0] - 2 < 10 and 0 <= index[1] - 1 < 9:
                    n_index_1 = (index[0] - 2, index[1] - 1)  # corrected index[0] - 2
                if 0 <= index[0] - 2 < 10 and 0 <= index[1] + 1 < 9:
                    n_index_2 = (index[0] - 2, index[1] + 1)  # corrected index[0] - 2
            if a[1] > index[1]:
                if (
                    0 <= index[0] - 1 < 10 and 0 <= index[1] + 2 < 9
                ):  # corrected index[0] - 1
                    n_index_1 = (index[0] - 1, index[1] + 2)
                if (
                    0 <= index[0] + 1 < 10 and 0 <= index[1] + 2 < 9
                ):  # corrected index[0] + 1
                    n_index_2 = (index[0] + 1, index[1] + 2)
            elif a[1] < index[1]:  # changed from "if" to "elif"
                if (
                    0 <= index[0] - 1 < 10 and 0 <= index[1] - 2 < 9
                ):  # corrected index[0] - 1
                    n_index_1 = (index[0] - 1, index[1] - 2)
                if (
                    0 <= index[0] + 1 < 10 and 0 <= index[1] - 2 < 9
                ):  # corrected index[0] + 1
                    n_index_2 = (index[0] + 1, index[1] - 2)
            cases_to_update.append(n_index_1)
            cases_to_update.append(n_index_2)

        cases_to_update = list(set(cases_to_update))

        for e in cases_to_update:
            if e == None:
                cases_to_update.remove(e)

        n_cases_to_update = []
        for key in cases_to_update:
            if board[key[0]][key[1]] not in zones[self.color]:
                n_cases_to_update.append(board[key[0]][key[1]])

        for cas in palais[self.color]:
            n_cases_to_update.append(cas)
        return n_cases_to_update

    def draw(self):
        chemin = "Xiangqi\\fonts\\SIMSUN.ttf"
        c = 1 if self.color == 0 else 0
        font = pg.font.Font(
            chemin,
            35,
        )
        ecrit = font.render(self.name, True, (colors[self.color]))

        surface_size = max(ecrit.get_width(), ecrit.get_height()) + 30
        cercle = pg.Surface((surface_size, surface_size), pg.SRCALPHA)

        center = (surface_size // 2, surface_size // 2)

        pg.draw.circle(cercle, couleurs[1], center, surface_size // 2 - 1)
        pg.draw.circle(cercle, colors[self.color], center, surface_size // 2 - 3)
        pg.draw.circle(cercle, couleurs[1], center, surface_size // 2 - 5)

        text_rect = ecrit.get_rect(center=(center[0], center[1] - 2))
        cercle.blit(ecrit, text_rect.topleft)
        screen.blit(cercle, (self.x - surface_size // 2, self.y - surface_size // 2))

    def out(self, entites, pion):
        self.outed = True
        entites.remove(pion)


# Class Board qui dessine le tableau du jeu d'échec
class Board:
    def __init__(self):
        self.taille_cellule = 75
        self.color = (0, 0, 0)

    def draw_rect(self, pos):
        x, y = pos
        pg.draw.rect(
            screen,
            self.color,
            pg.Rect(x, y, self.taille_cellule, self.taille_cellule),
            2,
        )

    def draw_line(self, pos1, pos2, lar):
        x1, y1 = pos1
        x2, y2 = pos2
        pg.draw.line(screen, self.color, (x1, y1), (x2, y2), lar)

    def draw_board(self):
        pos = (75, 75)
        pos1 = (75 + 3 * 73, 75)
        pos2 = (75 + 5 * 73, 75 + 2 * 73)
        pos3 = (68, 68)
        pos4 = (730 - 63, 68)

        for k in range(2):
            for i in range(4):
                for j in range(8):
                    self.draw_rect(pos)
                    pos = (pos[0] + 73, pos[1])
                pos = (75, pos[1] + 73)
            pos = (75, 75 + 5 * 73)

        for b in range(2):
            for a in range(2):
                self.draw_line(pos1, pos2, 3)
                if b == 1:
                    pos1 = (pos1[0], pos1[1] + 2 * 73)
                    pos2 = (pos2[0], pos2[1] - 2 * 73)
                else:
                    pos1 = (pos1[0], pos1[1] + 2 * 73)
                    pos2 = (pos2[0], pos2[1] - 2 * 73)
            pos1 = (75 + 3 * 73, 75 + 7 * 73)
            pos2 = (75 + 5 * 73, 75 + 9 * 73)

        for t in range(2):
            self.draw_line(pos3, pos4, 5)
            pos3 = (pos4[0], pos4[1])
            pos4 = (pos4[0], pos4[1] + 800 - 2 * 64)

        pos3 = (68, 68)
        pos4 = (68, 800 - 60)

        for h in range(2):
            self.draw_line(pos3, pos4, 5)
            pos3 = (pos4[0], pos4[1])
            pos4 = (pos4[0] + 730 - 2 * 65, pos4[1])


# Class Game qui comporte le jeu d'échec chinois
class Game:
    def __init__(self, board, players, pions, cases):
        self.board = board
        self.players = players
        self.pions = pions
        self.running = False
        self.cases = cases
        self.turn = 0
        self.dernier_mouvement = None
        self.current_player = None
        self.start = False

    def run(self):
        pg.init()
        self.turn = 0
        self.current_player = self.players[self.turn]
        self.running = True

    def switch_player(self):
        self.turn = (self.turn + 1) % 2
        self.current_player = self.players[self.turn]
        for ent in entities:
            if isinstance(ent, Pion) and ent.color == self.current_player:
                ent.cases_dispo()
        self.dernier_mouvement = None

    def display_current_player(self):
        font = pg.font.Font("Xiangqi\\fonts\\Poppins.ttf", 30)
        font2 = pg.font.Font("Xiangqi\\fonts\\Poppins.ttf", 18)
        player_name = self.players[self.turn].name
        text = f"{player_name}"
        txt1 = "Au tour de :"
        t1 = font2.render(txt1, True, (255, 255, 255))
        self.current_player_text = font.render(text, True, (255, 255, 255))
        points1 = [(100 + 96, 780), (350 + 96, 780), (320 + 96, 878), (100 + 96, 878)]
        points2 = [(350 + 96, 780), (450 + 96, 780), (450 + 96, 878), (320 + 96, 878)]
        c = 1 if self.turn == 0 else 0
        txt2 = f"{self.players[c].name}"
        t2 = font2.render(txt2, True, (255, 255, 255))
        pg.draw.polygon(screen, colss[self.turn], points1)
        pg.draw.polygon(screen, colss[c], points2)
        img = (
            pg.image.load("Xiangqi/img/player1.png").convert_alpha()
            if self.turn == 0
            else pg.image.load("Xiangqi/img/player2.png").convert_alpha()
        )
        imgPlayer = pg.transform.scale(img, (90 * 0.81, 90))
        screen.blit(t1, ((110 + 96, 780)))
        screen.blit(t2, ((345 + 96, 815)))
        screen.blit(self.current_player_text, (110 + 96, 810))
        screen.blit(imgPlayer, (330, 789))

    def validate_move(self, ent):
        if self.dernier_mouvement is not None:
            ent.cases_dispo()
            self.switch_player()
        self.dernier_mouvement = None

    def retour_arriere(self):
        if self.dernier_mouvement:
            ent, ancienne_case = self.dernier_mouvement
            x, y = cases[ancienne_case].split("-")
            x, y = int(x), int(y)
            ent.x = x
            ent.y = y
            ent.case = ancienne_case
            if ent.last_case:
                ent.last_case.pop()
            self.dernier_mouvement = None
            ent.cases_dispo()
        self.dernier_mouvement = None


# Initialisation de la classe MainMenu pour demander les noms des joueurs
board = Board()
pp1 = None
pp2 = None
game = Game(board, [pp1, pp2], pions, cases)


# Utilisation des class
game.run()
i = 1

# Création de tout les piosn du jeu
entities = []
for col, entite in pions.items():
    for g in range(len(entite)):
        tr = cases.get(spawn[col].get(entite[g])[0])
        del spawn[col][entite[g]][0]
        w, x = tr.split("-")
        pos = (int(w), int(x))
        couleur = 0 if col == "white" else 1
        mov = mouvs.get(pion.get(entite[g]))
        pion_entite = Pion(pos, entite[g], couleur, mov)
        entities.append(pion_entite)

for entiy in entities:
    entiy.cases_dispo()

ic += 1

def get_player_names():
    font = pg.font.Font(None, 32)
    input_box1 = pg.Rect(200, 300, 140, 32)
    input_box2 = pg.Rect(200, 350, 140, 32)
    button_box = pg.Rect(200, 400, 140, 32)
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('dodgerblue2')
    color = color_inactive
    active1 = False
    active2 = False
    text1 = ''
    text2 = ''
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                return None, None
            if event.type == MOUSEBUTTONDOWN:
                if input_box1.collidepoint(event.pos):
                    active1 = not active1
                else:
                    active1 = False

                if input_box2.collidepoint(event.pos):
                    active2 = not active2
                else:
                    active2 = False

                if button_box.collidepoint(event.pos):
                    if len(text1) > 1 and len(text2) > 1:
                        done = True

                color = color_active if active1 or active2 else color_inactive

            if event.type == KEYDOWN:
                if active1:
                    if event.key == K_RETURN:
                        active1 = False
                    elif event.key == K_BACKSPACE:
                        text1 = text1[:-1]
                    else:
                        text1 += event.unicode
                if active2:
                    if event.key == K_RETURN:
                        active2 = False
                    elif event.key == K_BACKSPACE:
                        text2 = text2[:-1]
                    else:
                        text2 += event.unicode

        screen.fill((30, 30, 30))
        txt_surface1 = font.render(text1, True, color)
        txt_surface2 = font.render(text2, True, color)

        width1 = max(200, txt_surface1.get_width()+10)
        width2 = max(200, txt_surface2.get_width()+10)
        input_box1.w = width1
        input_box2.w = width2

        screen.blit(txt_surface1, (input_box1.x+5, input_box1.y+5))
        screen.blit(txt_surface2, (input_box2.x+5, input_box2.y+5))
        pg.draw.rect(screen, color, input_box1, 2)
        pg.draw.rect(screen, color, input_box2, 2)

        # Draw button
        pg.draw.rect(screen, pg.Color('dodgerblue2'), button_box)
        button_text = font.render("Commencer le jeu", True, (255, 255, 255))
        screen.blit(button_text, (button_box.x + 5, button_box.y + 5))

        pg.display.flip()

    return text1, text2

# Boucle principale du jeu
while game.running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game.running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()
            for ent in entities:
                roi_x, roi_y = ent.x, ent.y
                distance_to_roi = distance(roi_x, roi_y, mouse_x, mouse_y)
                if distance_to_roi <= 30:
                    # Vérifier si le joueur peut bouger ce pion
                    if ent.color == game.current_player.color:
                        if len(ent.cases_available) == 0:
                            ent.suivre_souris = False
                            vx, vy = cases.get(ent.case).split("-")
                            if ent.last_case:
                                ent.last_case.pop()  # Retirer le dernier mouvement sauvegardé
                            ent.x = int(vx)
                            ent.y = int(vy)
                            game.selected_pion = None
                        else:
                            ent.suivre_souris = True
                            # Sauvegarder le dernier mouvement avant de suivre la souris
                            ent.last_case.append(ent.case)
                            game.selected_pion = ent
                if ent.case in zones[ent.color] and ent.fr == "soldat":
                    ent.movements.append((1, 0))
                    ent.movements.append((-1, 0))
                if ent.fr == "soldat" and ent.color == 1:
                    if ent.case not in zones[ent.color]:
                        if (1, 0) in ent.movements:
                            ent.movements.remove((1, 0))
                        if (-1, 0) in ent.movements:
                            ent.movements.remove((-1, 0))

            # Gestion du bouton "Retour" lorsqu'un pion a bougé
            if 75 < mouse_x < 175 and 780 < mouse_y < 880:
                if pg.mouse.get_pressed()[0]:
                    game.retour_arriere()

            # Gestion du bouton "Valider" pour confirmer le mouvement
            elif 570 < mouse_x < 670 and 780 < mouse_y < 880:
                if pg.mouse.get_pressed()[0]:
                    game.validate_move(ent)

        elif event.type == pg.MOUSEBUTTONUP:
            for ent in entities:
                if ent.suivre_souris:
                    event_x, event_y = ent.x, ent.y
                    b = {}
                    ent.cases_available.append(ent.case)
                    for j in range(len(ent.cases_available)):
                        pos_e = cases.get(ent.cases_available[j])
                        xx, yy = pos_e.split("-")
                        xx = int(xx)
                        yy = int(yy)
                        d = distance(event_x, event_y, xx, yy)
                        b[d] = ent.cases_available[j]

                    sorted_b = dict(sorted(b.items()))
                    ak = 0
                    for k, v in sorted_b.items():
                        if ak == 0:
                            c = cases.get(v)
                            x, y = c.split("-")
                            x = int(x)
                            y = int(y)

                            # Vérifier si la case cible n'est pas occupée par un autre pion
                            case_occupee = False
                            for autre_ent in entities:
                                if autre_ent.case == v:
                                    if autre_ent != ent:
                                        if autre_ent.color == ent.color:
                                            case_occupee = True
                                            break

                            if not case_occupee:
                                if not game.dernier_mouvement:
                                    # Déplacer le pion uniquement si la case n'est pas occupée
                                    ent.x = x
                                    ent.y = y
                                    last_case = ent.case
                                    ent.case = v
                                    ent.liste_actions = (v, ent.liste_actions)
                                    if game.dernier_mouvement is None:
                                        if ent.case != last_case:
                                            game.dernier_mouvement = (
                                                ent,
                                                ent.liste_actions[1][0],
                                            )
                                    ak = 1
                                    if (
                                        ent.case in zones[ent.color]
                                        and ent.fr == "soldat"
                                    ):
                                        ent.movements.append((1, 0))
                                        ent.movements.append((-1, 0))
                                    if ent.fr == "soldat" and ent.color == 1:
                                        if ent.case not in zones[ent.color]:
                                            if (1, 0) in ent.movements:
                                                ent.movements.remove((1, 0))
                                            if (-1, 0) in ent.movements:
                                                ent.movements.remove((-1, 0))
                                    for enti in entities:
                                        if enti.color != ent.color:
                                            if ent.case == enti.case:
                                                enti.out(entities, enti)
                                else:
                                    casee = cases[ent.case]
                                    xc, yc = casee.split("-")
                                    xc = int(xc)
                                    yc = int(yc)
                                    ent.x = xc
                                    ent.y = yc
                                for enties in entities:
                                    if len(enties.cases_available) == 0:
                                        enties.cases_dispo()
                        abc = False
                        ent.cases_dispo()
                        ent.suivre_souris = False
    if game.start == False:
        n1, n2 = get_player_names()
        p1 = Player(n1, 0)
        p2 = Player(n2, 1)
        game.players = [p1, p2]
        game.start = True
        game.current_player = game.players[0]
    if game.start == True:
        screen.fill((255, 206, 162))
        board.draw_board()

        for ent in entities:
            if ent.suivre_souris:
                ii = 1
                for case_available in ent.cases_available:
                    x, y = cases[case_available].split("-")
                    x = int(x)
                    y = int(y)
                    x1, y1 = cases[ent.case].split("-")
                    x1 = int(x1)
                    y1 = int(y1)
                    if ii == 1:
                        pg.draw.circle(screen, (255, 220, 29), (x1, y1), 10)
                    pg.draw.circle(screen, (35, 105, 255), (x, y), 40)
                    ii = 0

        # Afficher le texte du joueur actuel
        game.display_current_player()

        # Dessiner le bouton "Retour"
        pg.draw.rect(screen, (35, 105, 255), (75, 780, 100, 100), border_radius=3)
        font = pg.font.Font("Xiangqi\\fonts\\Poppins.ttf", 22)
        texte_retour = font.render("Retour", True, (255, 255, 255))
        screen.blit(texte_retour, (85, 810))

        # Dessiner le bouton "Valider"
        pg.draw.rect(screen, (35, 105, 255), (570, 780, 100, 100), border_radius=3)
        font = pg.font.Font("Xiangqi\\fonts\\Poppins.ttf", 22)
        texte_valider = font.render("Valider", True, (255, 255, 255))
        screen.blit(texte_valider, (580, 810))

        # Dessiner les pions
        for ent in entities:
            ent.draw()

        if i == 1:
            i += 1

        for ent in entities:
            if ent.suivre_souris:
                ent.x, ent.y = pg.mouse.get_pos()

    pg.display.flip()

pg.quit()
