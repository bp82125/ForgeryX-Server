import os
import cv2
import asyncio
from app.services.img_proc.wavelet import high_frequency_noise_wavelet
from app.services.img_proc.median import median
from app.services.img_proc.ghost import ghost
from app.services.img_proc.ela import ela
from app.services.img_proc.blocking import extract_blocking_artifact


async def process_image(image, file_dir):
    image_tasks = [
        ("wavelet_noise_map.png", high_frequency_noise_wavelet),
        ("median_image.png", median),
        ("ela_image.png", ela),
        ("blocking_artifact_map.png", extract_blocking_artifact),
    ]

    for filename, process_func in image_tasks:
        output_path = os.path.join(file_dir, filename)
        processed_img = process_func(image)
        cv2.imwrite(output_path, processed_img)
        yield output_path
        await asyncio.sleep(0.1)

    for quality, ghost_map in ghost(image):
        output_path = os.path.join(file_dir, f"ghost_map_{quality}.png")
        cv2.imwrite(output_path, ghost_map)
        yield output_path
        await asyncio.sleep(0.1)
