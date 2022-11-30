from numpy import median
from rejectionGenerator import rejectionGeneratorFinal


# Number 1
# this is the first robust rejection method to find dead columns in an image
# I defined the same image in image and image2 so the sets wouldn't overlap, everything else I tried had an issue for
# some reason


def pixel_linearmult(M, image, image2, nu):
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
                    if (col - j) >= 0:
                        pixel_set.append(data[row][col - j])
                except:
                    continue
                try:
                    pixel_set.append(data[row][col + j])
                except:
                    continue
            # for edge cases
            if len(pixel_set) < (2 * M):
                # find out how many are missing
                missing = (2 * M) - len(pixel_set)
                # for cases on the right side
                if col > col_count / 2:
                    for x in range(missing):
                        pixel_set.append(data[row][(col - (M + 1)) - x])
                # cases on the left side
                else:
                    for x in range(missing):
                        pixel_set.append(data[row][(col + (M + 1)) + x])
            # populate sets with the middle pixel and find the median
            pixel_set.extend(pixel)

            end = 0
            pixel_set = sorted(pixel_set)
            while end == 0:
                pixel_median = median(pixel_set)
                # populate set of absolute deviations\
                # use the raw deviations as an index map to remove pixels from a set if the primary
                # pixel is not rejected
                rawDev = (pixel_set - pixel_median)
                absdev = sorted(abs(rawDev))
                # define the
                # tests to the rejection factor using lorentzians
                # rejection_factor, sigma = rejectionGenerator(absdev, f)
                rejection_factor, sigma = rejectionGeneratorFinal(absdev, nu)
                # check if the largest pixel deviation is outlying
                if len(absdev) == 1:
                    print('doodoo')
                    dataTemp[row][col] = 0
                    end = 1
                    continue

                if abs(absdev[-1]) > rejection_factor:
                    # reject the main pixel if it's too big, flag, and end the loop
                    if abs(pixel - pixel_median) > rejection_factor:
                        dataTemp[row][col] = 1
                        flaggedPixels += 1
                        end = 1
                    # if not remove the outlying pixels from this set that were not the main pixel, and repeat
                    else:
                        annihilate = []
                        for i in range(len(rawDev)):
                            if abs(rawDev[i]) > rejection_factor:
                                annihilate.append(i)
                        pixel_set = [v for i, v in enumerate(pixel_set) if i not in annihilate]
                # if no more rejections no pixel is flagged and the loop ends
                else:
                    dataTemp[row][col] = 0
                    end = 1

    # Apply new data
    image2[0].data = dataTemp

    # percent rejected
    print('Percent pixels rejected: ', flaggedPixels / (2048 * 2064))
    return image2
