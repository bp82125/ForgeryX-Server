import os
import cv2
import asyncio

from photoholmes.utils.image import save_image

from app.services.methods import METHODS
from app.services.sse_response import SSE_Response, SSE_Error_Response
from app.services.utils import save_to_json
from app.core.config import settings


async def process_multi_output_method(method_id, details, image_path, file_dir):
    multi_output_results = await asyncio.to_thread(
        details["function"],
        image_path,
        output_dir=file_dir,
        filename=details["filename"],
    )

    for identifier, output_path in multi_output_results:
        yield SSE_Response(
            status="processing",
            message=f"Method {details['name']} applied with identifier {identifier}",
            method_id=method_id,
            method_name=f"{details['name']} - {identifier}",
            output_path=output_path,
            result_type="multi_output",
            method_type=details["method_type"],
        )


async def process_scored_method(method_id, details, image_path, file_dir):
    output_path = os.path.join(file_dir, details["filename"])
    processed_img, score = await asyncio.to_thread(details["function"], image_path)
    await asyncio.to_thread(save_image, output_path, processed_img)

    return SSE_Response(
        status="processing",
        message=f"Method {details['name']} applied with score {score}",
        method_id=method_id,
        method_name=details["name"],
        output_path=output_path,
        result_type="score",
        method_type=details["method_type"],
        score=score
    )


async def process_standard_method(method_id, details, image_path, file_dir):
    output_path = os.path.join(file_dir, details["filename"])
    processed_img = await asyncio.to_thread(details["function"], image_path)
    await asyncio.to_thread(save_image, output_path, processed_img)

    return SSE_Response(
        status="processing",
        message=f"Method {details['name']} applied successfully",
        method_id=method_id,
        method_name=details["name"],
        output_path=output_path,
        result_type="standard",
        method_type=details["method_type"],
    )


async def process_image(image_path, file_dir):
    if not os.path.exists(image_path):
        yield SSE_Error_Response(f"Image at path {image_path} does not exist.").to_sse()
        return

    try:
        for method_id, details in METHODS.items():
            if details["result_type"] == "multi_output":
                async for result in process_multi_output_method(method_id, details, image_path, file_dir):
                    save_to_json(result.to_json(), file_dir,
                                 settings.RESULT_FILE)
                    yield result.to_sse()
                    await asyncio.sleep(0.3)
            elif details["result_type"] == "score":
                result = await process_scored_method(method_id, details, image_path, file_dir)
                save_to_json(result.to_json(), file_dir, settings.RESULT_FILE)
                yield result.to_sse()
                await asyncio.sleep(0.3)
            else:
                result = await process_standard_method(method_id, details, image_path, file_dir)
                save_to_json(result.to_json(), file_dir, settings.RESULT_FILE)
                yield result.to_sse()
                await asyncio.sleep(0.3)

    except Exception as e:
        yield SSE_Error_Response(f"Unexpected processing error: {str(e)}", 503).to_sse()
