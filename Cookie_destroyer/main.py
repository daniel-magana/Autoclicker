import cv2 as cv
import numpy as np
import os
import win32api, win32con
import time
from windowcapture import WindowCapture
from vision import Vision
from hsvfilter import HsvFilter
import pyautogui
import keyboard

#Click
def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(np.random.uniform(0.05,0.15))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("Debug? Y/N")
debug = keyboard.read_key()
if debug == 'y':
    debug = True
else:
    debug = False

# initialize the WindowCapture class
wincap = WindowCapture('Chrome_WidgetWin_1')
# initialize the Vision class
vision_golden = Vision('golden_processed.jpg')
# initialize the trackbar window
#vision_golden.init_control_gui()

#Start the threads
wincap.start()
vision_golden.start()

# HSV filter
hsv_filter = HsvFilter(19, 210, 214, 28, 255, 255, 115, 0, 62, 0)

#WindowCapture.list_window_names()

loop_time = time.time()
freeze = False
auto_golden = False
auto_mode = False
golden_cd = 2
auto_cd = 0.08
timer = 0
timer2 = 0

gold_cookie_cont = 0

while(True):

    # if we don't have a screenshot yet, don't run the code below this point yet
    if wincap.screenshot is None:
        continue

    # get an updated image of the game
    if not freeze:
        screenshot = wincap.screenshot
    #cv.imshow('Ss', screenshot)

    vision_golden.update(screenshot)

    # pre-process the image
    processed_image = vision_golden.apply_hsv_filter(screenshot, hsv_filter)



    # get click positions of rectangles
    click_pos = vision_golden.get_click_points()

    # debug the loop rate
    deltaTime = time.time() - loop_time
    #print('FPS {}'.format(1 / deltaTime))
    loop_time = time.time()

    # click golden cookies
    timer += deltaTime
    timer2 += deltaTime
    #if timer > golden_cd and len(click_pos)>0:
        #print(click_pos[0])
        #print(wincap.get_screen_position(click_pos[0]))
    if timer > golden_cd and auto_golden and len(click_pos)>0:
            print("Gold!")
            gold_cookie_cont += 1
            pyautogui.click(wincap.get_screen_position(click_pos[0]))
            timer = 0
    if auto_mode and timer2 > auto_cd:
        galleton_x = int(wincap.w/5)
        galleton_y = int(wincap.h/2)
        galleton = (galleton_x, galleton_y)
        pyautogui.click(wincap.get_screen_position(galleton))
        auto_cd = np.random.uniform(0.001, 0.005)
        timer2 = 0

    # display the processed image
    if debug:
        # do object detection
        rectangles = vision_golden.find(processed_image, 0.245)

        # draw the detection results onto the original image
        output_image = vision_golden.draw_rectangles(screenshot, rectangles)
        
        cv.imshow('Processed', processed_image)
        cv.imshow('Matches', output_image)

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    press = cv.waitKey(10)
    if keyboard.is_pressed('p'):
        freeze = not freeze
        print("Freeze", freeze)
        time.sleep(0.05)
    elif keyboard.is_pressed('a'):
        auto_mode = not auto_mode
        print("Autoclick mode", auto_mode)
        time.sleep(0.05)
    elif keyboard.is_pressed('g'):
        auto_golden = not auto_golden
        print("Catch golden cookies", auto_golden)
        time.sleep(0.05)
    elif keyboard.is_pressed('q'):
        wincap.stop()
        vision_golden.stop()
        cv.destroyAllWindows()
        break

print('The grandma is resting.')
print('%i golden cookies clicked.' % gold_cookie_cont)
print("Press enter to close the window.")
keyboard.wait('enter')