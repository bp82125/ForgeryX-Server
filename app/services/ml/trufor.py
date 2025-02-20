import gc  # Garbage collection
import torch
import cv2
import numpy as np
import gc

from photoholmes.methods.trufor import TruFor, trufor_preprocessing

weight_path = "/home/nhat82125/ForgeryX-Server/weights/trufor/trufor.pth.tar"
device = "cuda" if torch.cuda.is_available() else "cpu"

weights = torch.load(weight_path, weights_only=False)
truForModel = TruFor(weights=weights)
truForModel.to_device(device)
truForModel.eval()


def prepare_image(image):
    return torch.from_numpy(cv2.cvtColor(image, cv2.COLOR_BGR2RGB).transpose(2, 0, 1))


def trufor(image):
    tp_image = prepare_image(image).to(device)
    model_input = trufor_preprocessing(image=tp_image)

    with torch.no_grad():
        heatmap, confidence, detection, _ = truForModel.predict(**model_input)

    cool_heatmap = (heatmap * confidence).cpu().numpy()
    score = detection.item()

    jet_heatmap = cv2.applyColorMap(
        np.uint8(255 * cool_heatmap), cv2.COLORMAP_JET)

    del tp_image, model_input, heatmap, confidence, detection
    torch.cuda.empty_cache()
    gc.collect()

    return jet_heatmap, score
