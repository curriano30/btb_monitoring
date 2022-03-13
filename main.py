import time

import pyautogui

import mouse
from decision import check_si_cumple_hora_y_duracion
from webdriver import Driver, YouTube
import deepl_api as da
from canal import Canal

if __name__ == "__main__":

    yt = YouTube()
    canales = ['https://www.youtube.com/c/elrubiusOMG/videos','https://www.youtube.com/c/Paracetamor', 'https://www.youtube.com/user/byCalitos79/videos']
    for canal in canales:
        yt.browser.get(canal)
        yt.actualizar_pagina()
        hora, duracion = yt.comprobar_hora_duracion_ultimo_video()
        if check_si_cumple_hora_y_duracion(hora, duracion):
            yt.entrar_en_ultimo_video()
            top_comment = yt.obtener_top_comentario()
            print(top_comment)
            top_comment = da.reescribir_comentario(top_comment)
            print(top_comment)
            mouse.escribir_comentario(yt.browser.current_url, top_comment)

    # pyautogui.moveTo(500,500)
    # yt = None
    # canales = ['https://www.youtube.com/c/elrubiusOMG/videos','https://www.youtube.com/c/Paracetamor', 'https://www.youtube.com/user/byCalitos79/videos']
    # for canal in canales:
    #     mouse.escribir_comentario('https://www.youtube.com/watch?v=h0EmwU7upVY', 'hola', pos_x=10, pos_y=10)
    #     yt.browser.get(canal)
    #     hora, duracion = yt.comprobar_hora_duracion_ultimo_video()
    #     yt.actualizar_pagina()
    #     yt.entrar_en_ultimo_video()
    #     x, y = yt.obtener_x_y_from_comment_and_submit()
    #     top_comment = yt.obtener_top_comentario()
    #     print(top_comment)
    #     top_comment = da.reescribir_comentario(top_comment)
    #     print(top_comment)
