from astropy.io import fits
from pixelEradicator import pixel_eradicator
from pixelEradicatorMult import pixel_eradicatormult
from pixelEradicatorSDMedian import pixel_eradicatorSDMedian
from columnFlagInitial import columnFlagger
from hotPixelHunter import hotPixelHunter
from columnLocator import columnLocator
from fitsSubtraction import fitsElimination
from linearColumnCorrection import linearColumnCorrector

# Read in files
# have to do one at  time for some reason
image = fits.open('brokenColumnP6.fits')
image2 = fits.open('brokenColumnP6.fits')
imageBroke = fits.open('M10NewCorrection.fits')
imageCol = fits.open('M10Final.fits')
imageHot1 = fits.open('M1FirstHotPixel.fits')
imagePixel = fits.open('M12Subbed.fits')
# eradicate the bad pixels, M = 1, 2, 3, 4, 5
# [output1] = pixel_eradicatormult(1, image, image2, 1)
# [output2] = columnFlagger(imageBroke)
# [output3] = hotPixelHunter(10, 1, image, image2, 1, 1)
# [output4] = columnLocator(10, image, image2, 1)
[output5] = linearColumnCorrector(imagePixel, imageCol, image, image2)
# overwrite the image
# output1.writeto("dontmatta.fits", overwrite=True)
# output2.writeto("swagger.fits", overwrite=True)
# output3.writeto("M1HotUltimate.fits", overwrite=True)
# output4.writeto("M10NewUlt.fits", overwrite=True)
output5.writeto("M10Corrected.fits", overwrite=True)
# close the image
image.close()
