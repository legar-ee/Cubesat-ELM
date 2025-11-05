import numpy as np


def dark_bright(image):  # Compute darkest/brightest radiances and their pixels in each band
    row, col, band = image.shape

    darkest_rads = np.min(image, axis=(0, 1))
    brightest_rads = np.max(image, axis=(0, 1))
    
    darkest_pixels = np.argmin(image, axis=(0, 1))
    brightest_pixels = np.argmax(image, axis=(0, 1))
    darkest_row, darkest_col = np.unravel_index(darkest_pixels, (row, col))
    brightest_row, brightest_col = np.unravel_index(brightest_pixels, (row, col))
    darkest_pixels = list(zip(darkest_row, darkest_col))
    brightest_pixels = list(zip(brightest_row, brightest_col))

    # Rads are in an 1D array with 'band' number of elements, and pixels are a list of 'band' number of (row, col) tuples
    return (darkest_rads, darkest_pixels, brightest_rads, brightest_pixels)


def elm(image, dark_bright_data):
    


