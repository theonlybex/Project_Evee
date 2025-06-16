Here's a Python script using pyautogui to open YouTube in a web browser:

import pyautogui
import time
import webbrowser

webbrowser.open('https://www.youtube.com')
time.sleep(3)
pyautogui.click(x=100, y=100)  # Click on browser window to focus