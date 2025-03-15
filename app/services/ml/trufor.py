import gc  # Garbage collection
import torch
import cv2
import numpy as np
import gc

from photoholmes.methods.trufor import TruFor, trufor_preprocessing
from photoholmes.utils.image import read_image, create_heatmap
from app.core.config import settings

weight_path = f"{settings.WEIGHT_DIR}/trufor/trufor.pth.tar"
device = "cuda" if torch.cuda.is_available() else "cpu"

TruForModel = TruFor(weights=weight_path)
TruForModel.to_device(device)
TruForModel.eval()


def trufor(image_path):
    tp_image = read_image(image_path).to(device)
    model_input = trufor_preprocessing(image=tp_image)

    heatmap, confidence, detection, _ = TruForModel.predict(**model_input)

    cool_heatmap = (heatmap * confidence).cpu().numpy()
    score = detection.item()

    result_heatmap = create_heatmap(cool_heatmap)

    return result_heatmap, score
