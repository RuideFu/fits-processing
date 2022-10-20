from os import remove

import numpy as np
from scipy import special
from numpy import median, floor, sqrt


def pixel_eradicatorSDMedian(M, image, image2):
    # read in the images and get their data
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
            for j in range(1, M + 1):
                try:
                    pixel_set.append(data[row][col - j])
                except:
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
            while swag == 0:
                # populate set of absolute deviations
                pixelmedian = median(pixel_set)
                rejection_factor = rejectionGenerator(pixel_set)
                # print('Set: ', pixel_set, 'Rejection: ', rejection_factor)
                if abs(pixel - pixelmedian) > rejection_factor:
                    dataTemp[row][col] = 100
                    flaggedPixels += 1
                    swag = 1
                else:
                    annihilate = []
                    for i in range(len(pixel_set)):
                        if abs(pixel_set[i] - pixelmedian) > rejection_factor:
                            annihilate.append(i)
                    pixel_set = [v for i, v in enumerate(pixel_set) if i not in annihilate]
                if len(annihilate) == 0:
                    dataTemp[row][col] = 0
                    swag = 1

    # Apply new data
    image2[0].data = dataTemp

    # percent rejected
    print('Percent pixels rejected: ', flaggedPixels / (2048 * 2064))

    return [image2]


# def rejectionGenerator(pixelSet):
    # rejection_factor = np.std(pixelSet, ddof=1) * sqrt(2) * special.erfinv(1 - (0.5 / len(pixelSet)))
    # return rejection_factor

def rejectionGenerator(pixelSet):
    N = len(pixelSet)
    # now we have the final set to be tested (absdev) we find the rejection factor
    pixelMedian = median(pixelSet)
    variance = sum(((x - pixelMedian) * (x - pixelMedian)) for x in pixelSet) / (N - 1)
    sigma = sqrt(variance)
    rejection_factor = sigma * sqrt(2) * special.erfinv(1 - (0.5 / N))
    return rejection_factor
