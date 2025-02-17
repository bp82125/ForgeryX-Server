import cv2
import numpy as np

DISPLAY_MULTIPLIER = 10
SC_WIDTH = 600
SC_HEIGHT = 600


def get_noise_residue(original, filtered):
    noise = cv2.absdiff(original, filtered)
    return np.clip(noise * DISPLAY_MULTIPLIER, 0, 255).astype(np.uint8)


def scale_image(image, width, height):
    h, w = image.shape[:2]
    if h > w and h > height:
        width = (height * w) // h
    elif w > h and w > width:
        height = (width * h) // w
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_NEAREST)


def median(image, kernel_size=3):
    median_filtered = cv2.medianBlur(image, kernel_size)
    noise_residue = get_noise_residue(image, median_filtered)
    display_image = noise_residue if len(
        noise_residue.shape) == 2 else cv2.cvtColor(noise_residue, cv2.COLOR_BGR2RGB)
    return scale_image(display_image, SC_WIDTH, SC_HEIGHT)
