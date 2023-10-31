from pynput.mouse import Listener
import pyautogui
import pyperclip

copy_to_clipboard = True
exit_listener = False

def on_click(x, y, button, pressed):
    global copy_to_clipboard, exit_listener
    
    if pressed:
        color = pyautogui.pixel(x, y)
        hex_color = "#{:02X}{:02X}{:02X}".format(*color)
        pyperclip.copy(hex_color)
        listener.stop()

with Listener(on_click=on_click) as listener:
    listener.join()
