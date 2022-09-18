from os import remove

import numpy as np
from scipy import special
from numpy import median, floor, sqrt

## IMPORTANT you are an idiot, write the flagged pixels into a new image file you are overwriting you are stupid!!!!


def pixel_eradicator(M, image, image2):
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
            # pick up later here 08-21-2022 -- Do not need to make pixel memory, just loop through the set
            pixel_median = median(pixel_set)
            # populate set of absolute deviations
            absdev = abs(pixel_median - pixel_set)
            absdev = sorted(absdev)
            # print(absdev)

            # retrieve the rejection factor from the original absdev set
            rejection_factor = rejectionGenerator(absdev)
            # # now we decide whether to reject the pixel in the middle or not
            #
            # if abs(pixel_median - pixel) > rejection_factor:
            #       data[row][col] = 100
            #       print('think fast chucklenuts')
            # else:
            #     data[row][col] = 0
            # print('go ahead and cry, baby')

            # dan wants us to try a new way, now we are going to move through the absdev set from high to low and see if
            # anything gets rejected, if anything around our target is rejected we cast them out and recalculate, if our
            # target is rejected too, we flag it and move on
            swag = 0
            while swag == 0:
                # problem -- pixel median not updating correctly with pixel, go get some lunch
                # Here we are mass rejecting pixels that do not make the cut, but we need to switch to rejecting only
                # one at a time
                # for p in range(len(absdev)):
                #     # print('myasshurts', len(absdev))
                #     if abs(pixel_median - absdev[int(p)]) < rejection_factor:
                #         flaggedSet.append(absdev[int(p)])
                # only remove the pixel with the highest deviation from absdev and repeat
                entryLength = len(pixel_set)
                pixel_set = sorted(pixel_set)
                if abs(absdev[-1]) > rejection_factor:
                    if (absdev[-1]) == abs(pixel - pixel_median):
                        swag = 1
                        dataTemp[row][col] = 30 * np.pi
                        flaggedPixels += 1
                        print(absdev, abs(pixel - pixel_median), 'flagged from priority removal')
                        continue
                    else:
                        pixel_set.pop(-1)
                    # print(absdev)
                else:
                    dataTemp[row][col] = 0
                    swag = 1
                    continue
                exitLength = len(pixel_set)
                pixel_median = median(pixel_set)
                # populate set of absolute deviations
                absdev = abs(pixel_median - pixel_set)
                absdev = sorted(absdev)
                # print(absdev)
                if len(absdev) > 1:
                    rejection_factor = rejectionGenerator(absdev)
                else:
                    dataTemp[row][col] = 30 * np.pi
                    flaggedPixels += 1
                    swag = 1
                    print(absdev, abs(pixel - pixel_median), 'flagged from reduction')
                    continue
                if entryLength == exitLength:
                    if abs(pixel_median - pixel) > rejection_factor:
                        dataTemp[row][col] = 30 * np.pi
                        flaggedPixels += 1
                        print(absdev, abs(pixel - pixel_median), 'natural flag')
                    else:
                        dataTemp[row][col] = 0
                    swag = 1
                    continue
                # print(absdev, abs(pixel_median - pixel))
                # if abs(pixel_median - pixel) > rejection_factor:
                #     data[row][col] = 30 * np.pi
                #     flaggedPixels += 1
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
    if N < 4:
        sigma = (absdev[int(i) - 1] + (absdev[int(i)] - absdev[int(i) - 1]) * (i_minus - floor(i_minus))) * correction
    else:
        sigma = (absdev[int(i)] + (absdev[int(i) + 1] - absdev[int(i)]) * (i_minus - floor(i_minus))) * correction
    rejection_factor = sigma * sqrt(2) * special.erfinv(1 - (0.5 / N))
    # print('rejection', rejection_factor)
    # print('pixel', abs(pixel_median - pixel))
    return rejection_factor
