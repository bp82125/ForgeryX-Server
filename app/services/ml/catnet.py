import torch
import cv2
import numpy as np

from photoholmes.methods.catnet import CatNet, catnet_preprocessing
from photoholmes.utils.image import read_jpeg_data

weight_path = "/home/nhat82125/photoholmes/weights/catnet/weights.pth"
device = "cuda" if torch.cuda.is_available() else "cpu"
arch_config = "pretrained"

weights = torch.load(weight_path, weights_only=False)

CatNetModel = CatNet(
    arch_config=arch_config,
    weights=weights,
)

CatNetModel.to_device(device)
CatNetModel.eval()

def prepare_image(image):
    return torch.from_numpy(cv2.cvtColor(image, cv2.COLOR_BGR2RGB).transpose(2, 0, 1))


def ensure_jpeg(image):
    encode_param = [cv2.IMWRITE_JPEG_QUALITY, 95]

    success, encoded_img = cv2.imencode(".jpg", image, encode_param)
    if success:
        decoded_img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
        if decoded_img is not None:
            return prepare_image(decoded_img)

    return cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)

def catnet(image_path):
    image = ensure_jpeg(cv2.imread(image_path))
    
    dct, qtables = read_jpeg_data(image_path)

    image_data = {"image": image, "dct_coefficients": dct, "qtables": qtables}
    input = catnet_preprocessing(**image_data)


    with torch.no_grad():
        output = CatNetModel.predict(**input)
    
    binary_image = np.array(output[0].cpu().numpy(), dtype=np.float32)
    
    normalized_image = (binary_image - np.min(binary_image)) / \
        (np.max(binary_image) - np.min(binary_image))
    heatmap = cv2.applyColorMap(
        np.uint8(255 * normalized_image), cv2.COLORMAP_JET)
    
    return heatmap
