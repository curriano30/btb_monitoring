import sys
import webbrowser
import pyautogui
import time


urls = ["https://www.youtube.com/watch?v=wOzdGoSKfw0", "https://www.youtube.com/watch?v=DGSgJVuEFrM",
        "https://www.youtube.com/watch?v=n-f56zl1oLU"]


def abir_video(url):
    webbrowser.open(url)
    time.sleep(20)


def escribir_comentario(url, comment, pos_x=None, pos_y=None):
    time_to_sleep = 3
    abir_video(url)
    y = localizacion_imagen_perfil(url)
    time.sleep(time_to_sleep)
    pyautogui.click()
    time.sleep(time_to_sleep)
    for c in comment:
        pyautogui.write(c)
    localizacion_boton_comentar(y)
    pyautogui.click()

def localizacion_imagen_perfil(url):
    time_to_sleep = 5
    time.sleep(time_to_sleep)
    pyautogui.moveTo(153, 200)
    time.sleep(1)
    pyautogui.click()
    # Go to example.com
    pyautogui.scroll(-3)
    time.sleep(time_to_sleep)
    j = 0
    for i in range(0, 200, 2):
        print(pyautogui.pixel(130, 500 + i))
        pyautogui.moveTo(130, 500 + i)
        if pyautogui.pixel(130, 500 + i).red + pyautogui.pixel(130, 500 + i).green > 300 and\
                pyautogui.pixel(130, 500 + i).blue < 75 :
            j += 1
            if j == 2:
                break
    time.sleep(time_to_sleep)
    pyautogui.moveTo(250, 500 + i)
    time.sleep(time_to_sleep)
    return 500+i

def localizacion_boton_comentar(y):
    time_to_sleep=3
    time.sleep(time_to_sleep)
    pyautogui.moveTo(850, y)
    j = 0
    for i in range(0, 120, 1):
        pyautogui.moveTo(850, y + i)
        print(pyautogui.pixel(850, y + i))
        if pyautogui.pixel(850, y + i).blue == 212:
            j += 1
            if j == 5:
                break
    pyautogui.moveTo(850, y + i)

