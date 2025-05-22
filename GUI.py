import webbrowser
import pyautogui
import time 

#open youtube
webbrowser.open("www.youtube.com")

#wait for the browser to load
time.sleep(5)

#press tab to get to search bar
for _ in range(4):
    pyautogui.press("tab")
    time.sleep(0.2)

#write and enter
pyautogui.write("lofi music")
pyautogui.press("enter")