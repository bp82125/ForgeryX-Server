from app.services.img_proc.wavelet import high_frequency_noise_wavelet
from app.services.img_proc.ela import ela
from app.services.img_proc.blocking import blocking
from app.services.ml.mesorch import mesorch
from app.services.ml.trufor import trufor
from app.services.ml.catnet import catnet
from app.services.img_proc.dq import dq
from app.services.ml.exif_as_language import exif_as_language


METHODS = {
    "trufor": {
        "filename": "trufor.png",
        "function": trufor,
        "name": "TruFor",
        "result_type": "score",
        "method_type": "deep_learning",
    },
    "wavelet": {
        "filename": "wavelet.png",
        "function": high_frequency_noise_wavelet,
        "name": "High frequency noise (WAVELET)",
        "method_type": "image_processing",
        "result_type": "standard",
    },
    "exif_as_language": {
        "filename": 'exif_as_language.png',
        "name": "EXIF as Language",
        "function": exif_as_language,
        "method_type": "deep_learning",
        "result_type": "score",
    },
    "ela": {
        "filename": "ela.png",
        "function": ela,
        "name": "Error Level Analysis (ELA)",
        "method_type": "image_processing",
        "result_type": "standard",
    },
    "blocking": {
        "filename": "blocking.png",
        "function": blocking,
        "name": "JPEG blocking artifact inconsistencies (BLOCK)",
        "method_type": "image_processing",
        "result_type": "standard",
    },
    "catnet": {
        "filename": 'catnet.png',
        "function": catnet,
        "name": "CAT-Net",
        "method_type": "deep_learning",
        "result_type": "standard",
    },
    "dq": {
        "filename": 'dq.png',
        "name": "DQ",
        "function": dq,
        "method_type": "image_processing",
        "result_type": "standard",
    },
    "mesorch": {
        "filename": 'mesorch.png',
        "name": "Mesorch",
        "function": mesorch,
        "method_type": "deep_learning",
        "result_type": "standard",
    }
}
