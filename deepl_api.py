import deepl
import re
import os


# Function to convert
def lista_a_string(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += f'{ele.strip()} '

        # return string
    return str1

def eliminar_tildes(text):
    text = text.replace('á', 'a')
    text = text.replace('é', 'e')
    text = text.replace('í', 'i')
    text = text.replace('ó', 'o')
    text = text.replace('ú', 'u')
    return text

def filtrar_texto(text):
    text = eliminar_tildes(text)
    list = re.findall('[a-zA-Z0-9_ .]+', text)
    return lista_a_string(list)

def traducir_ingles_a_espanol(text):
    translator = deepl.Translator('d6b7f5f4-2ba9-c391-1acd-edf91485cbcb:fx')
    return translator.translate_text(text, target_lang="ES").text

def traducir_espanol_a_ingles(text):
    translator = deepl.Translator('d6b7f5f4-2ba9-c391-1acd-edf91485cbcb:fx')
    return translator.translate_text(text, target_lang="EN-GB").text

def reescribir_comentario(text):
    text = traducir_espanol_a_ingles(text)
    return traducir_ingles_a_espanol(text)


