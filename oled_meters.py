from luma.core.virtual import viewport
import oled_meter
import time


class Meters:
    """Object for drawing level meters for array of audio level threads"""

    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def render(self, device, level_threads):
        widget_width = device.width // 4
        widget_height = device.height
        widgets = []

        for level_thread in level_threads:
            meter = oled_meter.Meter(widget_width, widget_height,
                                     level_thread, interval=0.1)
            widgets.append(meter)

        virtual = viewport(device,
                           width=widget_width * len(widgets),
                           height=widget_height)

        for i, widget in enumerate(widgets):
            virtual.add_hotspot(widget, (i * widget_width, 0))

        while self._running:
            virtual.set_position((0, 0))
            time.sleep(0.1)
