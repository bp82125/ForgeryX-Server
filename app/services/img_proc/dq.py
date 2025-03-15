import cv2
import numpy as np

from photoholmes.methods.dq import DQ, dq_preprocessing
from photoholmes.utils.image import read_jpeg_data, create_heatmap

from app.services.utils import ensure_jpeg

DQ_Method = DQ()


def dq(image_path):
    image = ensure_jpeg(cv2.imread(image_path))
    dct, _ = read_jpeg_data(image_path)

    image_data = {"image": image, "dct_coefficients": dct}
    image_input = dq_preprocessing(**image_data)

    output = DQ_Method.predict(**image_input)

    heatmap = create_heatmap(output)

    return heatmap
