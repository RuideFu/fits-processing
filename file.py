from astropy.io import fits

b_image = fits.open('47_tuc_7165651_B_0006_reduced.fits')
v_image = fits.open('47_tuc_7165651_V_0008_reduced.fits')
r_image = fits.open('47_tuc_7165651_R_0010_reduced.fits')

print(b_image.info())
print(v_image.info())
print(r_image.info())

b_image.close()
v_image.close()
r_image.close()
