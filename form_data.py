import random
import tkinter
from os import walk
from tkinter import *

import numpy as np
from PIL import Image, ImageTk

from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

from csv import DictWriter


def random_image():
    f = []
    for (dirpath, dirnames, filenames) in walk("images_clean"):
        f.extend(filenames)
        break

    return random.sample(f, 2)


def rgb_to_hex(color):
    return '#%02x%02x%02x' % color


def delta_e(color1, color2):
    color1_rgb = sRGBColor(color1[0] / 255, color1[1] / 255, color1[2] / 255)
    color2_rgb = sRGBColor(color2[0] / 255, color2[1] / 255, color2[2] / 255)
    color1_lab = convert_color(color1_rgb, LabColor)
    color2_lab = convert_color(color2_rgb, LabColor)
    return delta_e_cie2000(color1_lab, color2_lab)


def change_pic(choice):
    file = random_image()

    test1 = ImageTk.PhotoImage(Image.open("images_clean/" + file[0]))
    label1.config(image=test1)
    label1.image = test1
    color1 = get_average_color("images_clean/" + file[0])
    canvas1 = Canvas(root, height=120, width=120, bg="#fff")
    canvas1.create_rectangle(0, 0, 180, 120, outline=rgb_to_hex(color1), fill=rgb_to_hex(color1))

    test2 = ImageTk.PhotoImage(Image.open("images_clean/" + file[1]))
    label2.config(image=test2)
    label2.image = test2
    color2 = get_average_color("images_clean/" + file[1])
    canvas2 = Canvas(root, height=120, width=120, bg="#fff")
    canvas2.create_rectangle(0, 0, 180, 120, outline=rgb_to_hex(color2), fill=rgb_to_hex(color2))

    delta = delta_e(color1, color2)
    labelDelta.config(text="ΔE*: " + str(delta))

    # Position image
    label1.place(x=(540 - test1.width()) / 2, y=0)
    canvas1.place(x=420, y=400)

    label2.place(x=(540 - test2.width()) / 2 + 540, y=0)
    canvas2.place(x=540, y=400)

    labelDelta.place(x=332, y=532)

    if choice < 3:
        insert_to_csv(color1, color2, delta, choice)


def get_average_color(images_path):
    img = Image.open(images_path)
    img_rgba = img.convert("RGBA")

    shape = np.array(img)
    datas = img_rgba.getdata()

    data = []
    for item in datas:
        data.append(item)

    data = np.array(data)
    data = data.reshape(shape.shape[0], shape.shape[1], 4)

    rs = 0
    gs = 0
    bs = 0
    length = 0

    for y in data:
        for x in y:
            if x[3] > 100:
                rs = rs + x[0]
                gs = gs + x[1]
                bs = bs + x[2]
                length = length + 1

    average = (int(rs / length), int(gs / length), int(bs / length))
    return average


def insert_to_csv(color1, color2, delta, similarity):
    fields = ['R1', 'G1', 'B1', 'R2', 'G2', 'B2', 'DELTA_E', 'SIMILARITY']
    new = {
        'R1': color1[0],
        'G1': color1[1],
        'B1': color1[2],
        'R2': color2[0],
        'G2': color2[1],
        'B2': color2[2],
        'DELTA_E': delta,
        'SIMILARITY': similarity
    }
    with open('dataset.csv', 'a', newline='') as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames=fields)
        dictwriter_object.writerow(new)
        f_object.close()


root = Tk()
root.geometry("1080x640")
root.configure(background='white')

# Create a photoimage object of the image in the path
label1 = tkinter.Label(bg="white")
label2 = tkinter.Label(bg="white")
labelDelta = tkinter.Label(bg="white", width=60)

change_pic(3)

button_no = tkinter.Button(root, text="Clash", width=20, bg='red', fg='white', command=lambda: change_pic(0))
# button_middle = tkinter.Button(root, text="Don't know", width=20, bg='yellow', fg='black',command=lambda: change_pic(1))
button_yes = tkinter.Button(root, text="Distinguishable", width=20, bg='green', fg='white',command=lambda: change_pic(1))
button_skip = tkinter.Button(root, text="Skip", width=20, bg='white', fg='black', command=lambda: change_pic(3))

button_yes.place(x=632, y=600)
# button_middle.place(x=472, y=600)
button_no.place(x=312, y=600)

button_skip.place(x=920, y=600)

root.mainloop()
