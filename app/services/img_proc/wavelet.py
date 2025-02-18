import cv2
import numpy as np
import pywt


def estimate_noise_std(block):
    # Median Absolute Deviation (MAD)
    MAD_CONSTANT = 0.6745
    return np.median(np.abs(block - np.median(block))) / MAD_CONSTANT


def process_channel(channel, block_size=32):
    coeffs2 = pywt.dwt2(channel, 'db8')
    _, (_, _, HH) = coeffs2

    height, width = HH.shape
    noise_map = np.zeros((height, width))

    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            block = HH[i:i+block_size, j:j+block_size]
            if block.shape == (block_size, block_size):
                noise_map[i:i+block_size, j:j +
                          block_size] = estimate_noise_std(block)

    return noise_map


def high_frequency_noise_wavelet(image, block_size=8, threshold=1.0):
    ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    Y, Cr, Cb = cv2.split(ycrcb)

    noise_Y = process_channel(Y, block_size)
    noise_Cr = process_channel(Cr, block_size)
    noise_Cb = process_channel(Cb, block_size)

    combined_noise_map = np.maximum.reduce([noise_Y, noise_Cr, noise_Cb])
    combined_noise_map = cv2.normalize(
        combined_noise_map, None, 0, 255, cv2.NORM_MINMAX)

    heatmap = cv2.applyColorMap(
        combined_noise_map.astype(np.uint8), cv2.COLORMAP_JET)

    # segmented_map = np.zeros_like(combined_noise_map)
    # mean_noise = np.mean(combined_noise_map)
    # segmented_map[combined_noise_map > mean_noise +
    #               threshold] = 255

    return heatmap
