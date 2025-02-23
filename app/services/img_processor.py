import os
import cv2
import asyncio
from app.core.config import settings


async def process_image(image_path, file_dir):
    if not os.path.exists(image_path):
        raise ValueError(f"Image at path {image_path} does not exist.")

    for method_id, details in settings.IMAGE_PROCESSING_METHODS.items():
        if method_id == "ghost":
            for quality, ghost_map in details["function"](image_path):
                ghost_method_id = f"ghost_{quality}"
                output_path = os.path.join(
                    file_dir, f"ghost_map_{quality}.png")
                cv2.imwrite(output_path, ghost_map)
                yield {
                    "method_id": ghost_method_id,
                    "method_name": f"{details['name']} - Quality {quality}",
                    "output_path": output_path,
                    "type": details["type"]
                }
                await asyncio.sleep(0.1)

        elif method_id in ["trufor", "exif_as_language"]:
            output_path = os.path.join(file_dir, details["filename"])
            processed_img, score = details["function"](image_path)
            cv2.imwrite(output_path, processed_img)
            yield {
                "method_id": method_id,
                "method_name": details["name"],
                "output_path": output_path,
                "score": score,
                "type": details["type"]
            }
            await asyncio.sleep(0.1)
        else:
            output_path = os.path.join(file_dir, details["filename"])
            processed_img = details["function"](image_path)
            cv2.imwrite(output_path, processed_img)
            yield {
                "method_id": method_id,
                "method_name": details["name"],
                "output_path": output_path,
                "type": details["type"]
            }
            await asyncio.sleep(0.1)
