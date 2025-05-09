import exiftool
from .helpers import convert_metadata_value, convert_to_actual_focal_length
import os
import imghdr


def get_metadata(image_path):
    metadata = {}
    
    if not image_path:
        raise ValueError("Image path is not provided")

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found at: {image_path}")

    with exiftool.ExifTool() as et:
        exif_data = et.execute_json(image_path)

    if exif_data and isinstance(exif_data, list):
        metadata = exif_data[0]

    metadata = {key.split(":")[-1].strip(): value
                for key, value in metadata.items()}

    converted_metadata = {key: convert_metadata_value(key,
                                                      value) for key, value in metadata.items()}

    if 'FocalLength35efl' in converted_metadata and 'ScaleFactor35efl' in converted_metadata:
        converted_metadata['FocalLength'] = convert_to_actual_focal_length(
            converted_metadata['FocalLength35efl'], converted_metadata['ScaleFactor35efl'])

    return converted_metadata
