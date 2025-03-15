import gc
from photoholmes.methods.focal import Focal, focal_preprocessing
from photoholmes.utils.image import read_image

from app.core.config import settings

import torch

weight_dir = f"{settings.WEIGHT_DIR}/focal"
path_to_weights = {"ViT": f"{weight_dir}/VIT_weights.pth",
                   "HRNet": f"{weight_dir}/HRNET_weights.pth"}

FocalModel = Focal(
    weights=path_to_weights,
)

device = "cuda" if torch.cuda.is_available() else "cpu"
FocalModel.to_device(device)
FocalModel.eval()


def focal(image_path):
    image = read_image(image_path)
    image_data = {"image": image}

    model_input = focal_preprocessing(**image_data)

    output = FocalModel.predict(**model_input)

    binary_output = output.cpu()

    normalized_output = (binary_output - binary_output.min()) / \
        (binary_output.max() - binary_output.min())

    return (normalized_output * 255).byte().numpy()
