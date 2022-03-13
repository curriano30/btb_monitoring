from selenium.webdriver.common.by import By
import webbrowser
import urllib.request

class Canal:
    def __init__(self):
        self.atributos = {}

    def actualizar_informacion_canal(self):
        """
        Si sube algún nuevo video y no está registrado en el fichero de información se añade para cuando
        se vuelvan a actualizar las estadisticas.
        :return:
        """

    def extraer_atributos_canal(self):
        """
        Según la URL del canal obtendrá de un fichero la información asociada a ese canal.
        Busca crear los atributos de un canal para luego en la funcion aplica_comentario
        estudiar si aplica o no un comentario.
        :return:
        """
        # se ejecuta cada vez para un canal
        # leer toda la informacion de interés para luego extraer atributos
        # estudiarla como atributos para luego poder aplicar la función aplica_comentario
        pass

    def aplica_comentario(self) -> bool:
        """
        Algoritmo que dice segun unos parámetros de entrada, si un video aplica o no para comentarse
        :return:
        """


