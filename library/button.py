"""
button.py - Button Handling Library with Debouncing and Long Press Detection

Author: Andrew Stephen Nacion

This library provides a Button class to handle button presses with debouncing 
and long-press detection using GPIO pins.

Features:
- Debouncing to prevent false triggers.
- Detection of single presses.
- Detection of long presses.

License: MIT License
"""

from machine import Pin
import time

# Global debug flag for the module.
DEBUG = True

def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

class Button:
    def __init__(self, pin_num, use_pullup=False, debounce_ms=50, press_duration_ms=500):
        """
        Initializes the Button instance.

        Args:
            pin_num (int): GPIO pin number to which the button is connected.
            use_pullup (bool): Whether to enable the internal pull-up resistor. Default is False.
            debounce_ms (int): Debounce time in milliseconds to prevent false presses. Default is 50ms.
            press_duration_ms (int): Minimum duration in milliseconds for a valid press. Default is 500ms.
        """
        if use_pullup:
            self.pin = Pin(pin_num, Pin.IN, Pin.PULL_UP)
        else:
            self.pin = Pin(pin_num, Pin.IN)

        self.debounce_ms = debounce_ms
        self.press_duration_ms = press_duration_ms
        initial_state = self.pin.value()  # Should be 1 if not pressed (active-low)

        # Use separate state variables for the two methods to prevent interference.
        self.last_state_once = initial_state
        self.last_state_for = initial_state

        self.last_press_time = 0
        self.press_start_time = 0

    def is_pressed_for(self):
        """
        Checks if the button is pressed for at least the specified duration.

        Returns:
            bool: True if the button is pressed for the required duration, False otherwise.
        """
        current_time = time.ticks_ms()
        current_state = self.pin.value()
        debug_print("[is_pressed_for] Current State:", current_state, "Last State:", self.last_state_for)

        # Detect falling edge (active-low): button pressed.
        if current_state == 0 and self.last_state_for == 1:
            self.press_start_time = current_time

        # On rising edge: button released. Check if it was pressed long enough.
        if current_state == 1 and self.last_state_for == 0:
            press_duration = time.ticks_diff(current_time, self.press_start_time)
            if press_duration >= self.press_duration_ms:
                self.last_state_for = current_state
                return True

        self.last_state_for = current_state
        return False

    def is_pressed_once(self):
        """
        Checks if the button is pressed once (with debouncing).

        Returns:
            bool: True if the button is pressed once, False otherwise.
        """
        current_time = time.ticks_ms()
        current_state = self.pin.value()
        debug_print("[is_pressed_once] Current State:", current_state, "Last State:", self.last_state_once)

        # Detect a falling edge with sufficient debounce time.
        if current_state == 0 and self.last_state_once == 1:
            if time.ticks_diff(current_time, self.last_press_time) > self.debounce_ms:
                debug_print("Button press detected!")
                self.last_press_time = current_time
                self.last_state_once = current_state
                return True

        self.last_state_once = current_state
        return False
