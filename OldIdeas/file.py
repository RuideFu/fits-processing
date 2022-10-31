from astropy.io import fits
from util import correction
# Read in files
b_image = fits.open('47_tuc_7165651_R_0010_reduced.fits')
g_image = fits.open('47_tuc_7165651_V_0008_reduced.fits')
r_image = fits.open('47_tuc_7165651_B_0006_reduced.fits')

# for r in range(500):
#     for c in range(500):
#         r_data[r][c] = 0
#
# r_image[0].data = r_data
# r_image.writeto("R_Output.fits", overwrite=True)

[output_r, output_g, output_b] = correction(r_image, g_image, b_image)

output_r.writeto("R_Output.fits", overwrite=True)
output_g.writeto("G_Output.fits", overwrite=True)
output_b.writeto("B_Output.fits", overwrite=True)

# Close images
r_image.close()
g_image.close()
b_image.close()
