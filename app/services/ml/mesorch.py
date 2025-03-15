
import gc
import torch

from app.core.config import settings

from photoholmes.utils.image import read_image, create_heatmap
from photoholmes.methods.mesorch import Mesorch, mesorch_preprocessing


checkpoint_path = f'{settings.WEIGHT_DIR}/mesorch/mesorch.pth'
device = 'cuda' if torch.cuda.is_available() else 'cpu'

MesorchModel = Mesorch(seg_pretrain_path=None, conv_pretrain=False)

checkpoint = torch.load(
    checkpoint_path, map_location=device, weights_only=False)

MesorchModel.load_state_dict(checkpoint['model'])
MesorchModel.to_device(device)
MesorchModel.eval()


def mesorch(image_path):
    tp_image = read_image(image_path)
    mesorch_input = mesorch_preprocessing(image=tp_image)

    mesorch_output = MesorchModel.predict(**mesorch_input)

    binary_mask = mesorch_output.cpu().numpy()

    heatmap = create_heatmap(binary_mask)

    return heatmap
