def is_case_disponible(enti ,case, entities, color):
    for ente in entities:
        if ente != enti:
            if ente.case == case:
                if ente.color != color:
                    return True
                return False
    return True
