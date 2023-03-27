import time
from pyautogui import platformModule, _normalizeXYArgs
from pynput import keyboard

execute = False
halt = False
x, y = _normalizeXYArgs(None, None)

#--------------------------------------------
def on_press(key):
    try:
        if key.char == 'a':
            global execute, x, y
            execute = not execute
            x, y = _normalizeXYArgs(None, None)
    except AttributeError:
        pass

def on_release(key):
    try:
        if key.char == 'a':
            # global execute
            # execute = not execute
            # print(execute)
            pass

    except AttributeError:
        if key == keyboard.Key.esc:
            global halt
            halt = True
            return False

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

#--------------------------------------------
while not halt:
    if execute:
        while execute:
            time.sleep(0.0005)
            platformModule._click(x, y, 'left')
    else:
        time.sleep(0.01)
