import time
import pyautogui

hours   = 8
minutes = 60
for i in range(hours*minutes):
    pyautogui.move(10,10)
    pyautogui.move(-10,-10)
    time.sleep(60)
    print(f'{time.strftime("%Y.%m.%d %H:%M:%S")} i:{i of {hours*minutes}}')
