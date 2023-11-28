from pynput.keyboard import Controller, Key
from datetime import datetime
import time, os, sys

os.system("cls" if os.name == "nt" else "clear")

def pause_current_audio(delay):
    keyboard = Controller()

    time.sleep(delay)

    keyboard.press(Key.media_play_pause)
    keyboard.release(Key.media_play_pause)

    current_time = datetime.now().strftime("%H:%M:%S")
    print(f'Exited at {current_time}')

    sys.exit()

while True:
    user_input = input("Enter time until pause in minutes: ")

    if user_input.isdigit():
        pause_current_audio(int(user_input) * 60)
    else:
        print("Not an integer...")
        time.sleep(2)
        os.system("cls" if os.name == "nt" else "clear")