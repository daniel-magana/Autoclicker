from pyautogui import *
import pyautogui
import time
import keyboard
import numpy as np
import random
import win32api, win32con

time.sleep(2)

#Click
def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def rand_wait():
    return np.random.uniform(0.1,0.3)
    
#Press a button
pyautogui.keyDown('1')
time.sleep('0.1')
pyautogui.keyUp('1')

#To see mouse position and RGB values at mouse position
pyautogui.displayMousePosition()

#Check if pixel is == color:
if pyautogui.pixel(100,100) == [200,200,200]:
    click(100,100)

#Loox for an image
if pyautogui.locateOnScreen('una imagen', grayscale=True, confidence=0.8) != None:
    #Found!
    time.sleep(1)

#Use a small region
while keyboard.is_pressed('q') == False:
    pic = pyautogui.screenshot(region=(100,100,200,200))
    width, height=pic.size

    for x in range(0,width,5):
        for y in range(0,height,5):
            r,g,b = pic.getpixel((x,y))

            #if r==bla: dostuff

#Program flow
while keyboard.is_pressed('q') == False:
    #Do stuff
    time.sleep(1)
