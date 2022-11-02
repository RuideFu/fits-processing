import numpy as np
from scipy import special
from numpy import sqrt
from columnFlagInitial import columnFlagger
# Number 2
# This file uses the pixel flagged image generated by the first robust rejection method (in pixelEradicatorMult.py),
# finds the indexes using columnFlagInitial.py, and calculates the smallest area in each column where the regions
# above and below are not statistically outlying, effectively finding the length of the broken column


def columnLocator(pixelFlaggedImage, f):
    # calculate column indexes
    columnIndexes, mu, sigma, columnVals = columnFlagger(pixelFlaggedImage, f)
    # Define flagged image date
    data = pixelFlaggedImage[0].data
    dataTemp = pixelFlaggedImage[0].data * 0
    row_count = data.shape[0]
    col_count = data.shape[1]
    N_R = row_count
    NColBase = np.zeros(len(columnIndexes))
    # make a list of the number of rejected pixels in each flagged column
    for i in range(len(columnIndexes)):
        NColBase[i] = columnVals[(columnIndexes[i])]
    NColMin = np.zeros(len(NColBase))
    for i in range(len(NColBase)):
        NColMin[i] = (N_R * ((NColBase[i] - mu) / (N_R - mu)))
    # find the cdf for each broken column
    flaggedColData = np.zeros((len(columnIndexes), N_R))
    for col in range(len(columnIndexes)):
        for row in range(row_count):
            flaggedColData[col, row] = data[row, columnIndexes[col]]
    cdf = []
    for n in range(len(columnIndexes)):
        for i in range(len(flaggedColData)):
            cdf.append(np.cumsum(flaggedColData[i]))
    # below is Dan's method for moving through each column and finding maximum regions above and below that are not
    # statistically outlying
    N_LOW = []
    N_HIGH = []
    # define the columns we will be analyzing
    for p in range(len(NColMin)):
        N_L = 0
        N_H = N_R - 1
        small = N_R
        # ensure that columns are not flagged for having too few flagged pixels
        if columnVals[(columnIndexes[p])] > mu:
            for i in range(N_R - int(NColMin[p])):
                for j in range(i + int(NColMin[p]) - 1, N_R - 1):
                    if (j - i + 1) < small:
                        if i > 0:
                            x = cdf[p][N_R - 1] - (cdf[p][j] - cdf[p][i])
                        if i == 0:
                            x = cdf[p][N_R - 1] - (cdf[p][j])
                        muPrime = mu * ((N_R - (j - i + 1)) / N_R)
                        sigmaPrime = sigma * ((N_R - (j - i + 1)) / N_R)
                        if abs(x - muPrime) < sigmaPrime * sqrt(2) * special.erfinv(1 - (0.5 / (N_R - (j - i + 1)))):
                            small = j - i + 1
                            N_L = i
                            N_H = j
                    if j - i + 1 == small:
                        if i > 0:
                            x = cdf[p][N_R - 1] - (cdf[p][j] - cdf[p][i])
                        if i == 0:
                            x = cdf[p][N_R - 1] - (cdf[p][j])
                        muPrime = mu * ((N_R - (j - i + 1)) / N_R)
                        sigmaPrime = sigma * ((N_R - (j - i + 1)) / N_R)
                        if abs(x - muPrime) < sigmaPrime * sqrt(2) * special.erfinv(1 - (0.5 / (N_R - (j - i + 1)))):
                            if i < N_L:
                                N_L = i
                            if j > N_H:
                                N_H = j
            N_LOW.append(N_L)
            N_HIGH.append(N_H)
    # flag the columns based on the regions we just found for each
    for row in range(row_count):
        for col in range(len(columnIndexes)):
            if N_LOW[col] <= row <= N_HIGH[col]:
                dataTemp[row][columnIndexes[col]] = 1

    pixelFlaggedImage[0].data = dataTemp

    return pixelFlaggedImage, columnIndexes
