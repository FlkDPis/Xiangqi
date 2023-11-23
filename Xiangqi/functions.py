def is_case_disponible(case, entities):
    for ente in entities:
        if ente.case == case:
            return False
    return True
