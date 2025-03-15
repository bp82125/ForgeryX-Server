import gc
from photoholmes.methods.psccnet import PSCCNet, psccnet_preprocessing
from photoholmes.utils.image import read_image

from app.core.config import settings

import torch
import numpy as np
import cv2

device = "cuda"
arch_config = "pretrained"
weight_dir = f"{settings.WEIGHT_DIR}/psccnet"

path_to_weights = {
    "FENet": f"{weight_dir}/FENet.pth",
    "SegNet": f"{weight_dir}/SegNet.pth",
    "ClsNet": f"{weight_dir}/ClsNet.pth",
}

PSCCNetMethod = PSCCNet(
    arch_config=arch_config,
    weights=path_to_weights,
)

PSCCNetMethod.to_device(device)
PSCCNetMethod.eval()


def psccnet(image_path):
    image = read_image(image_path)
    image_data = {"image": image}

    method_input = psccnet_preprocessing(**image_data)

    with torch.no_grad():
        output = PSCCNetMethod.predict(**method_input)

    binary_map = output[0].cpu().numpy()
    score = output[1].cpu().numpy()[0]

    normalized_map = (binary_map - np.min(binary_map)) / \
        (np.max(binary_map) - np.min(binary_map))

    heatmap = cv2.applyColorMap(
        np.uint8(255 * normalized_map), cv2.COLORMAP_JET)

    return heatmap, score
