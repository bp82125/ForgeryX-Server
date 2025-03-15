import gc
from photoholmes.utils.image import read_image, create_heatmap
from photoholmes.methods.exif_as_language import exif_as_language_preprocessing, EXIFAsLanguage

from app.core.config import settings

import torch


arch_config = "pretrained"
path_to_weights = f"{settings.WEIGHT_DIR}/exif_as_language/weights.pth"

ExifModel = EXIFAsLanguage(
    arch_config=arch_config,
    weights=path_to_weights,
)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
ExifModel.to_device(device)


def exif_as_language(image_path):
    image = read_image(image_path)
    model_input = exif_as_language_preprocessing(image=image)

    with torch.no_grad():
        output = ExifModel.predict(**model_input)

    consistency_map, _, score, _, _ = output

    heatmap = create_heatmap(consistency_map)

    return heatmap, score
