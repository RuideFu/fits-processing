from astropy.io import fits
from pixelEradicator import pixel_eradicator
# Read in files
# have to do one at  time for some reason
image = fits.open('brokenColumnP6.fits')
image2 = fits.open('brokenColumnP6.fits')
# eradicate the bad pixels, M = 1, 2, 3, 4, 5
# [output1] = pixel_eradicator(1, image, image2)
# [output2] = pixel_eradicator(2, image, image2)
# [output3] = pixel_eradicator(3, image, image2)
# [output4] = pixel_eradicator(4, image)
[output5] = pixel_eradicator(5, image, image2)
# overwrite the image
# output1.writeto("M1.fits", overwrite=True)
# output2.writeto("M2tosend.fits", overwrite=True)
# output3.writeto("M3.fits", overwrite=True)
# output4.writeto("M4Single3b.fits", overwrite=True)
output5.writeto("M9.fits", overwrite=True)
# close the image
image.close()
