import decimal
import time
import threading
import random

from pynput import keyboard
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import pyautogui
import pyperclip

delay = float(decimal.Decimal(random.randrange(1, 2)) / 100)
button = Button.left
start_stop_key = KeyCode(char='`')
exit_key = KeyCode(char='C')
start = False


class ClickMouse(threading.Thread):
    def __init__(self, delay, button):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running:

                pyautogui.keyDown('shift')
                global start
                if start:

                    pyautogui.hotkey('ctrl', 'c')
                    text = pyperclip.paste()

                    with open("item.txt", "w") as f:
                        f.write(text)
                    print("copied")
                    desire = open('desires.txt', 'r')
                    lines = desire.readlines()

                    with open('item.txt') as f:
                        for line in lines:
                            if line.lower() in f.read().lower():
                                print("true")
                                pyperclip.copy('')
                                pyautogui.keyUp('shift')
                                exit(self)

                            f.seek(0)
                else:
                    start = True




                time.sleep(self.delay)

                mouse.click(self.button)
                print("CLICK")

            time.sleep(0.1)


mouse = Controller()
click_thread = ClickMouse(delay, button)
click_thread.start()


def on_press(key):
    if key == start_stop_key:
        if click_thread.running:
            click_thread.stop_clicking()
        else:
            click_thread.start_clicking()
    elif key == exit_key:
        pyautogui.keyUp('shift')
        click_thread.exit()
        listener.stop()


with Listener(on_press=on_press) as listener:
    listener.join()
