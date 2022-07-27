from astropy.io import fits
from pixelEradicator import pixel_eradicator
# Read in files
image = fits.open('brokenColumnP6.fits')
# eradicate the bad pixels, M = 1
output = pixel_eradicator(2, image)
# overwrite the image
output.writeto("eradicated.fits", overwrite=True)
# close the image
image.close()
