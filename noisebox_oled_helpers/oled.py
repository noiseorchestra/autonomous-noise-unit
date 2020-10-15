from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont, ImageDraw
from luma.core.virtual import viewport
from noisebox_oled_helpers.meter import Meter
from noisebox_oled_helpers.scroll import ScrollPanel
from threading import Thread
import time


class OLED:
    """Helper object for OLED functions"""

    def __init__(self):
        self.serial = i2c(port=1, address=0x3C)
        self.device = ssd1306(self.serial, rotate=0)
        self._meters_running = False
        self._scrolling_text_running = False

    def draw_text(self, x, y, text):
        """Draw one line of text"""

        with canvas(self.device) as draw:
            draw.text((x, y), text, fill="white")
        time.sleep(1)

    def draw_lines(self, lines):
        """Draw several lines of standard text"""

        with canvas(self.device) as draw:
            y = 0
            for line in lines:
                draw.text((0, y), line, fill="white")
                y += 13
        time.sleep(1)

    def render_meters(self, level_threads):
        """Render level meters"""

        widget_width = self.device.width // 4
        widget_height = self.device.height
        widgets = []
        for level_thread in level_threads:
            meter = Meter(level_thread.name, widget_width, widget_height,
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

    def start_meters(self, level_threads):
        """Start level meters in thread"""

        self._meters_running = True
        oled_meters = Thread(target=self.render_meters,
                             args=(level_threads,))
        oled_meters.start()

    def stop_meters(self):
        """Stop level meter thread"""

        self._meters_running = False

    def render_scrolling_text(self, text_array):
        """Render scrolling text"""

        y = 0
        panel_width = self.device.width
        panel_height = self.device.height // 4
        virtual = viewport(self.device,
                           width=self.device.width,
                           height=self.device.height)
        widgets = []

        for line in text_array:
            panel = ScrollPanel(panel_width,
                          panel_height,
                          line, interval=0.1)

            widgets.append(panel)

        for widget in widgets:
            virtual.add_hotspot(widget, (0, y))
            y += panel_height

        virtual.set_position((0, 0))

        while self._scrolling_text_running:
            virtual.set_position((0, 0))
            time.sleep(0.1)

    def start_scrolling_text(self, text_array):
        """Start scrolling text in thread"""

        self._scrolling_text_running = True
        t = Thread(target=self.render_scrolling_text, args=(text_array,))
        t.start()

    def stop_scrolling_text(self):
        """STop scrolling text thread"""

        self._scrolling_text_running = False

    def draw_ip_menu(self, picker_value, ip_address):
        self.draw_text(10, 40, ip_address + picker_value)
