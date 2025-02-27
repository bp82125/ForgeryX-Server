import cv2
import numpy as np

from photoholmes.methods.dq import DQ, dq_preprocessing
from photoholmes.utils.image import read_jpeg_data

from app.services.utils import ensure_jpeg

DQ_Method = DQ()

def dq(image_path):
    image = ensure_jpeg(cv2.imread(image_path))
    dct, qtables = read_jpeg_data(image_path)
    
    image_data = {"image": image, "dct_coefficients": dct}
    input = dq_preprocessing(**image_data)
    
    output = DQ_Method.predict(**input)
    
    binary_image = np.array(output, dtype=np.float32)

    normalized_image = cv2.normalize(binary_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    heatmap = cv2.applyColorMap(normalized_image, cv2.COLORMAP_JET)
    
    return heatmap
