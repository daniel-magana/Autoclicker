from PIL.Image import Image
import cv2 as cv
import numpy as np
import pyautogui
from PIL import ImageGrab
import win32gui, win32ui, win32con

#https://stackoverflow.com/questions/38970354/win32gui-findwindow-not-finding-window

haystack_img = cv.imread('ss3.png', cv.IMREAD_UNCHANGED)
needle_img = cv.imread('gold_og.png', cv.IMREAD_UNCHANGED)

result = cv.matchTemplate(haystack_img,needle_img, cv.TM_CCOEFF_NORMED)


#One result
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

print("Best match pos: "+ str(max_loc))
print("Best match confidence: "+ str(max_val))

needle_w = needle_img.shape[1]
needle_h = needle_img.shape[0]

threshold = 0.8
if threshold <= max_val:
    print("Found")

    top_left = max_loc
    bot_right = (top_left[0] + needle_w, top_left[1] + needle_h)

    cv.rectangle(haystack_img, top_left, bot_right,
                color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

    cv.imshow("Result", haystack_img)
    cv.waitKey()

    #cv.imwrite('result.png', haystack_img)
else:
    print("Not found")

#More than one result, rectangle aggroupation
threshold=0.85

locations = np.where(result >= threshold)

locations = list(zip(*locations[::-1]))

rectangles = []
for loc in locations:
    rect = [int(loc[0]), int(loc[1]), needle_w, needle_h]
    rectangles.append(rect)
    rectangles.append(rect)

rectangles, wheights = cv.groupRectangles(rectangles, 1, 0.5)

#Program flow

while(True):
    #ss = pyautogui.screenshot()
    #ss = ImageGrab.grab()

    ss = np.array(ss)
    ss = cv.cvtColor(ss, cv.COLOR_RGB2BGR)
    cv.imshow('Computer vision')

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break