from os import remove

import numpy as np
from scipy import special
from numpy import median, floor, sqrt

def fitsElimination(image1, image2):
    finalFits = image1[0].data * image2[0].data

    image1[0].data = finalFits

    row_count = image1[0].data.shape[0]
    col_count = image1[0].data.shape[1]
    flaggedPixels = 0

    for row in range(row_count):
        for col in range(col_count):
            if image1[0].data[row][col] != 0:
                flaggedPixels = flaggedPixels + 1

    print('Percent pixels rejected: ', flaggedPixels / (2048 * 2064))
    return image1
