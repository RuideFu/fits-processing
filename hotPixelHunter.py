from os import remove

import numpy as np
from scipy import special
from numpy import median, floor, sqrt
from columnLocator import columnLocator
from rejectionGenerator import rejectionGenerator


def hotPixelHunter(pixelFlaggedImage, M, image, image2, f, p):
    # read in the images and get their data
    # dataFlagged = columnLocator(brokenImage)
    dataFlagged, columnIndexes = columnLocator(pixelFlaggedImage, f)
    dataFlagged = dataFlagged[0].data
    data = image[0].data
    dataTemp = image2[0].data
    row_count = data.shape[0]
    col_count = data.shape[1]
    flaggedPixels = 0
    # rejDeviationFraction = []
    # move through each pixel
    for row in range(row_count):
        for col in range(col_count):
            pixel = [data[row][col]]
            # define the M pixels to its left and right
            pixel_set = []

            for j in range(0, (2 * M) + 1):
                for i in range(0, (2 * M) + 1):
                    try:
                        if dataFlagged[(row - M) + i][(col - M) + j] > 0:
                            continue
                        else:
                            try:
                                dangerRegion = 0
                                # keep this for now, later you'll run through like normal, then recalculate for regions
                                # in flagged columns
                                for m in columnIndexes:
                                    if col == m:
                                        dangerRegion = 1
                                if dangerRegion == 1:
                                    if (col - M) + j != col or ((col - M) + j == col and (row - M) + i == row):
                                        pixel_set.append(data[(row - M) + i][(col - M) + j])
                                else:
                                    pixel_set.append(data[(row - M) + i][(col - M) + j])
                            except:
                                continue

                    except:
                        continue
            if len(pixel_set) == 1:
                pixel_set = []
                for i in range(0, (2 * M) + 1):
                    try:
                        if dataFlagged[(row - M) + i][col] > 0:
                            continue
                        else:
                            try:
                                pixel_set.append(data[(row - M) + i][col])
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
                rejection_factor, sigma = rejectionGenerator(absdev, p)
                # absdevPixel = abs(pixel - pixel_median)
                if abs(absdev[-1]) > rejection_factor:
                    if abs(pixel - pixel_median) > rejection_factor:
                        dataTemp[row][col] = 100
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
    # with open('rejectionDeviationM1Hot.txt', 'w') as f:
    #     f.write('\n'.join(str(x) for x in rejDeviationFraction))
    # percent rejected
    print('Percent pixels rejected: ', flaggedPixels / (2048 * 2064))
    return image2
