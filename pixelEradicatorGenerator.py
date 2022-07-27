from astropy.io import fits
from pixelEradicator import pixel_eradicator
# Read in files
image = fits.open('brokenColumnP6.fits')
# eradicate the bad pixels, M = 1, 2, 3, 4, 5
output1 = pixel_eradicator(1, image)
output2 = pixel_eradicator(2, image)
output3 = pixel_eradicator(3, image)
output4 = pixel_eradicator(4, image)
output5 = pixel_eradicator(5, image)
# overwrite the image
output1.writeto("eradicatedM1.fits", overwrite=True)
output2.writeto("eradicatedM2.fits", overwrite=True)
output3.writeto("eradicatedM3.fits", overwrite=True)
output4.writeto("eradicatedM4.fits", overwrite=True)
output5.writeto("eradicatedM5.fits", overwrite=True)
# close the image
image.close()
