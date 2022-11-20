from astropy.io import fits

from columnFlagInitial import columnFlagger
from columnLocator import columnLocator
from hotPixelHunter import hotPixelHunter
from linearColumnCorrection import linearColumnCorrector
from pixelEradicatorMult import pixel_linearmult
import time

# This is the file I've used to initialize tests
# Read in files
# have to do one at  time for some reason
image = fits.open('brokenColumnP6.fits')
image2 = fits.open('brokenColumnP6.fits')
# imagePixel = fits.open('M5Lorentzian.fits')
# imageCol = fits.open('M10columnLocated.fits')
# imageHot1 = fits.open('Number2.fits')
# imagePixel = fits.open('Number3_3.fits')
# imagePixelM10 = fits.open('M10NewCorrection.fits')
# eradicate the bad pixels, M = 1, 2, 3, 4, 5
start = time.time()
[output1] = pixel_linearmult(10, image, image2, 0)
# [output2] = columnFlagger(imageBroke, 1)
# [output3] = hotPixelHunter(imageBroke, 2, image, image2, 1, 1)
# [output4] = columnLocator(imagePixel, 1)
# [output5] = linearColumnCorrector(imagePixel, imageCol, image, image2)
# overwrite the image
output1.writeto("M10nuinf.fits", overwrite=True)
# output2.writeto("swagger.fits", overwrite=True)
# output3.writeto("Number3_3.fits", overwrite=True)
# output4.writeto("LorentzianM5Example.fits", overwrite=True)
# output5.writeto("Number4_3.fits", overwrite=True)
# close the image
image.close()
end = time.time()
print("This took: ", end - start, " seconds")
