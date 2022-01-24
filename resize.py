import os
from PIL import Image

path = "images_mini/"
dirs = os.listdir(path)


def resize():
    for item in dirs:
        if os.path.isfile(path + item):
            f, e = os.path.splitext(path + item)
            print(f + '.png')
            im = Image.open(f + '.png')
            im_resize = im.resize((45, 60), Image.ANTIALIAS)
            im_resize.save(f + '.png', 'PNG')


resize()
