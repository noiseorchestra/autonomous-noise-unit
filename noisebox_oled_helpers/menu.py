# Based on https://gist.github.com/codelectron/d493d4aaa6fc858ce69f2b335afd0b00#file-oled_rot_menu_rpi-py

from luma.core.render import canvas
from PIL import ImageFont


class Menu:
    """Class for drawing OLED menu"""

    def __init__(self, menu_items):
        # persist values
        self.counter = 0
        self.menuindex = 0
        self.default_menu_items = menu_items
        self.menu_items = menu_items
        self.device = None

    def start(self, device):
        """Start menu"""

        self.device = device
        self.draw_menu()

    def invert(self, draw, x, y, text):
        """invert selected menue item"""

        font = ImageFont.load_default()
        draw.rectangle((x, y, x+120, y+12), outline=255, fill=255)
        draw.text((x, y), text, font=font, outline=0, fill="black")

    def menu(self, device, draw, menustr, index):
        """return prepared menu"""

        font = ImageFont.load_default()
        draw.rectangle(self.device.bounding_box, outline="white", fill="black")
        for i in range(len(menustr)):
            if(i == index):
                self.menuindex = i
                self.invert(draw, 2, i*10, menustr[i])
            else:
                draw.text((2, i*10), menustr[i], font=font, fill=255)

    def draw_menu(self):
        """draw menu on convas"""

        with canvas(self.device) as draw:
            self.menu(self.device, draw, self.menu_items, self.counter % len(self.menu_items))

    def new_menu_items(self, new_menu_items):
        """Set new menu items"""

        self.menu_items = new_menu_items
        self.menuindex = 0
        self.counter = 0
