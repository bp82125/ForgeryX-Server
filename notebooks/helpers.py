import os
import orjson

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

metadata_path = os.path.join(BASE_DIR, 'metadata_mappings.json')

with open(metadata_path, 'rb') as f:
    METADATA_MAPPINGS = orjson.loads(f.read())


def convert_encoding_process(value):
    return METADATA_MAPPINGS["encoding_process"].get(str(value), "Unknown Encoding Process")


def convert_filesize(file_size_bytes):
    file_size_kb = round(file_size_bytes / 1024)
    return f"Filesize {file_size_kb} kB"


def convert_exif_byte_order(byte_order):
    return METADATA_MAPPINGS["byte_order"].get(byte_order, "Unknown byte order")


def convert_jfif_version(jfif_version):
    major, minor = jfif_version.split()
    return f"JFIF {major}.{int(minor):02d}"


def convert_exif_orientation(orientation):
    return METADATA_MAPPINGS["orientation"].get(str(orientation), "Unknown orientation")


def convert_resolution_unit(unit):
    return METADATA_MAPPINGS["resolution_unit"].get(str(unit), "Unknown resolution unit")


def convert_ycbcr_subsampling(subsampling):
    return METADATA_MAPPINGS["ycbcr_subsampling"].get(subsampling, "Unknown subsampling")


def convert_ycbcr_positioning(positioning):
    return METADATA_MAPPINGS["ycbcr_positioning"].get(str(positioning), "Unknown positioning")


def convert_exposure_program(program):
    return METADATA_MAPPINGS["exposure_program"].get(str(program), "Unknown exposure program")


def convert_components_configuration(components):
    component_mapping = METADATA_MAPPINGS["components"]
    return ", ".join([component_mapping.get(str(c), "Unknown") for c in components.split()])


def convert_subject_distance(distance):
    return f"{distance} meters"


def convert_metering_mode(mode):
    return METADATA_MAPPINGS["metering_mode"].get(str(mode), "Unknown metering mode")


def convert_flash_mode(flash):
    if isinstance(flash, int) and flash > 0:
        flash_str = str(flash)
    else:
        try:
            if isinstance(flash, str) and flash.startswith('0x'):
                flash_str = str(int(flash, 16))
            else:
                flash_str = str(flash)
        except (ValueError, TypeError):
            flash_str = str(flash)

    return METADATA_MAPPINGS["flash_mode"].get(flash_str, "Unknown flash mode")


def convert_color_space(color_space):
    return METADATA_MAPPINGS["color_space"].get(str(color_space), "Unknown color space")


def convert_interop_index(index):
    return METADATA_MAPPINGS["interop_index"].get(index, "Unknown Interop Index")


def convert_sensing_method(method):
    return METADATA_MAPPINGS["sensing_method"].get(str(method), "Unknown sensing method")


def convert_scene_type(scene):
    return METADATA_MAPPINGS["scene_type"].get(str(scene), "Unknown scene type")


def convert_custom_rendered(rendered):
    return METADATA_MAPPINGS["custom_rendered"].get(str(rendered), "Unknown custom rendering")


def convert_exposure_mode(mode):
    return METADATA_MAPPINGS["exposure_mode"].get(str(mode), "Unknown exposure mode")


def convert_white_balance(wb):
    return METADATA_MAPPINGS["white_balance"].get(str(wb), "Unknown white balance")


def convert_scene_capture_type(scene_capture):
    return METADATA_MAPPINGS["scene_capture_type"].get(str(scene_capture), "Unknown scene capture type")


def convert_contrast(contrast):
    return METADATA_MAPPINGS["contrast"].get(str(contrast), "Unknown contrast value")


def convert_saturation(saturation):
    return METADATA_MAPPINGS["saturation"].get(str(saturation), "Unknown saturation value")


def convert_sharpness(sharpness):
    return METADATA_MAPPINGS["sharpness"].get(str(sharpness), "Unknown sharpness value")


def convert_subject_distance_range(distance):
    return METADATA_MAPPINGS["subject_distance_range"].get(str(distance), "Unknown subject distance range")


def convert_profile_version(version):
    return METADATA_MAPPINGS["profile_version"].get(str(version), f"Unknown profile version")


def convert_profile_class(profile_class):
    return METADATA_MAPPINGS["profile_class"].get(profile_class, f"Unknown profile class")


def convert_cmm_flags(cmm_flags):
    return METADATA_MAPPINGS["cmm_flags"].get(str(cmm_flags), f"Unknown CMM flag")


def convert_device_manufacturer(device_manufacturer):
    return METADATA_MAPPINGS["device_manufacturer"].get(device_manufacturer, f"Unknown device manufacturer")


def convert_device_attributes(device_attributes):
    return METADATA_MAPPINGS["device_attributes"].get(device_attributes, f"Unknown device attributes")


def convert_rendering_intent(rendering_intent):
    return METADATA_MAPPINGS["rendering_intent"].get(str(rendering_intent), f"Unknown Rendering Intent")


