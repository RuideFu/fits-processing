from astropy.io import fits
from columnLocator import columnLocator
from hotPixelHunter import hotPixelHunter
from linearColumnCorrection import linearColumnCorrector
from pixelEradicatorMult import pixel_linearmult

image = fits.open('brokenColumnP6.fits')
image2 = fits.open('brokenColumnP6.fits')
linearPixelFlaggedImage = pixel_linearmult(10, image, image2, 1)
# have to restate image, image2 and create an alias from linearPixelFlaggedImage so that nothing is overwritten
imagePixelFlag = linearPixelFlaggedImage
dataFlagged, columnIndexes = columnLocator(imagePixelFlag, 1)
image = fits.open('brokenColumnP6.fits')
image2 = fits.open('brokenColumnP6.fits')
badPixels = hotPixelHunter(linearPixelFlaggedImage, 2, image, image2, 1, 1, dataFlagged, columnIndexes)
image = fits.open('brokenColumnP6.fits')
image2 = fits.open('brokenColumnP6.fits')
[output1] = linearColumnCorrector(badPixels, dataFlagged, image, image2)
output1.writeto("FinalFull.fits", overwrite=True)

image.close()
