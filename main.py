from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, KeyCode, Controller as KeyboardController
from pynput import keyboard as mainKeyboard
import pyautogui
import enum
from time import sleep, time
import math
import datetime
from random import random


class State(enum.Enum):
    PAUSED = 1
    QUITTING = 2
    RECORDING = 3
    RUNNING = 4


mouse = MouseController()
keyboard = KeyboardController()
current_state = State.PAUSED
click_locations = []
clicks_per_second = 6
click_interval = 1.0 / clicks_per_second
last_click_time = 0


def on_press(key):
    a = 1  # do nothing


def on_release(key):
    global current_state
    if key == KeyCode.from_char('r'):
        if current_state is not State.RECORDING:
            current_state = State.RECORDING
            print("RECORDING: hover over click location and press T to save...")
        else:
            current_state = State.PAUSED
            print(f"PAUSED: recorded {len(click_locations)} locations, waiting for command... (press I for help)")
    elif key == Key.space:
        if current_state is not State.RUNNING:
            if len(click_locations) > 0:
                current_state = State.RUNNING
                print(f"RUNNING: clicking {len(click_locations)} locations")
            else:
                current_state = State.PAUSED
                print("PAUSED: no locations to click, please record new locations... (press I for help)")
        else:
            current_state = State.PAUSED
            print("PAUSED: waiting for command... (press I for help)")
    elif key == KeyCode.from_char('i'):
        print_instructions()
    elif key == KeyCode.from_char('t'):
        if current_state is State.RECORDING:
            pos = mouse.position
            click_locations.append(pos)
            print(f"  - x: {pos[0]} y: {pos[1]}")
    elif key == Key.esc:
        print("QUITTING: have a nice day!")
        current_state = State.QUITTING


def click(pos, clicks=1):
    mouse.position = pos
    mouse.click(button=Button.left, count=clicks)


def print_instructions():
    print("R: Start click location recording (press T to save location)")
    print("SPACE: Start/Pause clicking")
    print("I: Print instructions")
    print("ESC: Quit")
    print()
    print("Waiting for command...")


def perform_clicks():
    global last_click_time
    for location in click_locations:
        click(location)
    last_click_time = time()


def play():
    global current_state
    keyboard_listener = mainKeyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    keyboard_listener.start()

    print_instructions()
    while current_state is not State.QUITTING:
        t = time()
        if current_state is State.RUNNING:
            if last_click_time + click_interval <= t:
                perform_clicks()


play()
