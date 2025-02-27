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

METHODS = {
    "trufor": {
        "filename": "trufor.png",
        "function": trufor,
        "name": "TruFor",
        "result_type": "score",
        "method_type": "deep_learning",
    },
    "wavelet": {
        "filename": "wavelet_noise_map.png",
        "function": high_frequency_noise_wavelet,
        "name": "High frequency noise (WAVELET)",
        "method_type": "image_processing",
        "result_type": "standard",
    },
    "exif_as_language": {
        "filename": 'exif.png',
        "name": "EXIF as Language",
        "function": exif_as_language,
        "method_type": "deep_learning",
        "result_type": "score",
    },
    "median": {
        "filename": "median_image.png",
        "function": median,
        "name": "Median filtering noise residue (MEDIAN)",
        "method_type": "image_processing",
        "result_type": "standard",
    },
    "psccnet": {
        "filename": 'psccnet.png',
        "name": "PSCC-Net",
        "function": psccnet,
        "method_type": "deep_learning",
        "result_type": "score",
    },
    "ela": {
        "filename": "ela_image.png",
        "function": ela,
        "name": "Error Level Analysis (ELA)",
        "method_type": "image_processing",
        "result_type": "standard",
    },
    "blocking": {
        "filename": "blocking_artifact_map.png",
        "function": blocking,
        "name": "JPEG blocking artifact inconsistencies (BLOCK)",
        "method_type": "image_processing",
        "result_type": "standard",

    },
    "splicebuster": {
        "filename": 'splicebuster.png',
        "function": splicebuster,
        "name": "SpliceBuster",
        "method_type": "image_processing",
        "result_type": "standard",
    },
    "catnet": {
        "filename": 'catnet.png',
        "function": catnet,
        "name": "CatNet",
        "method_type": "deep_learning",
        "result_type": "standard",
    },
    "ghost": {
        "filename": 'ghost.png',
        "name": "JPEG Ghosts (GHOST)",
        "function": ghost,
        "method_type": "image_processing",
        "result_type": "multi_output",
    },
    "dq": {
        "filename": 'dq.png',
        "name": "DQ",
        "function": dq,
        "method_type": "image_processing",
        "result_type": "standard",
    },
    "focal": {
        "filename": 'focal.png',
        "name": "Focal",
        "function": focal,
        "method_type": "deep_learning",
        "result_type": "standard",
    },
}
