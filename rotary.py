# Based on https://gist.github.com/codelectron/d493d4aaa6fc858ce69f2b335afd0b00#file-oled_rot_menu_rpi-py

import RPi.GPIO as GPIO
from oled_helpers import OLED_helpers
import time
import sys

class KY040:

    CLOCKWISE = 0
    ANTICLOCKWISE = 1

    def __init__(self, clockPin, dataPin, switchPin,
                 rotaryCallback, switchCallback):

        self.clockPin = clockPin
        self.dataPin = dataPin
        self.switchPin = switchPin
        self.rotaryCallback = rotaryCallback
        self.switchCallback = switchCallback

        try:
            GPIO.setup(clockPin, GPIO.IN)
            GPIO.setup(dataPin, GPIO.IN)
            GPIO.setup(switchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        except Exception as e:
            print("Rotary switch error:", e)
            oled_h = OLED_helpers()
            oled_h.draw_lines(["==ERROR==", "rotary switch error"])
            time.sleep(4)
            sys.exit("Exited because of rotary switch error")

    def start(self):
        GPIO.add_event_detect(self.clockPin,
                              GPIO.FALLING,
                              callback=self._clockCallback,
                              bouncetime=200)
        GPIO.add_event_detect(self.switchPin,
                              GPIO.FALLING,
                              callback=self._switchCallback,
                              bouncetime=300)

    def stop(self):
        GPIO.remove_event_detect(self.clockPin)
        GPIO.remove_event_detect(self.switchPin)

    def _clockCallback(self, pin):
        if GPIO.input(self.clockPin) == 0:
            data = GPIO.input(self.dataPin)
            if data == 1:
                self.rotaryCallback(self.ANTICLOCKWISE)
            else:
                self.rotaryCallback(self.CLOCKWISE)

    def _switchCallback(self, pin):
        if GPIO.input(self.switchPin) == 0:
            self.switchCallback()
