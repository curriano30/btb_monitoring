import time

import mouse
from decision import check_si_cumple_hora_y_duracion
from webdriver import Driver, YouTube
import deepl_api as da

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


