import time
from luma.core.virtual import hotspot


def vertical_bar(draw, x1, y1, x2, y2, text, i):
    """Draw meter bar and frame"""
    draw.rectangle((x1, y1) + (x2 - 1, y2 - 1), "black", "white")
    draw.text((i, 0), "scroll me!", font=None, fill="white")


def render(draw, width, height, text, i):
    """Calculate measurements and render"""
    vertical_bar(draw, 0, 0, width, height, text, i)


class Panel(hotspot):
    """Object for drawing level meter"""

    def __init__(self, width, height, interval, scroll=False):
        super(Panel, self).__init__(width, height)
        self._interval = interval
        self._last_updated = 0
        self.i = 0
        self.scroll = scroll

    def should_redraw(self):
        return time.time() - self._last_updated > self._interval

    def update(self, draw):
        text = "scroll me!"
        w, h = draw.textsize(text, font=None)
        if self.i * -1 >= w:
            self.i += w + self.width
        render(draw, self.width, self.height, text, self.i)
        if self.scroll:
            self.i -= 1
        self._last_updated = time.time()
