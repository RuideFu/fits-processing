from os import remove

import numpy as np
from scipy import special
from numpy import sqrt, linspace
from columnFlagInitial import columnFlagger
import matplotlib.pyplot as plt


def columnLocator(pixelFlaggedImage, f):
    columnIndexes, mu, sigma, columnVals = columnFlagger(pixelFlaggedImage, f)
    data = pixelFlaggedImage[0].data
    dataTemp = pixelFlaggedImage[0].data * 0
    row_count = data.shape[0]
    col_count = data.shape[1]
    N_R = row_count
    NColBase = []
    for i in range(len(columnIndexes)):
        NColBase.append(columnVals[(columnIndexes[i])])
    NColMin = []
    for i in range(len(NColBase)):
        NColMin.append(N_R * ((NColBase[i] - mu) / (N_R - mu)))
    # get the values from indexed columns and find the cdf for each
    flaggedColData = np.zeros((len(columnIndexes), N_R))
    for col in range(len(columnIndexes)):
        for row in range(row_count):
            # define the M pixels to its left and right
            flaggedColData[col, row] = flaggedColData[col, row] + data[row, columnIndexes[col]]
            # print(data[row, columnIndexes[1]], 'Row: ', row, 'COl: ', columnIndexes[1])
    cdf = []
    # print(NColMin)
    for n in range(len(columnIndexes)):
        for i in range(len(flaggedColData)):
            cdf.append(np.cumsum(flaggedColData[i]))

    N_LOW = []
    N_HIGH = []
    for p in range(len(NColMin)):
        N_L = 0
        N_H = N_R - 1
        small = N_R

        for i in range(N_R - int(NColMin[p])):
            for j in range(i + int(NColMin[p]) - 1, N_R - 1):
                if (j - i + 1) < small:
                    # print('j', j, 'i', i)
                    if i > 0:
                        x = cdf[p][N_R - 1] - (cdf[p][j] - cdf[p][i])
                    if i == 0:
                        x = cdf[p][N_R - 1] - (cdf[p][j])
                    # print('x', x)
                    muPrime = mu * ((N_R - (j - i + 1)) / N_R)
                    # print('mu', muPrime)
                    sigmaPrime = sigma * ((N_R - (j - i + 1)) / N_R)
                    # print('sugma', sigmaPrime)
                    # print('oof: ', abs(x - muPrime), 'swag: ', sigmaPrime * sqrt(2) * special.erfinv(1 - (0.5 / (N_R - (j - i)))))
                    if abs(x - muPrime) < sigmaPrime * sqrt(2) * special.erfinv(1 - (0.5 / (N_R - (j - i + 1)))):
                        # print('eeeeee')
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
        # print('Col: ', columnIndexes[p], 'High: ', N_H, 'Low: ', N_L)
        N_LOW.append(N_L)
        N_HIGH.append(N_H)

    # columnRanges = np.array((columnIndexes, N_LOW, N_HIGH))
    # print(columnRanges)
    for row in range(row_count):
        for col in range(len(columnIndexes)):
            if N_LOW[col] <= row <= N_HIGH[col]:
                dataTemp[row][columnIndexes[col]] = 1
    #
    pixelFlaggedImage[0].data = dataTemp

    return pixelFlaggedImage, columnIndexes
