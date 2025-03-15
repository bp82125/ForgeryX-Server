import cv2
import numpy as np

DISPLAY_MULTIPLIER = 10


def get_noise_residue(original, filtered):
    noise = cv2.absdiff(original, filtered)
    return np.clip(noise * DISPLAY_MULTIPLIER, 0, 255).astype(np.uint8)


def median(image_path, kernel_size=3):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image at path {image_path} could not be loaded.")

    median_filtered = cv2.medianBlur(image, kernel_size)
    noise_residue = get_noise_residue(image, median_filtered)
    display_image = noise_residue if len(
        noise_residue.shape) == 2 else cv2.cvtColor(noise_residue, cv2.COLOR_BGR2RGB)
    return display_image
