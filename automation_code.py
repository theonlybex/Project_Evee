import pyautogui
import time

# Open Word
pyautogui.hotkey('win', 'r')
pyautogui.write('winword')
pyautogui.press('enter')
time.sleep(2)

# Create new blank document
pyautogui.hotkey('ctrl', 'n')
time.sleep(1)

# Write capabilities
capabilities = "I can automate tasks like opening applications, typing text, clicking buttons, navigating menus, filling forms, and more using Python scripts with libraries like pyautogui, pywinauto, and selenium."
pyautogui.write(capabilities)