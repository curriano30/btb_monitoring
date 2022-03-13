import random

PROB = 0.1

def check_si_cumple_hora_y_duracion(hora, duracion):
    if hora > 45 and duracion > 180:
        return random.uniform(0,1) > PROB
    return False
