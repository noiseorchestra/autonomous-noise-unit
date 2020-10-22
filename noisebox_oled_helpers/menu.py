# Based on https://gist.github.com/codelectron/d493d4aaa6fc858ce69f2b335afd0b00#file-oled_rot_menu_rpi-py

from noisebox_oled_helpers.menu_items import MenuItems
import noisebox_oled_helpers.fonts as fonts
from luma.core.render import canvas
from PIL import ImageFont, Image
import os

class Menu(MenuItems):
    """Class for drawing OLED menu"""

    def __init__(self, dry_run=False):
        super().__init__(dry_run)
        self.dry_run = dry_run
        self.counter = 0
        self.menuindex = 0
        self.device = None

    def start(self, device):
        """Start menu"""

        self.device = device
        self.draw_menu()

    def invert(self, draw, x, y, text, font_size):
        """invert selected menue item"""

        font = fonts.generate_font(font_size)
        draw.rectangle((x, y, x+120, y+font_size), outline=255, fill=255)
        draw.text((x, y), text, font=font, outline=0, fill="black")

    def get_menu_item_str(self, i):
        menu_items = self.active_menu_items
        if type(menu_items[i]) is dict:
            value = menu_items[i]["value"]
            if menu_items[i]["name"] == "INPUT":
                value = "mono" if menu_items[i]["value"] == "1" else "stereo"
            return menu_items[i]["name"] + ": " + value
        return menu_items[i]

    def menu(self, draw, index):
        """return prepared menu"""

        font_size = 15
        font = fonts.generate_font(font_size)
        draw.rectangle(self.device.bounding_box, outline="white", fill="black")
        if self.main_menu == self.active_menu_items:
            draw.text((2, 0), "===== A.N.U =====", font=font, fill=255)
        for i in range(len(self.active_menu_items)):
            if i > 2:
                offset = 0 - font_size*(i-1)
            if(i == index):
                self.menuindex = i
                self.invert(draw, 2, i*font_size + font_size + offset, self.get_menu_item_str(i), font_size)
            else:
                draw.text((2, i*font_size + font_size + offset), self.get_menu_item_str(i), font=font, fill=255)

    def draw_menu(self):
        """draw menu on convas"""

        with canvas(self.device) as draw:
            self.menu(draw, self.counter % len(self.active_menu_items))

    def reset_menu(self):
        """Set new menu items"""

        self.menuindex = 0
        self.counter = 0

    def draw_ip_menu(self, picker_value, ip_address):
        with canvas(self.device) as draw:
            draw.text((10, 40), ip_address + picker_value, font=fonts.generate_font(15), fill="white")
