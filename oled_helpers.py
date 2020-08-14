from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont, ImageDraw
from oled_hotspot_layout import Layout
from luma.core.virtual import viewport
from oled_meter import Meter
from oled_hotspot import Panel
from threading import Thread
import time

class OLED:
    """Helper object for OLED functions"""
    # TODO
    # draw title
    # notification bar virtual area
    # notification icons
    # scrolling text

    def __init__(self):
        self.serial = i2c(port=1, address=0x3C)
        self.device = ssd1306(self.serial, rotate=0)
        self._meters_running = True
        self._layout_running = True

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

    def start_meters(self, level_threads):
        widget_width = self.device.width // 4
        widget_height = self.device.height
        widgets = []

        for level_thread in level_threads:
            meter = Meter(widget_width, widget_height,
                          level_thread, interval=0.2)
            widgets.append(meter)

        virtual = viewport(self.device,
                           width=widget_width * 4,
                           height=widget_height)

        for i, widget in enumerate(widgets):
            virtual.add_hotspot(widget, (i * widget_width, 0))

        while self._meters_running:
            virtual.set_position((0, 0))
            time.sleep(0.1)

    def stop_meters(self):
        self._meters_running = False

    def render_layout(self, text_array):

        y = 0
        panel_width = self.device.width
        panel_height = self.device.height // 4
        virtual = viewport(self.device,
                           width=self.device.width,
                           height=self.device.height)
        widgets = []

        for line in text_array:
            panel = Panel(panel_width,
                          panel_height,
                          line, interval=0.1)

            widgets.append(panel)

        for widget in widgets:
            virtual.add_hotspot(widget, (0, y))
            y += panel_height

        virtual.set_position((0, 0))

        while self._layout_running:
            virtual.set_position((0, 0))
            time.sleep(0.1)

    def start_layout(self, text_array):
        t = Thread(target=self.render_layout, args=(text_array,))
        t.start()

    def stop_layout(self):
        self._layout_running = False
