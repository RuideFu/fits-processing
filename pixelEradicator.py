from math import erf

from numpy import median, floor, sqrt


def pixel_eradicator(M, image):
    # read in the images and get their data
    data = image[0].data
    row_count = data.shape[0]
    col_count = data.shape[1]
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
            # calculate sigma
            absdev = [abs(pixel_median - pixel) for pixel in pixel_set]
            absdev = sorted(absdev)
            N = absdev[len(absdev)]
            correction = 1 + (1.7 / N)
            i = floor(0.683 * N)
            i_minus = 0.683 * (N - 1)

            sigma = (absdev[i] + ((absdev[i + 1] - absdev[i]) * (i_minus - floor(i_minus)))) * correction

            rejection_factor = sigma * sqrt(2) * erf(1 - 0.5/N) ** -1

            if abs(pixel_median - pixel) > rejection_factor:
                data[row][col] = 100
                print('think fast chucklenuts')
            else:
                data[row][col] = 0

    # Apply new data
    image[0].data = data

    return [image]
