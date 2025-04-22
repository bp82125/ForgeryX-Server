import os
import asyncio
from app.services.sse_response import SSE_Response
from app.services.utils import save_to_json
from app.services.metadata.get_metadata import get_metadata


async def process_metadata(image_path, file_dir):
    os.makedirs(file_dir, exist_ok=True)
    metadata = await asyncio.to_thread(get_metadata, image_path)

    metadata_response = SSE_Response(
        status="processing",
        message="Thông tin về EXIF metadata đã được trích xuất thành công",
        method_id="metadata",
        method_name="Metadata Extraction",
        result_type="metadata",
        method_type="metadata",
        metadata=metadata
    )

    save_to_json(metadata_response.to_json(), file_dir, "results.json")
    return metadata_response
