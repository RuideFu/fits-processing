from os import remove
import numpy as np
from scipy import special
from numpy import median, floor, sqrt


def linearColumnCorrector(badPixels, badColumns, rawImage, templateImage):
    imagedata = rawImage[0].data
    pixelData = badPixels[0].data
    columnData = badColumns[0].data
    tempData = templateImage[0].data

    row_count = imagedata.shape[0]
    col_count = imagedata.shape[1]

    for row in range(row_count):
        for col in range(col_count):
            if columnData[row][col] > 0:
                correctValSet = []
                i = 0
                valCounter = 0
                while valCounter < 2:
                    if col + i > col_count - 1:
                        valCounter = 100
                        continue
                    if columnData[row][col + i] == 0 and pixelData[row][col + i] == 0:
                        correctValSet.append(imagedata[row][col + i])
                        valCounter = valCounter + 1
                        i = i + 1
                    else:
                        i = i + 1
                i = 0
                valCounter = 0
                while valCounter < 2:
                    if col - i < 0:
                        valCounter = 100
                        continue
                    if columnData[row][col - i] == 0 and pixelData[row][col - i] == 0:
                        correctValSet.append(imagedata[row][col - i])
                        valCounter = valCounter + 1
                        i = i + 1
                    else:
                        i = i + 1
                tempData[row][col] = np.average(correctValSet)

            if pixelData[row][col] > 0:
                correctValSet = []
                valCounter = 0
                i = 1
                w = 1
                t = 1
                d = 1
                first = 0
                botCount = 0
                topCount = 0
                leftCount = 0
                rightCount = 0
                testx = [-1, 1]
                testy = [-1, 1]
                while valCounter < 4:
                    # top center
                    if first == 0:
                        for x in testx:
                            for y in testy:
                                try:
                                    if columnData[row + y][col + x] == 0 and pixelData[row + y][col + x] == 0:
                                        correctValSet.append(imagedata[row + x][col + y])
                                except:
                                    continue
                        first = 1

                    if col - t < 0 and leftCount == 0:
                        valCounter = valCounter + 1
                        leftCount = 1
                    if col + d > col_count - 1 and rightCount == 0:
                        valCounter = valCounter + 1
                        rightCount = 1
                    if row - i < 0 and botCount == 0:
                        valCounter = valCounter + 1
                        botCount = 1
                    if row + w > row_count - 1 and topCount == 0:
                        valCounter = valCounter + 1
                        topCount = 1
                    if botCount == 0:
                        if columnData[row - i][col] == 0 and pixelData[row - i][col] == 0:
                            correctValSet.append(imagedata[row - i][col])
                            botCount = 1
                            valCounter = valCounter + 1
                        else:
                            i = i + 1

                    if topCount == 0:
                        if columnData[row + w][col] == 0 and pixelData[row + w][col] == 0:
                            correctValSet.append(imagedata[row + w][col])
                            topCount = 1
                            valCounter = valCounter + 1
                        else:
                            w = w + 1
                    if leftCount == 0:
                        if columnData[row][col - t] == 0 and pixelData[row][col - t] == 0:
                            correctValSet.append(imagedata[row][col - t])
                            leftCount = 1
                            valCounter = valCounter + 1
                        else:
                            t = t + 1

                    if rightCount == 0:
                        if columnData[row][col + d] == 0 and pixelData[row][col + d] == 0:
                            correctValSet.append(imagedata[row][col + d])
                            rightCount = 1
                            valCounter = valCounter + 1
                        else:
                            d = d + 1

                tempData[row][col] = np.average(correctValSet)
    rawImage[0].data = tempData
    return rawImage
