from luma.core.virtual import viewport
from oled_hotspot import Panel
from threading import Thread
import time


class Layout:
    """Object for drawing an array of text lines with scrolling"""

    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def render(self, device, text_array):

        y = 0
        panel_width = device.width
        panel_height = device.height // 4
        virtual = viewport(device,
                           width=device.width,
                           height=device.height)
        widgets = []

        for line in text_array:
            panel = Panel(panel_width, panel_height,
                                        line, interval=0.1)
            widgets.append(panel)

        for widget in widgets:
            virtual.add_hotspot(widget, (0, y))
            y += panel_height

        virtual.set_position((0, 0))

        while self._running:
            virtual.set_position((0, 0))
            time.sleep(0.1)

    def start(self, device, text_array):
        t = Thread(target=self.render, args=(device, text_array,))
        t.start()
