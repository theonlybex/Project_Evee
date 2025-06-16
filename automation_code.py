import pyautogui
import time

pyautogui.hotkey('ctrl', 't')
time.sleep(1)
pyautogui.typewrite('https://www.youtube.com/results?search_query=CSGO')
pyautogui.press('enter')