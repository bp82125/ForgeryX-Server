from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse
import os
import uuid
import shutil
import cv2
import asyncio

router = APIRouter()


@router.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    strUuid = str(uuid.uuid4())

    file_dir = f"processed_images/{strUuid}"
    file_location = f'{file_dir}/{file.filename}'

    os.makedirs(file_dir, exist_ok=True)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image = cv2.imread(file_location)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    processed_file_location = f'{file_dir}/processed_{file.filename}'
    cv2.imwrite(processed_file_location, gray_image)

    async def event_generator():
        await asyncio.sleep(1)
        yield f"data: {processed_file_location}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
