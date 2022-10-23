from os import remove

import numpy as np
from scipy import special
from numpy import median, floor, sqrt

from rejectionGenerator import rejectionGenerator


def pixel_eradicatormult(M, image, image2, f):
    # read in the images and get their data
    data = image[0].data
    dataTemp = image2[0].data
    row_count = data.shape[0]
    col_count = data.shape[1]
    flaggedPixels = 0
    # move through each pixel
    rejDeviationFraction = []
    for row in range(row_count):
        for col in range(col_count):
            pixel = [data[row][col]]
            # define the M pixels to its left and right
            pixel_set = []
            for j in range(1, M + 1):
                try:
                    pixel_set.append(data[row][col - j])
                except:
                    # pixel_set.append(data[row][col - j])
                    continue
                try:
                    pixel_set.append(data[row][col + j])
                except:
                    continue
            # populate sets with the middle pixel and find the median
            pixel_set.extend(pixel)
            # populate set of absolute deviations

            # retrieve the rejection factor from the original absdev set
            swag = 0
            pixel_set = sorted(pixel_set)
            while swag == 0:
                pixel_median = median(pixel_set)
                # populate set of absolute deviations
                rawDev = (pixel_set - pixel_median)
                absdev = sorted(abs(rawDev))
                rejection_factor, sigma = rejectionGenerator(absdev, f)
                # absdevPixel = abs(pixel - pixel_median)
                if abs(absdev[-1]) > rejection_factor:
                    if abs(pixel - pixel_median) > rejection_factor:
                        dataTemp[row][col] = 1
                        flaggedPixels += 1
                        # rejectionDeviation = sigma * sqrt(2) * special.erfinv(1 - (0.5 / (len(absdev))))
                        # rejDeviationFraction.append(absdevPixel / rejectionDeviation)
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
    return image2

