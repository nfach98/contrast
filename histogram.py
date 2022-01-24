from os import walk
import random

import cv2
import matplotlib.pyplot as plt
from scipy.spatial import distance as dist


def random_image():
    f = []
    for (dirpath, dirnames, filenames) in walk("images"):
        f.extend(filenames)
        break

    return random.sample(f, 2)


def opencv_compare_hist():
    # METHOD #1: UTILIZING OPENCV
    # initialize OpenCV methods for histogram comparison
    OPENCV_METHODS = (
        ("Correlation", cv2.HISTCMP_CORREL),
        ("Chi-Squared", cv2.HISTCMP_CHISQR),
        ("Intersection", cv2.HISTCMP_INTERSECT),
        ("Hellinger", cv2.HISTCMP_BHATTACHARYYA))

    # loop over the comparison methods
    for (methodName, method) in OPENCV_METHODS:
        # initialize the results dictionary and the sort
        # direction
        results = {}
        reverse = False
        # if we are using the correlation or intersection
        # method, then sort the results in reverse order
        if methodName in ("Correlation", "Intersection"):
            reverse = True

        # loop over the index
        for (k, hist) in index.items():
            # compute the distance between the two histograms
            # using the method and update the results dictionary
            d = cv2.compareHist(index[list(index.keys())[0]], hist, method)
            results[k] = d
        # sort the results
        results = sorted([(v, k) for (k, v) in results.items()], reverse=reverse)

        # initialize the results figure
        fig = plt.figure("Results: %s" % methodName)
        fig.suptitle(methodName, fontsize=20)

        # loop over the results
        for (i, (v, k)) in enumerate(results):
            # show the result
            ax = fig.add_subplot(1, len(images), i + 1)
            ax.set_title("%.2f" % v)
            plt.imshow(images[k])
            plt.axis("off")

    # show the OpenCV methods
    plt.show()


def scipy_distance_metrics():
    # METHOD #2: UTILIZING SCIPY
    # initialize the scipy methods to compaute distances
    SCIPY_METHODS = (
        ("Euclidean", dist.euclidean),
        ("Manhattan", dist.cityblock),
        ("Chebysev", dist.chebyshev))

    # loop over the comparison methods
    for (methodName, method) in SCIPY_METHODS:
        # initialize the dictionary dictionary
        results = {}
        # loop over the index
        for (k, hist) in index.items():
            # compute the distance between the two histograms
            # using the method and update the results dictionary
            d = method(index[list(index.keys())[0]], hist)
            results[k] = d
        # sort the results
        results = sorted([(v, k) for (k, v) in results.items()])

        # initialize the results figure
        fig = plt.figure("Results: %s" % methodName)
        fig.suptitle(methodName, fontsize=20)
        # loop over the results
        for (i, (v, k)) in enumerate(results):
            # show the result
            ax = fig.add_subplot(1, len(images), i + 1)
            ax.set_title("%.2f" % v)
            plt.imshow(images[k])
            plt.axis("off")

    # show the SciPy methods
    plt.show()


index = {}
images = {}
paths = random_image()
print(paths)

for filename in paths:
    # extract the image filename (assumed to be unique) and
    # load the image, updating the images dictionary
    image = cv2.imread("images/" + filename, 1)
    images[filename] = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # extract a 3D RGB color histogram from the image,
    # using 8 bins per channel, normalize, and update
    # the index
    hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    hist = cv2.normalize(hist, hist).flatten()
    index[filename] = hist

opencv_compare_hist()
scipy_distance_metrics()
