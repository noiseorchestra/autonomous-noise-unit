from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont, ImageDraw
from luma.core.virtual import viewport
from threading import Thread
import time


class OLED_helpers:
    """Helper object for OLED functions"""
    # TODO
    # draw title
    # notification bar virtual area
    # notification icons
    # scrolling text

    def __init__(self):
        self.serial = i2c(port=1, address=0x3C)
        self.device = ssd1306(self.serial, rotate=0)

    def get_device(self):
        """Return OLED device object"""
        return self.device

    def draw_text(self, x, y, text):
        """Draw one line of standard text"""
        with canvas(self.device) as draw:
            draw.text((x, y), text, fill="white")

    def draw_lines(self, lines):
        """Draw several lines of standard text"""
        with canvas(self.device) as draw:
            y = 0
            for line in lines:
                draw.text((0, y), line, fill="white")
                y += 13

    def scroll_text(self, text, y=0, font=None, speed=1):
        full_text = text
        x = self.device.width

        # First measure the text size
        with canvas(self.device) as draw:
            w, h = draw.textsize(full_text, font)

        virtual = viewport(self.device, width=max(self.device.width, w + x + x), height=max(h, self.device.height))
        with canvas(virtual) as draw:
            draw.text((0, y), full_text, font=font, fill="white")

        i = 0
        while i < x:
            virtual.set_position((i, y))
            i += speed
            time.sleep(0.025)
