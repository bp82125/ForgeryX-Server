import asyncio
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse
import os
import uuid

import orjson

from app.services.get_example_outputs import get_example_outputs
from app.services.process_images import process_image
from app.core.config import settings
from app.services.sse_response import SSE_Error_Response, SSE_Response
from app.services.utils import resize_image, save_uploaded_file

router = APIRouter()


@router.get("/examples/{uuid}")
@router.get("/examples/{uuid}/")
async def get_example_stream(uuid: str):
    result_json_path = os.path.join(
        settings.EXAMPLE_DIR, uuid, settings.RESULT_FILE)

    return StreamingResponse(get_example_outputs(result_json_path), media_type="text/event-stream")


@router.post("/upload")
@router.post("/upload/")
async def process_image_stream(file: UploadFile = File(...)):
    strUuid = str(uuid.uuid4())
    file_dir = os.path.join(settings.OUTPUT_DIR, strUuid)
    file_location = save_uploaded_file(file, file_dir)

    if not file_location:
        return StreamingResponse(iter([SSE_Error_Response("File upload failed").to_sse()]), media_type="text/event-stream")

    image = resize_image(file_location, max_dimension=2000)

    if image is None:
        return StreamingResponse(iter([SSE_Error_Response("Invalid image file").to_sse()]), media_type="text/event-stream")

    async def event_generator():
        yield SSE_Response(status="starting", message="File received", output_path=file_location).to_sse()

        try:
            async for result in process_image(file_location, file_dir):
                yield result
        except Exception as e:
            yield SSE_Error_Response(f"Processing error: {str(e)}").to_sse()

        yield SSE_Response(status="finished", message="Processing complete", output_path=file_location).to_sse()

    return StreamingResponse(event_generator(), media_type="text/event-stream")
