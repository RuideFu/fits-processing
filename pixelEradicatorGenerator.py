from astropy.io import fits
from pixelEradicator import pixel_eradicator
from pixelEradicatorMult import pixel_eradicatormult
from pixelEradicatorSDMedian import pixel_eradicatorSDMedian
from columnFlagInitial import columnFlagger
from hotPixelHunter import hotPixelHunter
# Read in files
# have to do one at  time for some reason
image = fits.open('brokenColumnP6.fits')
image2 = fits.open('brokenColumnP6.fits')
imageBroke = fits.open('M10NewCorrection.fits')
# eradicate the bad pixels, M = 1, 2, 3, 4, 5
# [output1] = pixel_eradicatormult(10, image, image2)
# [output2] = columnFlagger(imageBroke)
[output3] = hotPixelHunter(1, image, image2)
# [output4] = pixel_eradicator(4, image)
# [output5] = pixel_eradicator(5, image, image2)
# overwrite the image
# output1.writeto("M10NewCorrection.fits", overwrite=True)
# output2.writeto("swagger.fits", overwrite=True)
# output3.writeto("M3.fits", overwrite=True)
# output4.writeto("M4Single3b.fits", overwrite=True)
# output5.writeto("M9.fits", overwrite=True)
# close the image
image.close()
