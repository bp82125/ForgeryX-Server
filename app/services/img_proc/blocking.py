import cv2
import numpy as np

from photoholmes.methods.blocking import BlockingArtifacts, blocking_preprocessing
from photoholmes.utils.image import read_image, create_heatmap

BlockingModel = BlockingArtifacts()


def blocking(image_path):
    image = read_image(image_path)
    image_data = {"image": image}

    image_input = blocking_preprocessing(**image_data)

    output = BlockingModel.predict(**image_input)
    
    heatmap = create_heatmap(output)

    return heatmap
