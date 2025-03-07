import exiftool
import orjson
from .helpers import convert_metadata_value


def get_metadata(image_path):
    metadata = {}

    with exiftool.ExifTool() as et:
        exif_data = et.execute_json(image_path)

    if exif_data and isinstance(exif_data, list):
        metadata = exif_data[0]

    metadata = {
        key.split(":")[-1].strip(): convert_metadata_value(key, value)
        for key, value in metadata.items()
    }

    results = orjson.dumps(metadata, option=orjson.OPT_INDENT_2 |
                           orjson.OPT_NON_STR_KEYS).decode('utf-8')

    return results
