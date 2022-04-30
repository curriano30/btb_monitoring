import math
import random

PROB = 0.1

def check_si_cumple_hora_y_duracion(hora, duracion):
    if hora > 45 and duracion > 180:
        return random.uniform(0,1) > PROB
    return False

def aplica_comentario(num_subs, num_visitas, num_comment, video_previo, likes_commen):
    if num_comment < 10:
        return False
    num_subs_ = (1-math.e**-(0.00002*num_subs))
    num_visitas_ = (1-math.e**-(0.001*num_visitas))
    num_comment_ = (1-math.e**-(0.00015*num_comment**3))
    video_previo_ = (1-math.e**-(0.05*video_previo))
    likes_commen_ = 0.8*(1-math.e**-(1000*likes_commen**3))+0.2

    prob = num_subs_*num_visitas_*num_comment_*video_previo_*likes_commen_
    flag = random.uniform(0, 1) <= (prob * 2)
    print("La prob de entrar es: " + str(prob) + str(flag))

    return flag


if __name__ == "__main__":
    with(open("output/dataset_monitor.txt")) as f:
        lines = f.readlines()
        for l in lines:
            n_subs = int(l.split(',')[0])
            num_visitas = int(l.split(',')[1])
            num_comment = int(l.split(',')[2])
            video_previo = float(l.split(',')[3])
            likes_commen = float(l.split(',')[4])
            aplica_comentario(n_subs, num_visitas, num_comment, video_previo, likes_commen)


