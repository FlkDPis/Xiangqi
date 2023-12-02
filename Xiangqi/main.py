import pygame as pg
from pygame.locals import *
from variables import *
from math import *
from functions import is_case_disponible

# Initialisation de certaines variables pour le jeu
screen = pg.display.set_mode((730, 800))


def distance(x1, y1, x2, y2):
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Class Case qui permet de savoir où sont les cases
class Case:
    def __init__(self, pos, name):
        self.x, self.y = pos.split("-")
        self.name = name


# Class Players qui permet de créer les joueurs
class Players:
    def __init__(self, name, pions, col):
        self.name = name
        self.gagne = False
        self.pions = pions
        self.color = col
        self.tour = 0


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
        if self.outed:
            self.out()
        self.movements = moves
        if self.color == 0 and self.fr == "soldat":
            self.movements = [(0, -1)]
        self.suivre_souris = False
        self.cases_available = []
        for j in range(len(self.movements)):
            a, b = self.movements[j][0], self.movements[j][1]
            n_x, n_y = self.x + (a * 73), self.y + (b * 73)
            for k, v in cases.items():
                if is_case_disponible(self, k, entities, self.color):
                    if str(n_x) + "-" + str(n_y) == v:
                        if self.fr == "roi" or self.fr == "conseiller":
                            if k in palais[self.color]:
                                self.cases_available.append(k)
                        else:
                            self.cases_available.append(k)

    def draw(self):
        chemin = "SIMSUN.ttf"
        c = 1 if self.color == 0 else 0
        font = pg.font.Font(
            chemin,
            35,
        )
        ecrit = font.render(self.name, True, (couleurs[self.color]))

        surface_size = max(ecrit.get_width(), ecrit.get_height()) + 30
        cercle = pg.Surface((surface_size, surface_size), pg.SRCALPHA)

        center = (surface_size // 2, surface_size // 2)

        pg.draw.circle(cercle, couleurs[self.color], center, surface_size // 2 - 1)
        pg.draw.circle(cercle, couleurs[c], center, surface_size // 2 - 3)

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

    def run(self):
        pg.init()
        self.running = True


# Initialisation des class
board = Board()
game = Game(board, ["Arthur", "Arthur"], pions, cases)


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
                    if len(ent.cases_available) == 0:
                        ent.suivre_souris = False
                        vx, vy = cases.get(ent.case).split("-")
                        vx = int(vx)
                        vy = int(vy)
                        ent.x = vx
                        ent.y = vy
                    else:
                        ent.suivre_souris = True
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
                                        case_occupee = True
                                        break

                            if not case_occupee:
                                # Déplacer le pion uniquement si la case n'est pas occupée
                                ent.x = x
                                ent.y = y
                                ent.case = v
                                ent.last_case.append(v)
                                ent.liste_actions = (v, ent.liste_actions)
                                ak = 1
                                for enti in entities:
                                    if enti != ent:
                                        if ent.case == enti.case:
                                            enti.out(entities, enti)
                                if ent.case in zones[ent.color] and ent.fr == "soldat":
                                    ent.movements.append((1, 0))
                                    ent.movements.append((-1, 0))

                    ent.cases_available = []
                    abc = False
                    for j in range(len(ent.movements)):
                        g_x, h_y = ent.movements[j][0], ent.movements[j][1]
                        n_x, n_y = ent.x + (g_x * 73), ent.y + (h_y * 73)
                        for k, v in cases.items():
                            if str(n_x) + "-" + str(n_y) == v:
                                if is_case_disponible(ent, k, entities, ent.color):
                                    if ent.fr == "roi" or ent.fr == "conseiller":
                                        if k in palais[ent.color]:
                                            ent.cases_available.append(k)
                                    else:
                                        ent.cases_available.append(k)
                        ent.suivre_souris = False

    screen.fill((255, 206, 162))
    board.draw_board()

    for ent in entities:
        if ent.suivre_souris:
            ii = 1
            for case_available in ent.cases_available:
                x, y = cases[case_available].split("-")
                x = int(x)
                y = int(y)
                x1,y1 = cases[ent.case].split("-")
                x1 = int(x1)
                y1 = int(y1)
                if ii == 1:
                    pg.draw.circle(screen, (255, 220, 0), (x1, y1), 10)
                pg.draw.circle(screen, (0, 147, 255), (x, y), 10)
                ii = 0
                    

    for ent in entities:
        ent.draw()

    if i == 1:
        i += 1

    for ent in entities:
        if ent.suivre_souris:
            ent.x, ent.y = pg.mouse.get_pos()

    pg.display.flip()

pg.quit()
