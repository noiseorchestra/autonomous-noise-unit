# Based on https://gist.github.com/codelectron/d493d4aaa6fc858ce69f2b335afd0b00#file-oled_rot_menu_rpi-py

import RPi.GPIO as GPIO
import time
import sys
from noisebox_rotary.rotary_state import SwitchState


class KY040:

    def __init__(self, noisebox, oled_menu):

        self.clockPin = 5
        self.dataPin = 6
        self.switchPin = 22
        self.noisebox = noisebox
        self.oled_menu = oled_menu
        self.switchState = SwitchState()
        self.CLOCKWISE = 0
        self.ANTICLOCKWISE = 1

        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.clockPin, GPIO.IN)
            GPIO.setup(self.dataPin, GPIO.IN)
            GPIO.setup(self.switchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        except Exception as e:
            print("Rotary switch error:", e)
            self.noisebox.oled.draw_lines(["==ERROR==", "rotary switch error"])
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
                self.switchState.rotaryCallback(self.oled_menu, self.ANTICLOCKWISE)
            else:
                self.switchState.rotaryCallback(self.oled_menu, self.CLOCKWISE)

    def _switchCallback(self, pin):
        if GPIO.input(self.switchPin) == 0:
            self.switchState.switchCallback(self.noisebox, self.oled_menu, self.oled)
