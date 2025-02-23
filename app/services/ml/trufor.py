import gc  # Garbage collection
import torch
import cv2
import numpy as np
import gc

from photoholmes.methods.trufor import TruFor, trufor_preprocessing
from photoholmes.utils.image import read_image

weight_path = "/home/nhat82125/photoholmes/weights/trufor/trufor.pth.tar"
device = "cuda" if torch.cuda.is_available() else "cpu"

weights = torch.load(weight_path, weights_only=False)
TruForModel = TruFor(weights=weights)
TruForModel.to_device(device)
TruForModel.eval()


def trufor(image_path):
    tp_image = read_image(image_path).to(device)
    model_input = trufor_preprocessing(image=tp_image)

    with torch.no_grad():
        heatmap, confidence, detection, _ = TruForModel.predict(**model_input)

    cool_heatmap = (heatmap * confidence).cpu().numpy()
    score = detection.item()

    jet_heatmap = cv2.applyColorMap(
        np.uint8(255 * cool_heatmap), cv2.COLORMAP_JET)

    del tp_image, model_input, heatmap, confidence, detection
    torch.cuda.empty_cache()
    gc.collect()

    return jet_heatmap, score
