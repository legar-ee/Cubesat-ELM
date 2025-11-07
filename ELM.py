import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import linregress


def target_radiance(image, known_endmember): # Find the same-type (grass, cloud, etc) radiance values as the known endmembers
    # Argument: image = 3D array (row, col, band); known_endmember = 1D array for each type (grass/cloud/etc)

    row, col, band = image.shape

    # Find the radiance values in the image
    image_flat = image.reshape((row*col), band)
    known_endmember = known_endmember.reshape(1, band)
    match_value = cosine_similarity(image_flat, known_endmember).flatten()
    target_index = np.argmax(match_value)
    target_row, target_col = np.unravel_index(target_index, (row, col))

    return image[target_row, target_col] # Return an 1D array of each type with 'band' elements; will need to stack them all up later


def elm(image, target_radiance, known_endmember): # Compute ELM
    # Argument: image = 3D array (row, col, band); target_radiance = 2D array (number of radiance values, band); kn
    row, col, band = image.shape
    gain = np.zeros(band)
    offset = np.zeros(band)

    for i in range(band):
        slope, intercept, _, _, _ = linregress(target_radiance[:, i], known_endmember[:, i])

        gain[i] = slope
        offset[i] = intercept

    gain = gain[np.newaxis, np.newaxis, :]
    offset = offset[np.newaxis, np.newaxis, :]

    return image*gain + offset



