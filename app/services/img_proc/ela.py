import cv2
import numpy as np

from photoholmes.methods.ela import ELA, ela_preprocessing
from photoholmes.utils.image import read_image

ELAModel = ELA()


def ela(image_path):
    image = read_image(image_path)
    image_data = {"image": image}

    image_input = ela_preprocessing(**image_data)

    output = ELAModel.predict(**image_input)

    return output
