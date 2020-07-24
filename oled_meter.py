import time
from luma.core.virtual import hotspot


def vertical_bar(draw, x1, y1, x2, y2, yh):
    """Draw meter bar boundry"""
    draw.rectangle((x1, y1) + (x2, y2), "black", "white")
    draw.rectangle((x1, yh) + (x2, y2), "white", "white")


def render(draw, width, height, meter):
    """Draw meter bar"""
    top_margin = 3
    bottom_margin = 3

    bar_height = height - 15 - top_margin - bottom_margin
    width_meter = width
    bar_width = 0.5 * width_meter
    bar_margin = (width_meter - bar_width) / 2

    x = bar_margin

    # cpu_height = bar_height * (percentages[0] / 100.0)
    y2 = height - bottom_margin
    vertical_bar(draw, x, y2 - bar_height - 1,
                 x + bar_width, y2, y2 - meter.get_current_value())

    x += width_meter


class Meter(hotspot):
    """Object for drawing level meter"""

    def __init__(self, width, height, meter, interval):
        super(Meter, self).__init__(width, height)
        self._interval = interval
        self._last_updated = 0
        self.meter = meter

    def should_redraw(self):
        return time.time() - self._last_updated > self._interval

    def update(self, draw):
        render(draw, self.width, self.height, self.meter)
        self._last_updated = time.time()
