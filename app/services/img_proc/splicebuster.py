
import cv2
import numpy as np
import torch

from photoholmes.methods.splicebuster import Splicebuster, splicebuster_preprocessing

SpliceBusterMethod = Splicebuster()

def prepare_image(image):
    return torch.from_numpy(cv2.cvtColor(image, cv2.COLOR_BGR2RGB).transpose(2, 0, 1))


def splicebuster(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image at path {image_path} could not be loaded.")

    image_data = {"image": image}

    input_image = splicebuster_preprocessing(**image_data)
    output = SpliceBusterMethod.predict(**input_image)

    binary_image = np.array(output, dtype=np.float32)
    normalized_image = cv2.normalize(
        binary_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    heatmap = cv2.applyColorMap(
        normalized_image, cv2.COLORMAP_JET)

    return heatmap
