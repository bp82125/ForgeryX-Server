import torch
import cv2


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
