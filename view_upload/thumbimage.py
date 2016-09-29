from PIL import Image
import os

size = 128, 128

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
im = Image.open('images.jpg')
print im.size
#im.thumbnail(size, Image.ANTIALIAS)
#im.save('thumb.jpg', 'JPEG')
