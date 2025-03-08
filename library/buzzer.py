"""
buzzer.py - Buzzer Handling Library with Tone and Melody Support

Author: Andrew Stephen Nacion
Copyright (c) 2025 Andrew Stephen Nacion
Licensed under the MIT License. See LICENSE file in the project root for full license information.

This library provides a Buzzer class to handle passive buzzers using GPIO pins and PWM.
Features include:
- Playing specific tones by frequency.
- Playing melodies using note names.
- Predefined melodies for startup, button press, and warning signals.

License: MIT License
"""

from machine import Pin, PWM
from utime import sleep

class Buzzer:
    def __init__(self, pin_number):
        """
        Initialize the passive buzzer on the specified GPIO pin.
        """
        self.pin = Pin(pin_number, Pin.OUT)
        self.pwm = PWM(self.pin)
        self.pwm.deinit()  # Turn off PWM initially.
        self.volume = 65534  # Set volume (duty cycle value, maximum is 65535)

        # Dictionary of tone frequencies.
        self.tones = {
            "B0": 31, "C1": 33, "CS1": 35, "D1": 37, "DS1": 39, "E1": 41, "F1": 44,
            "FS1": 46, "G1": 49, "GS1": 52, "A1": 55, "AS1": 58, "B1": 62, "C2": 65,
            "CS2": 69, "D2": 73, "DS2": 78, "E2": 82, "F2": 87, "FS2": 93, "G2": 98,
            "GS2": 104, "A2": 110, "AS2": 117, "B2": 123, "C3": 131, "CS3": 139,
            "D3": 147, "DS3": 156, "E3": 165, "F3": 175, "FS3": 185, "G3": 196,
            "GS3": 208, "A3": 220, "AS3": 233, "B3": 247, "C4": 262, "CS4": 277,
            "D4": 294, "DS4": 311, "E4": 330, "F4": 349, "FS4": 370, "G4": 392,
            "GS4": 415, "A4": 440, "AS4": 466, "B4": 494, "C5": 523, "CS5": 554,
            "D5": 587, "DS5": 622, "E5": 659, "F5": 698, "FS5": 740, "G5": 784,
            "GS5": 831, "A5": 880, "AS5": 932, "B5": 988, "C6": 1047, "CS6": 1109,
            "D6": 1175, "DS6": 1245, "E6": 1319, "F6": 1397, "FS6": 1480, "G6": 1568,
            "GS6": 1661, "A6": 1760, "AS6": 1865, "B6": 1976, "C7": 2093, "CS7": 2217,
            "D7": 2349, "DS7": 2489, "E7": 2637, "F7": 2794, "FS7": 2960, "G7": 3136,
            "GS7": 3322, "A7": 3520, "AS7": 3729, "B7": 3951, "C8": 4186, "CS8": 4435,
            "D8": 4699, "DS8": 4978
        }
        
        # Define default melodies and tones.
        self.startup_song = ["C5", "E5", "G5"]  # Startup melody.
        self.press_tone = "A4"                  # Single tone for button press.
        self.warning_song = ["E5", "G5", "A5", "P", "E5", "G5", "B5", "A5"]  # Warning sequence.
    
    def playtone(self, frequency):
        """
        Play a tone at the specified frequency.
        """
        self.pwm.init()
        self.pwm.freq(frequency)
        self.pwm.duty_u16(self.volume)
    
    def bequiet(self):
        """
        Turn off the buzzer.
        """
        self.pwm.duty_u16(0)
        self.pwm.deinit()
    
    def playsong(self, song):
        """
        Play a song given as a list of note names. "P" represents a pause.
        """
        for note in song:
            if note == "P":
                self.bequiet()
            else:
                self.playtone(self.tones[note])
            sleep(0.3)
        self.bequiet()
    
    def startup_buzzer(self):
        """
        Play the startup melody.
        """
        self.playsong(self.startup_song)
    
    def press_buzzer(self):
        """
        Play a short press tone.
        """
        self.playtone(self.tones[self.press_tone])
        sleep(0.1)
        self.bequiet()
    
    def warning_buzzer(self):
        """
        Play the warning sequence.
        """
        self.playsong(self.warning_song)
