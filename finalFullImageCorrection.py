from astropy.io import fits
from columnFlagInitial import columnFlagger
from columnLocator import columnLocator
from hotPixelHunter import hotPixelHunter
from linearColumnCorrection import linearColumnCorrector
from pixelEradicatorMult import pixel_linearmult

image = fits.open('brokenColumnP6.fits')
image2 = fits.open('brokenColumnP6.fits')
linearPixelFlaggedImage = pixel_linearmult(10, image, image2, 1)
dataFlagged, columnIndexes = columnLocator(linearPixelFlaggedImage, 1)
badPixels = hotPixelHunter(linearPixelFlaggedImage, 2, image, image2, 1, 1, dataFlagged, columnIndexes)
[output1] = linearColumnCorrector(badPixels, dataFlagged, image, image2)
output1.writeto("FinalFull.fits", overwrite=True)

image.close()