def convert_profile_creator(profile_creator):
    return convert_device_manufacturer(profile_creator)


def format_profile_id(profile_id):
    if isinstance(profile_id, str):
        profile_id = [int(byte) for byte in profile_id.split()]

    if not isinstance(profile_id, (list, tuple)) or len(profile_id) != 16:
        return "Invalid Profile ID format"

    return "".join(f"{byte:02x}" for byte in profile_id)


def format_image_size(image_size):
    if not isinstance(image_size, str):
        return "Invalid Image Size format"

    w, h = image_size.split(' ')

    return f"{w}x{h}"


def round_megapixels(megapixels):
    new_value = float(megapixels) if isinstance(
        megapixels, str) else megapixels

    if not isinstance(new_value, (int, float)):
        return "Invalid Megapixel value"

    return round(new_value, 1)


def round_scale_factor(scale_factor):
    new_value = float(scale_factor) if isinstance(
        scale_factor, str) else scale_factor

    if not isinstance(new_value, (int, float)):
        return "Invalid Scale Factor"

    return round(new_value, 2)


def format_shutter_speed(shutter_speed):
    new_value = float(shutter_speed) if isinstance(
        shutter_speed, str) else shutter_speed

    if not isinstance(new_value, (int, float)) or new_value <= 0:
        return "Invalid Shutter Speed"

    return f"1/{round(1 / new_value)} sec"


def format_circle_of_confusion(circle_of_confusion):
    new_value = float(circle_of_confusion) if isinstance(
        circle_of_confusion, str) else circle_of_confusion

    if not isinstance(new_value, float):
        return "Invalid Circle of Confusion value"

    return f"{round(new_value, 4)} mm"


def format_fov(fov):
    new_value = float(fov) if isinstance(fov, str) else fov

    if not isinstance(new_value, (int, float)):
        return "Invalid FOV value"

    return f"{round(new_value, 1)}°"


def format_hyperfocal_distance(hyperfocal_distance):
    new_value = float(hyperfocal_distance) if isinstance(
        hyperfocal_distance, str) else hyperfocal_distance

    if not isinstance(new_value, (int, float)):
        return "Invalid Hyperfocal Distance value"

    return f"{round(new_value, 2)} m"


def format_light_value(light_value):
    new_value = float(light_value) if isinstance(
        light_value, str) else light_value

    if not isinstance(new_value, (int, float)):
        return "Invalid Light Value"

    return f"{round(new_value, 1)}"


def convert_to_actual_focal_length(equivalent_focal_length, crop_factor):
    if crop_factor <= 0:
        raise ValueError("Crop factor must be greater than zero")

    actual_focal_length = float(equivalent_focal_length) / float(crop_factor)
    return f'{round(actual_focal_length, 2)} mm'


EXACT_MATCHES = {
    'FileSize': convert_filesize,
    'ExifByteOrder': convert_exif_byte_order,
    'EncodingProcess': convert_encoding_process,
    'YCbCrSubSampling': convert_ycbcr_subsampling,
    'YCbCrPositioning': convert_ycbcr_positioning,
    'JFIFVersion': convert_jfif_version,
    'ResolutionUnit': convert_resolution_unit,
    'Orientation': convert_exif_orientation,
    'ExposureProgram': convert_exposure_program,
    'ComponentsConfiguration': convert_components_configuration,
    'SubjectDistance': convert_subject_distance,
    'MeteringMode': convert_metering_mode,
    'Flash': convert_flash_mode,
    'ColorSpace': convert_color_space,
    'InteropIndex': convert_interop_index,
    'SensingMethod': convert_sensing_method,
    'SceneType': convert_scene_type,
    'CustomRendered': convert_custom_rendered,
    'ExposureMode': convert_exposure_mode,
    'WhiteBalance': convert_white_balance,
    'SceneCaptureType': convert_scene_capture_type,
    'Contrast': convert_contrast,
    'Saturation': convert_saturation,
    'Sharpness': convert_sharpness,
    'SubjectDistanceRange': convert_subject_distance_range,
    'ProfileVersion': convert_profile_version,
    'ProfileClass': convert_profile_class,
    'CMMFlags': convert_cmm_flags,
    'DeviceManufacturer': convert_device_manufacturer,
    'DeviceAttributes': convert_device_attributes,
    'RenderingIntent': convert_rendering_intent,
    'ProfileCreator': convert_profile_creator,
    'ProfileID': format_profile_id,
    'ImageSize': format_image_size,
    'Megapixels': round_megapixels,
    'ScaleFactor35efl': round_scale_factor,
    'ShutterSpeed': format_shutter_speed,
    'CircleOfConfusion': format_circle_of_confusion,
    'FOV': format_fov,
    'HyperfocalDistance': format_hyperfocal_distance,
    'LightValue': format_light_value,
}


def convert_metadata_value(key, value):
    if key in EXACT_MATCHES:
        return EXACT_MATCHES[key](value)

    return value
