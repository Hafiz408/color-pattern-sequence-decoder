# import cv2
# image = cv2.imread("colors/red.png")
# image = cv2.resize(image, (1, 1))
# print(image)

from PIL import Image
from env import *

def get_image_color(filename):
    img = Image.open(filename)
    img = img.convert('RGB')
    width, height = img.size
    r, g, b = img.getpixel((width//2, height//2))
    color = dec_to_color.get((r,g,b), 404)
    return color

# print(get_image_color("colors/red.png"))