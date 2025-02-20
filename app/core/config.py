from app.services.img_proc.wavelet import high_frequency_noise_wavelet
from app.services.img_proc.median import median
from app.services.img_proc.ghost import ghost
from app.services.img_proc.ela import ela
from app.services.img_proc.blocking import extract_blocking_artifact
from app.services.ml.trufor import trufor


class Settings:
    PROJECT_NAME: str = "ForgeryX-Server"
    API_V1_STR: str = "/api/v1"
    OUTPUT_DIR: str = "output"

    IMAGE_PROCESSING_METHODS = {
        "wavelet": {
            "filename": "wavelet_noise_map.png",
            "function": high_frequency_noise_wavelet,
            "name": "High frequency noise (WAVELET)",
            "type": "image_processing"
        },
        "median": {
            "filename": "median_image.png",
            "function": median,
            "name": "Median filtering noise residue (MEDIAN)",
            "type": "image_processing"
        },
        "ela": {
            "filename": "ela_image.png",
            "function": ela,
            "name": "Error Level Analysis (ELA)",
            "type": "image_processing"
        },
        "blocking": {
            "filename": "blocking_artifact_map.png",
            "function": extract_blocking_artifact,
            "name": "JPEG blocking artifact inconsistencies (BLOCK)",
            "type": "image_processing"
        },
        "ghost": {
            "name": "JPEG Ghosts (GHOST)",
            "function": ghost,
            "type": "image_processing"
        },
        "trufor": {
            "filename": "trufor.png",
            "function": trufor,
            "name": "TruFor",
            "type": "deep_learning"
        }
    }


settings = Settings()
