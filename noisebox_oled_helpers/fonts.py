from PIL import ImageFont
import os


def generate_font(size):
    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'fonts', "C&C Red Alert [INET].ttf"))
    return ImageFont.truetype(font_path, size)
