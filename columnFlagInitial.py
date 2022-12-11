from numpy import median, zeros

from rejectionGenerator import rejectionGeneratorFinal

# This locates the indexes bad columns in the image by going through each one and doing a robust rejection the same way
# as the flagging of pixels in the first robust rejection method
# The image here is the one produced by flagging pixels in the first robust rejection method


def columnFlagger(image):
    # read in the images and get their data
    data = image[0].data
    row_count = data.shape[0]
    col_count = data.shape[1]
    # move through each pixel
    columnVals = zeros(col_count)
    for col in range(col_count):
        for row in range(row_count):
            # calculate the number of rejections per column
            columnVals[col] = columnVals[col] + data[row][col]
    # proceed with the normal robust rejection method we have been using
    medianColVals = median(columnVals)
    absdevColVals = sorted(abs(columnVals - medianColVals))
    rejectionFactor, superSigma = rejectionGeneratorFinal(absdevColVals, 0)
    flaggedColumns = zeros(col_count)
    flaggedColumnIndexes = []
    for i in range(len(columnVals)):
        if columnVals[i] - medianColVals > rejectionFactor:
            flaggedColumnIndexes.append(i)
            flaggedColumns[i] = 1
        else:
            flaggedColumns[i] = 0
    return flaggedColumnIndexes, medianColVals, superSigma, columnVals
