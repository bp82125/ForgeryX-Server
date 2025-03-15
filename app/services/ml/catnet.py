import gc
import torch
import cv2
import numpy as np

from photoholmes.methods.catnet import CatNet, catnet_preprocessing
from photoholmes.utils.image import read_jpeg_data, create_heatmap
from app.core.config import settings
from app.services.utils import ensure_jpeg

weight_path = f"{settings.WEIGHT_DIR}/catnet/weights.pth"
device = "cuda" if torch.cuda.is_available() else "cpu"
arch_config = "pretrained"

weights = torch.load(weight_path, weights_only=False)

CatNetModel = CatNet(
    arch_config=arch_config,
    weights=weights,
)

CatNetModel.to_device(device)
CatNetModel.eval()

def catnet(image_path):
    image = ensure_jpeg(cv2.imread(image_path))
    
    dct, qtables = read_jpeg_data(image_path)

    image_data = {"image": image, "dct_coefficients": dct, "qtables": qtables}
    input = catnet_preprocessing(**image_data)

    with torch.no_grad():
        output = CatNetModel.predict(**input)
    
    binary_image = np.array(output[0].cpu().numpy(), dtype=np.float32)
    
    heatmap = create_heatmap(binary_image)
    
    return heatmap
