from math import log10


def filter_wavelength(filter):
    wavelength = {
        "U": 0.366,
        "B": 0.438,
        "V": 0.545,
        "R": 0.641,
        "I": 0.798,
        "u'": 0.35,
        "g\'": 0.475,
        "r\'": 0.6222,
        "i\'": 0.7362,
        "z\'": 0.9049,
        "J": 1.235,
        "H": 1.662,
        "Ks": 2.159,
    }
    return wavelength[filter]


def correction(x_image, y_image, z_image):
    # Assign headers
    x_header = x_image[0].header
    y_header = y_image[0].header
    z_header = z_image[0].header

    # Identify filters
    x_filter = x_header['Filter']
    y_filter = y_header['Filter']
    z_filter = z_header['Filter']

    # Lookup wavelength
    x_wavelength = filter_wavelength(x_filter)
    y_wavelength = filter_wavelength(y_filter)
    z_wavelength = filter_wavelength(z_filter)

    # human eye wavelength
    b_wavelength = 0.465
    g_wavelength = 0.532
    r_wavelength = 0.630

    # wavelength ratio
    lambda_y_x = y_wavelength / x_wavelength
    lambda_z_y = z_wavelength / y_wavelength
    lambda_g_b = g_wavelength / b_wavelength
    lambda_r_g = r_wavelength / g_wavelength

    # Zero correction values
    x_zp = 1
    y_zp = 0.6534314
    z_zp = 0.561823628

    # Extract data
    x_data = x_image[0].data
    y_data = y_image[0].data
    z_data = z_image[0].data

    row_count = x_data.shape[0]
    col_count = x_data.shape[1]

    for row in range(row_count):
        for col in range(col_count):
            x_pixel = x_data[row][col]
            y_pixel = y_data[row][col]
            z_pixel = z_data[row][col]
            if x_pixel >= 0 and y_pixel >= 0 and z_pixel >= 0:
                x_pixel = \
                    y_pixel * 10 ** \
                    ((log10(x_pixel / y_pixel) - (x_zp - y_zp) / 2.5) * lambda_g_b / lambda_y_x)
                z_pixel = \
                    y_pixel * 10 ** \
                    ((log10(z_pixel / y_pixel) - (z_zp - y_zp) / 2.5) * lambda_r_g / lambda_z_y)

            x_data[row][col] = x_pixel
            y_data[row][col] = y_pixel
            z_data[row][col] = z_pixel

    # Apply new data
    x_image[0].data = x_data
    y_image[0].data = y_data
    z_image[0].data = z_data

    return [z_image, y_image, x_image]
