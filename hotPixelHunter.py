from os import remove

import numpy as np
from scipy import special
from numpy import median, floor, sqrt
from columnLocator import columnLocator


def hotPixelHunter(M, image, image2, brokenImage):
    # read in the images and get their data
    # dataFlagged = columnLocator(brokenImage)
    dataFlagged = brokenImage[0].data
    data = image[0].data
    dataTemp = image2[0].data
    row_count = data.shape[0]
    col_count = data.shape[1]
    flaggedPixels = 0
    # move through each pixel
    for row in range(row_count):
        for col in range(col_count):
            pixel = [data[row][col]]
            # define the M pixels to its left and right
            pixel_set = []
            for j in range(0, (2 * M) + 1):
                for i in range(0, (2 * M) + 1):
                    try:

                        if dataFlagged[(row - M) + i][(col - M) + j] == 1:
                            continue
                        else:
                            try:
                                pixel_set.append(data[(row - M) + i][(col - M) + j])
                            except:
                                continue
                    except:
                        continue
            # populate sets with the middle pixel and find the median
            # populate set of absolute deviations
            # retrieve the rejection factor from the original absdev set
            swag = 0
            pixel_set = sorted(pixel_set)
            while swag == 0:
                if dataFlagged[row][col] == 1:
                    dataTemp[row][col] = 0
                    swag = 1
                    continue
                pixel_median = median(pixel_set)
                # populate set of absolute deviations
                rawDev = (pixel_set - pixel_median)
                absdev = sorted(abs(rawDev))
                if len(absdev) <= 1:
                    dataTemp[row][col] = 0
                    swag = 1
                    continue
                rejection_factor = rejectionGenerator(absdev)
                if abs(absdev[-1]) > rejection_factor:
                    if abs(pixel - pixel_median) > rejection_factor:
                        dataTemp[row][col] = 100
                        flaggedPixels += 1
                        swag = 1
                    else:
                        annihilate = []
                        for i in range(len(rawDev)):
                            if abs(rawDev[i]) > rejection_factor:
                                annihilate.append(i)
                        pixel_set = [v for i, v in enumerate(pixel_set) if i not in annihilate]

                else:
                    dataTemp[row][col] = 0
                    swag = 1

    # Apply new data
    image2[0].data = dataTemp

    # percent rejected
    print('Percent pixels rejected: ', flaggedPixels / (2048 * 2064))
    return [image2]


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
