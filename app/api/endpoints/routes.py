from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse
import os
import uuid
import shutil
import cv2


from app.services.img_processor import process_image
from app.core.config import settings

router = APIRouter()


@router.post("/upload")
@router.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    strUuid = str(uuid.uuid4())
    file_dir = f"{settings.OUTPUT_DIR}/{strUuid}"
    file_location = os.path.join(
        file_dir, f"{strUuid}{os.path.splitext(file.filename)[1]}")
    os.makedirs(file_dir, exist_ok=True)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image = cv2.imread(file_location)

    max_dimension = 2000
    height, width = image.shape[:2]
    if height > max_dimension or width > max_dimension:
        scaling_factor = max_dimension / float(max(height, width))
        new_size = (int(width * scaling_factor), int(height * scaling_factor))
        image = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)
        cv2.imwrite(file_location, image)

    async def event_generator():
        async for output_path in process_image(file_location, file_dir):
            yield f"data: {output_path}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
