from math import *


def is_case_disponible(enti, case, entities, color):
    for ente in entities:
        if ente != enti:
            if ente.case == case:
                if ente.color != color:
                    return True
                return False
    return True


def distance(x1, y1, x2, y2):
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
