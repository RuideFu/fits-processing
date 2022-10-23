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
imageBroke = fits.open('Number1.fits')
imageCol = fits.open('M10columnLocated.fits')
imageHot1 = fits.open('Number2.fits')
imagePixel = fits.open('Number3.fits')
imagePixelM10 = fits.open('M10NewCorrection.fits')
# eradicate the bad pixels, M = 1, 2, 3, 4, 5
# [output1] = pixel_eradicatormult(10, image, image2, 1)
# [output2] = columnFlagger(imageBroke)
# [output3] = hotPixelHunter(imageBroke, 2, image, image2, 1, 1)
# [output4] = columnLocator(imageBroke, 1)
[output5] = linearColumnCorrector(imagePixel, imageCol, image, image2)
# overwrite the image
# output1.writeto("Number1.fits", overwrite=True)
# output2.writeto("swagger.fits", overwrite=True)
# output3.writeto("Number3.fits", overwrite=True)
# output4.writeto("Number2.fits", overwrite=True)
output5.writeto("Number4.fits", overwrite=True)
# close the image
image.close()
