from numpy import sort, median


def pixel_eradicator(M, image):
    # read in the images and get their data
    data = image[0].data

    row_count = data.shape[0]
    col_count = data.shape[1]
    # move through each pixel
    for row in range(row_count):
        for col in range(col_count):
            pixel = data[row][col]
            # define the M pixels to its left and right
            pixels_left = []
            pixels_right = []
            for i in range(1, M):
                pixels_left[i] = [data[row-i][col]]
                pixels_right[i] = [data[row+i][col]]

            # find the median
            pixel_set = (pixel, pixels_left, pixels_right)
            pixel_median = median(pixel_set)
            # calculate sigma
            # N = 2*M + 1
            # for j in range(N):
            print(pixel_set), print(pixel_median)
