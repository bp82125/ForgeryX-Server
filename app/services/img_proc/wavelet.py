import cv2
import numpy as np

from photoholmes.methods.wavelet import Wavelet, wavelet_preprocessing
from photoholmes.utils.image import read_image, create_heatmap

WaveletModel = Wavelet()


def high_frequency_noise_wavelet(image_path):
    image = read_image(image_path)
    image_data = {"image": image}

    image_input = wavelet_preprocessing(**image_data)

    output = WaveletModel.predict(**image_input)

    heatmap = create_heatmap(output)

    return heatmap
