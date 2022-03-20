from pyautogui import *
import pyautogui
import time
import keyboard
import numpy as np
import random
import win32api, win32con

while keyboard.is_pressed('q') == False:
    #Loox for an image
    if pyautogui.locateCenterOnScreen('gold_c.png', grayscale=False, confidence=0.5) != None:
        #Found!
        print("🍪")
        time.sleep(0.5)
    else:
        print("no hay galleta 😥")