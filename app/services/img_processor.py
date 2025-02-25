import os
import cv2
import asyncio
from app.services.methods import IMAGE_PROCESSING_METHODS


async def process_image(image_path, file_dir):
    if not os.path.exists(image_path):
        raise ValueError(f"Image at path {image_path} does not exist.")

    for method_id, details in IMAGE_PROCESSING_METHODS.items():
        if method_id == "ghost":
            ghost_results = await asyncio.to_thread(details["function"], image_path)
            for quality, ghost_map in ghost_results:
                ghost_method_id = f"ghost_{quality}"
                output_path = os.path.join(
                    file_dir, f"ghost_map_{quality}.png")

                await asyncio.to_thread(cv2.imwrite, output_path, ghost_map)

                yield {
                    "method_id": ghost_method_id,
                    "method_name": f"{details['name']} - Quality {quality}",
                    "output_path": output_path,
                    "type": details["type"]
                }

        elif method_id in ["trufor", "exif_as_language", "psccnet"]:
            output_path = os.path.join(file_dir, details["filename"])
            processed_img, score = await asyncio.to_thread(details["function"], image_path)

            await asyncio.to_thread(cv2.imwrite, output_path, processed_img)

            yield {
                "method_id": method_id,
                "method_name": details["name"],
                "output_path": output_path,
                "score": score,
                "type": details["type"]
            }

        else:
            output_path = os.path.join(file_dir, details["filename"])
            processed_img = await asyncio.to_thread(details["function"], image_path)

            await asyncio.to_thread(cv2.imwrite, output_path, processed_img)

            yield {
                "method_id": method_id,
                "method_name": details["name"],
                "output_path": output_path,
                "type": details["type"]
            }
