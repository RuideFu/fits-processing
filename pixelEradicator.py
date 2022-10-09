from os import remove

import numpy as np
from scipy import special
from numpy import median, floor, sqrt


def pixel_eradicator(M, image, image2):
    # read in the images and get their data
    data = image[0].data
    dataTemp = image2[0].data
    row_count = data.shape[0]
    col_count = data.shape[1]
    flaggedPixels = 0
    # print('Dan Pixel: ', data[499][1158])
    # print('thang: ', rejectionGenerator([75, 73, 88, 85, -185, 702, -193, 106, 84, 71, 98, 79]))
    # special_set = [data[160][496], data[159][496], data[158][496], data[157][496], data[156][496], data[155][496], data[161][496], data[162][496], data[163][496], data[164][496], data[165][496]]
    # special_set = abs(special_set - median(special_set))
    # special_set = sorted(special_set)
    # print('Rejection:', rejectionGenerator(special_set), 'Set:', special_set)
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
            pixel_median = median(pixel_set)
            # populate set of absolute deviations
            absdev = abs(pixel_median - pixel_set)
            absdev = sorted(absdev)
            # retrieve the rejection factor from the original absdev set
            rejection_factor = rejectionGenerator(absdev)
            ##identified candidate for problem child
            # if pixel == data[588][1160]:
            #     print('Pixel Set:', pixel_set, 'Pixel Median', pixel_median, 'absdev: ', absdev, 'Pixel: ', pixel)
            swag = 0
            while swag == 0:
                # entryLength = len(pixel_set)
                pixel_set = sorted(pixel_set)
                pixel_median = median(pixel_set)
                # populate set of absolute deviations
                rawDev = (pixel_set - pixel_median)
                absdev = abs(rawDev)
                absdev = sorted(absdev)
                # if pixel == data[588][1160]:
                #     print('Reject Factor: ', rejectionGenerator(absdev))
                #     print('Pixel: ', pixel, 'Pixel Set', pixel_set)
                #     print(absdev[-1], abs(pixel - pixel_median))
                if abs(absdev[-1]) > rejection_factor:
                    if absdev[-1] == abs(pixel - pixel_median):
                        # if pixel == data[597][1161]:
                        #     print('Line 55')
                        dataTemp[row][col] = 100
                        flaggedPixels += 1
                        swag = 1
                        # print(absdev, abs(pixel - pixel_median), 'Row:', row, 'Col:', col, rejection_factor, rejectionGenerator(absdev))
                        continue
                    else:
                        for i in range(len(rawDev)):
                            if abs(rawDev[i]) == absdev[-1]:
                                annihilate = i
                        pixel_set.pop(annihilate)

                else:
                    dataTemp[row][col] = 0
                    swag = 1
                    continue
                # exitLength = len(pixel_set)
                if len(absdev) > 1:
                    rejection_factor = rejectionGenerator(absdev)
                else:
                    dataTemp[row][col] = 100
                    flaggedPixels += 1
                    swag = 1
                    # print(absdev, abs(pixel - pixel_median), 'flagged from reduction')
                    continue
                # if entryLength == exitLength:
                #     if abs(pixel_median - pixel) > rejection_factor:
                #         print('Line 82')
                #         dataTemp[row][col] = 100
                #         flaggedPixels += 1
                #         # print(absdev, abs(pixel - pixel_median), 'natural flag')
                #     else:
                #         print('Line 87')
                #         dataTemp[row][col] = 0
                #     swag = 1
                #     continue

    # Apply new data
    image2[0].data = dataTemp

    # percent rejected
    print('Percent pixels rejected: ', flaggedPixels / (2048 * 2064))

    return [image2]


def rejectionGenerator(absdev):
    N = len(absdev)

    # now we have the final set to be tested (absdev) we find the rejection factor

    correction = 1 + (1.7 / N)
    i = floor(0.683 * N)
    i_minus = 0.683 * (N - 1)
    sigma = (absdev[int(i) - 1] + (absdev[int(i)] - absdev[int(i) - 1]) * (i_minus - floor(i_minus))) * correction
    rejection_factor = sigma * sqrt(2) * special.erfinv(1 - (0.5 / N))
    return rejection_factor
