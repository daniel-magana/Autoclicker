import numpy as np
import win32gui, win32ui, win32con
from threading import Thread, Lock

class WindowCapture:

    # threading properties
    stopped = True
    lock = None
    screenshot = None
    # properties
    w = 100
    h = 100
    hwnd = None
    border_pixels = 7
    titlebar_pixels = 30
    offset_x = 0
    offset_y = 0
    cookie_window = None
    window_rect = None
    temp_rect = None
    wclass = None

    # constructor
    def __init__(self, window_class=None):
        # create a thread lock object
        self.lock = Lock()

        # find the handle for the window we want to capture.
        # if no window name is given, capture the entire screen
        if window_class is None:
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            self.hwnd = win32gui.GetDesktopWindow()
            self.wclass = window_class
            self.cookie_window = win32gui.FindWindow(window_class, None)
            if not self.cookie_window:
                raise Exception('Window not found: {}'.format(window_class))
            win32gui.SetForegroundWindow(self.cookie_window)
            

    def get_screenshot(self):
        
        #Update rect
        if self.cookie_window == None:
            self.temp_rect = win32gui.GetWindowRect(self.hwnd)
        else:
            self.cookie_window = win32gui.FindWindow(self.wclass, None)
            self.temp_rect = win32gui.GetWindowRect(self.cookie_window)

        #If the new rect is different
        if self.window_rect == None or self.window_rect != self.temp_rect:
            self.window_rect = self.temp_rect

            # get the window size
            #window_rect = win32gui.GetWindowRect(self.hwnd)
            self.w = self.window_rect[2] - self.window_rect[0]
            self.h = self.window_rect[3] - self.window_rect[1]

            # account for the window border and titlebar and cut them off
            self.w = int((self.w - (self.border_pixels * 2))*0.6)
            self.h = self.h - self.titlebar_pixels - self.border_pixels

            # set the cropped coordinates offset so we can translate screenshot
            # images into actual screen positions
            self.offset_x = self.window_rect[0] + self.border_pixels
            self.offset_y = self.window_rect[1] + self.titlebar_pixels

        # get the window image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.offset_x, self.offset_y), win32con.SRCCOPY)

        # convert the raw data into a format opencv can read
        #dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        # free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # drop the alpha channel, or cv.matchTemplate() will throw an error like:
        #   error: (-215:Assertion failed) (depth == CV_8U || depth == CV_32F) && type == _templ.type() 
        #   && _img.dims() <= 2 in function 'cv::matchTemplate'
        img = img[...,:3]

        # make image C_CONTIGUOUS to avoid errors that look like:
        #   File ... in draw_rectangles
        #   TypeError: an integer is required (got type tuple)
        # see the discussion here:
        # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109
        img = np.ascontiguousarray(img)

        return img

    # find the name of the window you're interested in.
    # once you have it, update window_capture()
    # https://stackoverflow.com/questions/55547940/how-to-get-a-list-of-the-name-of-every-open-window
    @staticmethod
    def list_window_names():
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)

    # translate a pixel position on a screenshot image to a pixel position on the screen.
    # pos = (x, y)
    # WARNING: if you move the window being captured after execution is started, this will
    # return incorrect coordinates, because the window position is only calculated in
    # the __init__ constructor.
    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)

    # threading methods
    
    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        # TODO: you can write your own time/iterations calculation to determine how fast this is
        while not self.stopped:
            # get an updated image of the game
            screenshot = self.get_screenshot()
            # lock the thread while updating the results
            self.lock.acquire()
            self.screenshot = screenshot
            self.lock.release()
