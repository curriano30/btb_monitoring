import sys
import time

import pyautogui

import mouse
from decision import aplica_comentario
from webdriver import YouTube
import deepl_api as da


"""
import time

import mouse
from decision import check_si_cumple_hora_y_duracion
from webdriver import Driver, YouTube
import deepl_api as da
from canal import Canal

if __name__ == "__main__":

    dic_videos = {}
    yt = YouTube()
    yt.abrir_pestanas()
    while(1):
        for window in yt.browser.window_handles:
            print('WINDOW: ' +  window)
            yt.browser.switch_to.window(window)
            yt.actualizar_pagina()
            titulo, hora, duracion = yt.comprobar_titulo_hora_duracion_ultimo_video()
            print(f'Titulo: {titulo}   Hora: {hora}   Duracion: {duracion}')
            if hora >= 45 and hora <= 60 and titulo not in dic_videos and duracion > 100:
                time_from_last_video = yt.obtener_dia_subida_penultimo_video()
                if time_from_last_video == -1:
                    continue
                print(f'Last video uploaded: {time_from_last_video}')
                n_subs = yt.obtener_num_subs()
                print(f'Num subs: {n_subs}')
                yt.entrar_en_ultimo_video()
                n_views, n_likes, n_commen = yt.obtener_estadisticas_video()
                dic_videos[titulo] = [n_subs,n_views,n_commen,time_from_last_video,round(n_likes/n_views,3)]
                with open('/home/sergio/Documents/btb_monitoring/output/dataset_monitor.txt', 'a') as f:
                    f.write(f'{n_subs},{n_views},{n_commen},{round(time_from_last_video, 2)},{round(n_likes/n_views,3)}\n')
                with open('/home/sergio/Documents/btb_monitoring/output/videos_analyzed.txt', 'a') as f:
                    f.write(f'{titulo}\n')
                yt.volver_al_canal()
        time.sleep(5)

"""

def obtener_videos_comentados():
    """
    Obtiene los videos que ya han sido comentados con el fin de no volver a comentarlos.
    :return:
    """
    with open("input/videos_comentados.txt", "r") as f:
        videos = [video.strip() for video in f.readlines()]

    return videos

if __name__ == "__main__":

    yt = YouTube()
    yt.abrir_pestanas()
    videos_comentados = obtener_videos_comentados()

    while(1):
        for window in yt.browser.window_handles:
            yt.browser.switch_to.window(window)
            yt.actualizar_pagina()
            titulo, hora, duracion = yt.comprobar_titulo_hora_duracion_ultimo_video()
            if hora >= 1 and hora <= 2 and titulo not in videos_comentados and duracion > 100:
                time_from_last_video = yt.obtener_dia_subida_penultimo_video()
                if time_from_last_video == -1:
                    continue
                n_subs = yt.obtener_num_subs()
                yt.entrar_en_ultimo_video()
                n_views, n_likes, n_commen = yt.obtener_estadisticas_video()
                likes_ratio = round(n_likes / n_views, 3)
                if aplica_comentario(n_subs, n_views, n_commen, time_from_last_video, likes_ratio):
                    top_comment = yt.obtener_top_comentario()
                    if top_comment == '':
                        continue
                    url = yt.browser.current_url
                    yt.volver_al_canal()
                    top_comment = da.reescribir_comentario(top_comment)
                    mouse.escribir_comentario(url, top_comment)
                    with open("input/videos_comentados.txt", "a") as f:
                        f.write(titulo)
                        f.write("\n")
                    videos_comentados.append(titulo)
                    sys.exit(0)
                else:
                    yt.volver_al_canal()
                time.sleep(30*60)



