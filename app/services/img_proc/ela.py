import cv2
import numpy as np

QUALITY = 75
DISPLAY_MULTIPLIER = 20
SC_WIDTH = 600
SC_HEIGHT = 600


def recompress_image(image, quality):
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    result, encimg = cv2.imencode('.jpg', image, encode_param)
    if not result:
        raise ValueError("Could not recompress the image.")
    recompressed_image = cv2.imdecode(encimg, 1)
    return recompressed_image


def get_image_difference(image1, image2):
    diff = image1.astype(np.float32) - image2.astype(np.float32)
    diff = diff ** 2
    return diff


def scale_image(image, width, height):
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_NEAREST)


def ela(image, quality):
    recompressed_image = recompress_image(image, quality)
    image_difference = get_image_difference(image, recompressed_image)

    ela_min = np.min(image_difference)
    ela_max = np.max(image_difference)

    int_difference = np.sqrt(image_difference) * DISPLAY_MULTIPLIER
    int_difference = np.clip(int_difference, ela_min, ela_max).astype(np.uint8)
