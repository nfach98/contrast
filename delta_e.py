# import colour
# import cv2
# import numpy as np
#
# image1_rgb = cv2.imread('images_clean/Bundesliga Arminia Bielefeld 2020-21 Home copy.png')
# image2_rgb = cv2.imread('images_clean/Bundesliga Arminia Bielefeld 2020-21 Third copy.png')
#
# image1_lab = cv2.cvtColor(image1_rgb.astype(np.float32) / 255, cv2.COLOR_RGB2Lab)
# image2_lab = cv2.cvtColor(image2_rgb.astype(np.float32) / 255, cv2.COLOR_RGB2Lab)
# e = colour.delta_E(image1_lab, image2_lab)
#
# print(np.mean(e))

import cv2
import numpy as np
import matplotlib.pyplot as plt
import skimage
from skimage import io, color
from PIL import Image

img = Image.open('images_clean/Bundesliga Bayer 04 Leverkusen 2016-17 Fourth copy.png')
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

average = (rs/length, gs/length, bs/length, 255)

avg_patch = np.zeros(shape=data.shape, dtype=np.uint8)
for i in range(len(avg_patch)):
    avg_patch[i] += np.uint8(average)

fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(6, 3))

ax0.imshow(img)
ax0.set_title('Image')
ax0.axis('off')

ax1.imshow(avg_patch)
ax1.set_title('Average colors')
ax1.axis('off')

plt.show()

# new_data = np.array(new_data)
# print(new_data.shape)
#
# average = data.mean(axis=0).mean(axis=0)
# print(average)

# img.putdata(newData)
# num = np.array(newData)
# print(num)
# average = num.mean(axis=0).mean(axis=0)
# print(num)

# img = io.imread('images_clean/Bundesliga Arminia Bielefeld 2021-22 Third copy.png')[:, :, :-1]
# average = img.mean(axis=0).mean(axis=0)
# print(img.shape)
#
# pixels = np.float32(img.reshape(-1, 3))
#
# n_colors = 5
# criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
# flags = cv2.KMEANS_RANDOM_CENTERS
#
# _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
# _, counts = np.unique(labels, return_counts=True)
#
# dominant = palette[np.argmax(counts)]
#
# avg_patch = np.ones(shape=img.shape, dtype=np.uint8) * np.uint8(average)
#
# indices = np.argsort(counts)[::-1]
# freqs = np.cumsum(np.hstack([[0], counts[indices] / float(counts.sum())]))
# rows = np.int_(img.shape[0] * freqs)
#
# dom_patch = np.zeros(shape=img.shape, dtype=np.uint8)
# # dom_90 = dom_patch[:54]
# for i in range(len(rows) - 1):
#     dom_patch[rows[i]:rows[i + 1], :, :] += np.uint8(palette[indices[i]])
#
# # 90 percent of all color
# list90 = dom_patch[:54].tolist()
# colors = []
# for i, li in enumerate(list90):
#     if len(colors) < 1 or li[0] not in colors:
#         colors.append(li[0])
#
# print(colors)
#
# fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(12, 6))
# ax0.imshow(avg_patch)
# ax0.set_title('Average color')
# ax0.axis('off')
# ax1.imshow(dom_patch)
# ax1.set_title('Dominant colors')
# ax1.axis('off')
# plt.show()
