import pygame as pg
from pygame.locals import *
from variables import *
from math import *

# Initialisation de certaines variables pour le jeu
screen = pg.display.set_mode((730, 800))
def distance(x1, y1, x2, y2):
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Class Case qui permet de savoir où sont les cases
class Case:
    def __init__(self, pos, name):
        self.x, self.y = pos.split("-")
        self.name = name


# Class Players qui permet de créer les joueurs
class Players:
    def __init__(self, name, pions):
        self.name = name
        self.points = 0
        self.pions = pions


# Class Pion qui crée les pions du jeu avec leur nom etc
class Pion:
    def __init__(self, pos, fr, color, moves):
        self.fr = fr
        self.name = pion.get(self.fr)
        self.x, self.y = pos
        self.out = False
        self.color = color
        self.case = cases.get(str(self.x) + "-" + str(self.y))
        if self.out:
            self.out()
        self.movements = moves
        self.suivre_souris = False
        self.cases_available = []
        for j in range(len(self.movements)):
            a, b = self.movements[j][0], self.movements[j][1]
            n_x, n_y = self.x + (a * 73), self.y + (b * 73)
            for k, v in cases.items():
                if str(n_x) + "-" + str(n_y) == v and k in palais[self.color]:
                    self.cases_available.append(k)

    def draw(self, screen):
        chemin = None
        c = 1 if self.color == 0 else 0
        font = pg.font.Font(
            chemin,
            35,
        )
        ecrit = font.render(self.name, True, (couleurs[c]))

        surface_size = max(ecrit.get_width(), ecrit.get_height()) + 25
        cercle = pg.Surface((surface_size, surface_size), pg.SRCALPHA)

        center = (surface_size // 2, surface_size // 2)

        pg.draw.circle(cercle, couleurs[c], center, surface_size // 2 - 1)
        pg.draw.circle(cercle, couleurs[self.color], center, surface_size // 2 - 3)

        text_rect = ecrit.get_rect(center=center)
        cercle.blit(ecrit, text_rect.topleft)
        screen.blit(cercle, (self.x - surface_size // 2, self.y - surface_size // 2))

    def out(self, screen):
        game.pions.pop(game.pions[self.color][self.name])
        self.name = ""
        screen.blit(self.name, (self.x, self.y))


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

# Test
entities = []
for col, entite in pions.items():
    for g in range(len(entite)):
        print(entite[g])
        tr = cases.get(spawn[col].get(entite[g])[0])
        del spawn[col][entite[g]][0]
        w,x = tr.split("-")
        pos = (int(w), int(x))
        couleur = 0 if col == "white" else 1
        mov = mouvs.get(pion.get(entite[g]))
        pion_entite = Pion(pos, entite[g], couleur, mov)
        entities.append(pion_entite)
        print(1)

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
                    ent.suivre_souris = True
        elif event.type == pg.MOUSEBUTTONUP:
            for ent in entities:
                if ent.suivre_souris:
                    event_x, event_y = ent.x, ent.y
                    b = {}
                    for j in range(len(ent.cases_available)):
                        pos_e = cases.get(ent.cases_available[j])
                        xx, yy = pos_e.split("-")
                        xx = int(xx)
                        yy = int(yy)
                        d = distance(event_x, event_y, xx, yy)
                        b[d] = ent.cases_available[j]
                        print(ent.cases_available)

                    sorted_b = dict(sorted(b.items()))
                    ak = 0
                    for k, v in sorted_b.items():
                        if ak == 0:
                            c = cases.get(v)
                            x, y = c.split("-")
                            x = int(x)
                            y = int(y)
                            ent.x = x
                            ent.y = y
                            ent.case = cases.get(str(ent.x) + "-" + str(ent.y))
                            ak = 1
                    ent.cases_available = []
                    for j in range(len(ent.movements)):
                        g_x, h_y = ent.movements[j][0], ent.movements[j][1]
                        n_x, n_y = ent.x + (g_x * 73), ent.y + (h_y * 73)
                        for k, v in cases.items():
                            if entite.fr == 'roi':
                                if k in palais[entite.color]:
                                   ent.cases_available.append(k)
                            elif str(n_x) + "-" + str(n_y) == v:
                                ent.cases_available.append(k)
                    ent.suivre_souris = False
                else:
                    ent.suivre_souris = False

    screen.fill((255, 206, 162))
    board.draw_board()
    for ent in entities:
        ent.draw(screen)
    if i == 1:
        print(cases)
        print(pions)
        i += 1
    for ent in entities:
        if ent.suivre_souris:
            ent.x, ent.y = pg.mouse.get_pos()
        
    pg.display.flip()

pg.quit()
