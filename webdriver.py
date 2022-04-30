import os
import sys
import time

import pyautogui
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium import webdriver
import urllib
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

class Driver():

    def __init__(self, puerto=None):

        self.browser = self.iniciar_conexion_geckodriver()

    def iniciar_conexion_geckodriver(self):
        """
        Crea la conexión mediante ChromeDriver al navegador de Chrome por el puerto correspondiente
        :return:
        """
        path = os.path.abspath(os.getcwd())
        options = webdriver.FirefoxOptions()
        options.add_argument('--disable-logging')
        w = webdriver.Firefox(executable_path="/home/sergio/Documents/btb_monitoring/geckodriver")
        w.maximize_window()
        return w

    def iniciar_conexion_remoto(self, puerto):

        w = webdriver.Remote(f'http://localhost:{puerto}',
                                  desired_capabilities=DesiredCapabilities.FIREFOX)
        w.maximize_window()

        return w



class YouTube(Driver):

    def __init__(self, puerto=None):

        def leer_urls():
            f = open('/home/sergio/Documents/btb_monitoring/input/canales.txt', 'r')
            return [canal.strip() for canal in f.readlines()]


        super().__init__(puerto)
        self.browser.get("https://youtube.com")
        time.sleep(3)
        elem = self.browser.find_elements(By.CLASS_NAME, "style-scope.ytd-consent-bump-v2-lightbox.style-primary.size-default")[1]
        elem.click()
        time.sleep(2)
        self.canales = leer_urls()


    def actualizar_pagina(self):
        """
        Renderiza de nuevo la página sin necesidad de recargarla para comprobar si se ha subido algún nuevo video.
        :return:
        """
        time.sleep(3)
        i = 0
        while(1):
            if i == 10:
                print("actualizar pagina: No llegó a cargar la pagin para clickar en video")
                sys.exit(0)
            try:
                elem = self.browser.find_element(By.CLASS_NAME,'style-scope.ytd-c4-tabbed-header-renderer.iron-selected')
                break
            except:
                time.sleep(4)
                i += 1
                continue
        elem.click()

    def comprobar_titulo_hora_duracion_ultimo_video(self):
        """
        Comprueba la hora y la duracion del último video subido
        :return:
        """
        time.sleep(3)
        details = self.browser.find_element(By.ID, 'details').text
        if 'Premieres' in details:
            return -1, -1, -1
        elems = self.browser.find_elements(By.CLASS_NAME, 'style-scope.ytd-grid-renderer')

        # obtenemos el primer video
        for elem in elems:
            if elem.text == '' or len(elem.text.split('\n')) > 4:
                continue
            else:
                break
        # si es una longitud de 3 es que es un short
        if len(elem.text.split('\n')) == 3:
            return -1, -1, -1
        i = 0
        for line in elem.text.split('\n'):
            if i == 0:
                minutes = int(line.split(':')[0])*60
                seconds = int(line.split(':')[1])
                duracion = minutes + seconds
                i += 1
            elif i == 1:
                titulo = line
                i += 1
            elif i == 2:
                i += 1
                continue
            elif i == 3:
                if 'streamed' in line.lower() or 'premiere' in line.lower():
                    return -1, -1, -1
                value = int(line.split(' ')[-3])
                range = line.split(' ')[-2]
                if "second" in range:
                    value = 0
                elif "minutes" in range:
                    value = 0
                elif "hour" in range:
                    pass
                elif "day" in range:
                    value *= 24
                else:
                    value = 7*24
                video_previo = value
                i += 1

        try:
            return titulo, video_previo, duracion
        except:
            return -1, -1, -1

    def volver_al_canal(self):
        """
        Retrocede al canal de nuevo para la prox monitorizacion
        :return:
        """
        time.sleep(3)
        self.browser.find_element(By.CLASS_NAME, 'style-scope.ytd-video-owner-renderer').click()
        time.sleep(5)
        try:
            self.browser.find_elements(By.CLASS_NAME, 'style-scope.tp-yt-paper-tab')[1].click()
        except:
            print("A")

    def obtener_dia_subida_penultimo_video(self):
        """
        Obtiene el numero de dias que han pasado desde que subio el ultimo video
        :return:
        """
        time.sleep(2)
        details = self.browser.find_elements(By.ID, 'details')[1].text
        time_ = details.split('\n')[2]
        try:
            value = int(time_.split(' ')[-3])
            range = time_.split(' ')[-2]
        except:
            return -1

        if "hour" in range:
            value /= 60
        elif "day" in range:
            pass
        elif "week" in range:
            value *= 7
        elif "month" in range:
            value *= 28
        elif "minute" in range:
            value = 0
        else:
            value = 500

        return value

    def obtener_num_subs(self):
        time.sleep(2)
        details = self.browser.find_element(By.ID, 'subscriber-count').text
        try:
            value = int(details.split(' ')[0].replace('.', ''))
        except:
            value = float(details.split(' ')[0][:-1])
            unidad = details.split(' ')[0][-1]
            if 'M' in unidad:
                value = value * 1000000
            elif 'K' in unidad:
                value = value * 1000
        return int(value)

    def entrar_en_ultimo_video(self):
        """
        Entra en el último video
        :return:
        """
        time.sleep(2)
        elems = self.browser.find_elements(By.ID, 'thumbnail')
        for elem in elems:
            if elem.get_attribute('href'):
                elem.click()
                break

    def obtener_x_y_from_comment_and_submit(self):
        """
        Obtiene las coordenadas para escribir un comentario como para comentar
        :return:
        """
        time.sleep(3)
        self.browser.execute_script("window.scrollTo(0,500)")
        time.sleep(3)
        elem = self.browser.find_element(By.CLASS_NAME, 'style-scope.ytd-comment-simplebox-renderer')
        x = elem.rect['x']+150.0
        y = elem.rect['y']-500+125
        return x, y


        #element.getSize().getWidth()

    def obtener_estadisticas_video(self):
        """
        Obtiene estadisticas de un video:
            - numero de visualizaciones
            - numero de likes
            - número de comentarios
            -
        :return:
        """
        time.sleep(3)
        self.browser.execute_script("window.scrollTo(0,500)")
        time.sleep(5)
        i = 0
        while(1):
            if i == 12:
                self.browser.get(self.browser.current_url)
                time.sleep(5)
                print("Obtener estadisticas: primer while(1) - No llegó a cargar la pagin para clickar en video")
                sys.exit(0)
            try:
                n_comments = int(self.browser.find_element(By.CLASS_NAME, 'style-scope.ytd-comments-header-renderer')
                                 .text.split('\n')[0]
                                 .split(' ')[0])
                break
            except:
                self.browser.execute_script("window.scrollTo(0,500)")
                time.sleep(3)
                i += 1
                continue
        try:
            n_views = int(self.browser.find_element(By.CLASS_NAME, 'view-count.style-scope.ytd-video-view-count-renderer')
                        .text.split(' ')[0].replace(',',''))
        except:
            print("A")

        try:
            n_likes = int(self.browser.find_element(By.CLASS_NAME, 'style-scope.ytd-video-primary-info-renderer')
                          .text.split('\n')[-4])
        except:
            n_likes = int(float(self.browser.find_element(By.CLASS_NAME, 'style-scope.ytd-video-primary-info-renderer')
                          .text.split('\n')[-4][:-1])*1000)

        return n_views, n_likes, n_comments

    def obtener_top_comentario(self):
        """
        Lee los comentarios más likeados por los usuarios y su texto para después crear uno igual.
        :return:
        """
        time.sleep(3)
        self.browser.execute_script("window.scrollTo(0,500)")
        time.sleep(10)
        elems = self.browser.find_elements(By.ID, 'comment')
        final_comments = set()
        i = 0
        for elem in elems:
            if elem.text != '' and len(elem.text.split('\n')) >= 4:
                i += 1
                lineas = elem.text.split('\n')
                comment = lineas[2:-2]
                c = ""
                for line in comment:
                    c += line + "\n"
                try:
                    likes = int(lineas[-2])
                except:
                    continue
                final_comments.add((i, likes, c, len(c)))
                if i >= 50:
                    break
        comments = list(final_comments)
        comments.sort(key=lambda x : x[0])
        f_c = ''
        for c in comments[6:]:
            if c[3] > 200:
                continue
            f_c = c[2]
            break

        f_c = f_c.replace('\n\n\n\n', '\n')
        f_c = f_c.replace('\n\n\n', '\n')
        f_c = f_c.replace('\n\n', '\n')

        return f_c

    def abrir_pestanas(self):
        """
        Pasa una lista de Canales y los abre en distintas pestañas
        :return:
        """
        # obtenemos el tab primero
        p = self.browser.current_window_handle

        # abrimos tantas pestañas como URLs hayamos mandado
        if len(self.canales) > 1:
            for canal in self.canales:
                self.browser.execute_script(f"window.open('{canal}')")

        # cambiamos a la pestaña principal
        self.browser.switch_to.window(p)

        # obenemos la URL de los partidos
        self.browser.get(self.canales[0])

        for window in self.browser.window_handles:
            self.browser.switch_to.window(window)
            self.browser.maximize_window()







            # lineas = elem.text.split('\n')
            # comment = lineas[2]
            # likes = int(lineas[3])

# todo mejorar escritura de comentario que falla (quita letras)
# todo quitar \n de los comentarios que queda a veces raro el comentario
# revisar script 'Comentar'





