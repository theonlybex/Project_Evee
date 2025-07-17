import pyautogui
import time

# Open the Start menu
pyautogui.hotkey('winleft')
time.sleep(1)

# Type "Word" to search for Microsoft Word
pyautogui.write('Word')
time.sleep(1)

# Press Enter to open Microsoft Word
pyautogui.press('enter')
time.sleep(3)

# Wait for Word to open and create a new document
pyautogui.hotkey('ctrl', 'n')