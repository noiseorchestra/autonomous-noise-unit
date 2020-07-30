import time
from luma.core.virtual import hotspot


def scrollable_panel(draw, x1, y1, x2, y2, text, i):
    """Draw meter bar and frame"""
    draw.rectangle((x1, y1) + (x2 - 1, y2 - 1), "black", "black")
    draw.text((i, 0), text, font=None, fill="white")


def render(draw, width, height, text, i):
    """Calculate measurements and render"""
    scrollable_panel(draw, 0, 0, width, height, text, i)


class Panel(hotspot):
    """Object for drawing level meter"""

    def __init__(self, width, height, text, interval, scroll=False):
        super(Panel, self).__init__(width, height)
        self._interval = interval
        self._last_updated = 0
        self.i = 0
        self.scroll = scroll
        self.text = text

    def should_redraw(self):
        return time.time() - self._last_updated > self._interval

    def update(self, draw):
        w, h = draw.textsize(self.text, font=None)
        if self.i * -1 >= w:
            self.i += w + self.width
        if self.width < w:
            self.scroll = True
        render(draw, self.width, self.height, self.text, self.i)
        if self.scroll:
            self.i -= 1
        self._last_updated = time.time()
