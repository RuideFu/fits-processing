from os import remove

import numpy as np
from scipy import special
from numpy import median, floor, sqrt

from rejectionGenerator import rejectionGenerator


def columnFlagger(image, f):
    # read in the images and get their data
    data = image[0].data
    row_count = data.shape[0]
    col_count = data.shape[1]
    # move through each pixel
    columnVals = np.zeros(col_count)
    for col in range(col_count):
        for row in range(row_count):
            # define the M pixels to its left and right
            columnVals[col] = columnVals[col] + data[row][col]

    medianColVals = median(columnVals)
    absdevColVals = sorted(abs(columnVals - medianColVals))
    rejectionFactor, superSigma = rejectionGenerator(absdevColVals, f)
    flaggedColumns = np.zeros(col_count)
    flaggedColumnIndexes = []
    for i in range(len(columnVals)):
        if columnVals[i] - medianColVals > rejectionFactor:
            flaggedColumnIndexes.append(i)
            flaggedColumns[i] = 1
        else:
            flaggedColumns[i] = 0
    # for col in range(col_count):
    #     for row in range(row_count):
    #         # define the M pixels to its left and right
    #         data[row][col] = flaggedColumns[col]
    return flaggedColumnIndexes, medianColVals, superSigma, columnVals
