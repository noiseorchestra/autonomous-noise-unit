from luma.core.virtual import viewport
import oled_hotspots
import time


class Layout:
    """Object for drawing level meters for array of audio level threads"""

    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def render(self, device):
        panel_width = device.width
        panel1_height = device.height // 4
        panel2_height = device.height - panel1_height

        panel1 = oled_hotspots.Panel(panel_width, panel1_height, interval=0.1)
        panel2 = oled_hotspots.Panel(panel_width, panel2_height, interval=0.1, scroll=True)

        virtual = viewport(device,
                           width=device.width,
                           height=device.height)

        virtual.add_hotspot(panel1, (0, 0))
        virtual.add_hotspot(panel2, (0, panel1_height))
        virtual.set_position((0, 0))

        x = 0
        while self._running:
            x += 1
            virtual.set_position((0, 0))
            time.sleep(0.1)
            if x == 100:
                self._running = False
