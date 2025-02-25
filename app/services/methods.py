from app.services.img_proc.wavelet import high_frequency_noise_wavelet
from app.services.img_proc.median import median
from app.services.img_proc.ghost import ghost
from app.services.img_proc.ela import ela
from app.services.img_proc.blocking import blocking
from app.services.ml.trufor import trufor
from app.services.img_proc.splicebuster import splicebuster
from app.services.ml.catnet import catnet
from app.services.img_proc.dq import dq
from app.services.ml.exif_as_language import exif_as_language
from app.services.ml.focal import focal
from app.services.ml.psccnet import psccnet

IMAGE_PROCESSING_METHODS = {
    "trufor": {
        "filename": "trufor.png",
        "function": trufor,
        "name": "TruFor",
        "type": "deep_learning"
    },
    "wavelet": {
        "filename": "wavelet_noise_map.png",
        "function": high_frequency_noise_wavelet,
        "name": "High frequency noise (WAVELET)",
        "type": "image_processing"
    },
    "exif_as_language": {
        "filename": 'exif.png',
        "name": "EXIF as Language",
        "type": "deep_learning",
        "function": exif_as_language
    },
    "median": {
        "filename": "median_image.png",
        "function": median,
        "name": "Median filtering noise residue (MEDIAN)",
        "type": "image_processing"
    },
    "psccnet": {
        "filename": 'psccnet.png',
        "name": "PSCC-Net",
        "type": "deep_learning",
        "function": psccnet
    },
    "ela": {
        "filename": "ela_image.png",
        "function": ela,
        "name": "Error Level Analysis (ELA)",
        "type": "image_processing"
    },
    "blocking": {
        "filename": "blocking_artifact_map.png",
        "function": blocking,
        "name": "JPEG blocking artifact inconsistencies (BLOCK)",
        "type": "image_processing"
    },
    "splicebuster": {
        "filename": 'splicebuster.png',
        "function": splicebuster,
        "name": "SpliceBuster",
        "type": "image_processing",
    },
    "catnet": {
        "filename": 'catnet.png',
        "function": catnet,
        "name": "CatNet",
        "type": "deep_learning"
    },
    "ghost": {
        "name": "JPEG Ghosts (GHOST)",
        "function": ghost,
        "type": "image_processing"
    },

    "dq": {
        "filename": 'dq.png',
        "name": "DQ",
        "type": "image_processing",
        "function": dq
    },
    "focal": {
        "filename": 'focal.png',
        "name": "Focal",
        "type": "deep_learning",
        "function": focal
    },
}
