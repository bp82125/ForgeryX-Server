from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.endpoints.image import router as image_router
from app.core.config import settings
import uvicorn

app = FastAPI(title=settings.PROJECT_NAME)

app.mount("/processed_images",
          StaticFiles(directory="processed_images"), name="processed_images")

app.include_router(image_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
