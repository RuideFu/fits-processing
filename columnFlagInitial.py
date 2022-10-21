from os import remove

import numpy as np
from scipy import special
from numpy import median, floor, sqrt


def columnFlagger(image):
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
    rejectionFactor = rejectionGenerator(absdevColVals)

    flaggedColumns = np.zeros(col_count)

    for i in range(len(columnVals)):
        if columnVals[i] - medianColVals > rejectionFactor:
            print('AAAAAAAAA MY BLOOD', i)

            flaggedColumns[i] = 100
        else:
            flaggedColumns[i] = 0
    print(columnVals[2045] - medianColVals, rejectionFactor)
    for col in range(col_count):
        for row in range(row_count):
            # define the M pixels to its left and right
            data[row][col] = flaggedColumns[col]

    image[0].data = data

    return image

def rejectionGenerator(absdev):
    N = len(absdev)

    # now we have the final set to be tested (absdev) we find the rejection facto
    # print(absdev)
    if N >= 6:
        correction = 1 + (2.2212 * (N ** (-1.137)))
    if N == 5:
        correction = 1.31
    if N == 4:
        correction = 1.53
    if N == 3:
        correction = 1.59
    if N == 2:
        correction = 1.76

    i = floor(0.683 * N)
    i_minus = 0.683 * (N - 1)
    sigma = (absdev[int(i) - 1] + (absdev[int(i)] - absdev[int(i) - 1]) * (i_minus - floor(i_minus))) * correction
    rejection_factor = sigma * sqrt(2) * special.erfinv(1 - (0.5 / N))
    return rejection_factor
