from numpy import median
from rejectionGenerator import rejectionGeneratorFinal


# Number 3
# This is the robust pixel flagging algorithm for finding hot pixels AROUND columns
# We define sets surrounding the pixel we are analyzing, and do our normal Cheuvanet rejection with those sets

# PixelflaggedImage is the flagged set from pixeleradicatormult, and the other image is the base image


def hotPixelHunter(pixelFlaggedImage, M, image, image2, f, p, dataFlagged, columnIndexes):
    # read in the images and get their data
    # Define the matrix (dataFlagged) that we will use to skip pixels we already flagged as dead columns
    # keeping this here as a reference if we need to change, (linear) pixelFlaggedImage and f can be used with the line
    # below to find the indexes of the columns we need, but I've chosen to skip that and have the output of
    # columnLocator be an input for this function (dataFlagged), let me know if you want this changed
    # dataFlagged, columnIndexes = columnLocator(pixelFlaggedImage, f)
    dataFlagged = dataFlagged[0].data
    data = image[0].data
    dataTemp = image2[0].data
    row_count = data.shape[0]
    col_count = data.shape[1]
    flaggedPixels = 0
    # move through each pixel
    for row in range(row_count):
        for col in range(col_count):
            pixel = [data[row][col]]
            pixel_set = []
            # create sets of pixels surrounding the one we are analyzing, going either 1 or 2 rows out (sets of 8 and 24
            # pixes surrounding the one we are analyzing)
            for j in range(0, (2 * M) + 1):
                for i in range(0, (2 * M) + 1):
                    try:
                        if dataFlagged[(row - M) + i][(col - M) + j] > 0:
                            continue
                        else:
                            try:
                                # determine if we should check if our main pixel is potentially in or around a dead
                                # column, and append it to the set accordingly
                                dangerRegion = 0
                                for m in columnIndexes:
                                    if m - M <= col <= m + M:
                                        dangerRegion = 1
                                # avoid flagged pixels
                                if dangerRegion == 1:
                                    if (col - M) + j != col or ((col - M) + j == col and (row - M) + i == row):
                                        pixel_set.append(data[(row - M) + i][(col - M) + j])
                                # append like normal if not in a bad column
                                else:
                                    pixel_set.append(data[(row - M) + i][(col - M) + j])
                            except:
                                continue

                    except:
                        continue
            # for a special case where the pixel we are analyzing is surrounded by columns and/or on an edge of an image
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
            end = 0
            pixel_set = sorted(pixel_set)
            while end == 0:
                # check if our pixel is in a dead column, and skip it if it is
                if dataFlagged[row][col] == 1:
                    dataTemp[row][col] = 0
                    end = 1
                    continue
                pixel_median = median(pixel_set)
                # populate set of absolute deviations
                rawDev = (pixel_set - pixel_median)
                absdev = sorted(abs(rawDev))
                if len(absdev) <= 1:
                    dataTemp[row][col] = 0
                    end = 1
                    continue
                # define the robust rejection criterion for each set
                rejection_factor, sigma = rejectionGenerator(absdev, p)
                if abs(absdev[-1]) > rejection_factor:
                    if abs(pixel - pixel_median) > rejection_factor:
                        dataTemp[row][col] = 100
                        flaggedPixels += 1
                        end = 1
                    else:
                        # remove the outlying pixels that are not the one we are analyzing from the set, and repeat
                        annihilate = []
                        for i in range(len(rawDev)):
                            if abs(rawDev[i]) > rejection_factor:
                                annihilate.append(i)
                        pixel_set = [v for i, v in enumerate(pixel_set) if i not in annihilate]

                else:
                    dataTemp[row][col] = 0
                    end = 1

    # Apply new data
    image2[0].data = dataTemp
    badPixels = image2
    # percent rejected
    print('Percent pixels rejected: ', flaggedPixels / (2048 * 2064))
    return badPixels
