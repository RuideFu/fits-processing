from astropy.io import fits
from pixelEradicator import pixel_eradicator
from pixelEradicatorMult import pixel_eradicatormult
from pixelEradicatorSDMedian import pixel_eradicatorSDMedian
from columnFlagInitial import columnFlagger
from hotPixelHunter import hotPixelHunter
from columnLocator import columnLocator
from fitsSubtraction import fitsElimination

# Read in files
# have to do one at  time for some reason
image = fits.open('brokenColumnP6.fits')
image2 = fits.open('brokenColumnP6.fits')
imageBroke = fits.open('M10NewCorrection.fits')
imageCol = fits.open('M10Final.fits')
imageHot1 = fits.open('M1FirstHotPixel.fits')
imageHot2 = fits.open('M2FirstHotPixel.fits')
# eradicate the bad pixels, M = 1, 2, 3, 4, 5
# [output1] = pixel_eradicatormult(5, image, image2, 2)
# [output2] = columnFlagger(imageBroke)
[output3] = hotPixelHunter(1, image, image2, imageCol, 1)
# [output4] = columnLocator(imageBroke, 2)
# [output5] = fitsElimination(imageHot1, imageHot2)
# overwrite the image
# output1.writeto("M5newFactorRejection.fits", overwrite=True)
# output2.writeto("swagger.fits", overwrite=True)
output3.writeto("M2FirstHotPixel.fits", overwrite=True)
# output4.writeto("M10Final.fits", overwrite=True)
# output5.writeto("M12Subbed.fits", overwrite=True)
# close the image
image.close()
