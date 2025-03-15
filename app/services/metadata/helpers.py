def convert_metadata_value(key, value):
    if not value:
        return value

    exact_matches = {
        'FileSize': convert_filesize,
        'FilePermissions': convert_file_permissions,
        'ExifByteOrder': convert_exif_byte_order,
        'EncodingProcess': convert_encoding_process,
        'YCbCrSubSampling': convert_ycbcr_subsampling,
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
        'FocalLength35efl': format_focal_length_35efl,
        'HyperfocalDistance': format_hyperfocal_distance,
        'LightValue': format_light_value,
    }

    if key in exact_matches:
        return exact_matches[key](value)

    if any(date_key in key for date_key in ['CreateDate', 'ModifyDate', 'FileModifyDate', 'FileAccessDate', 'FileInodeChangeDate', 'DateTimeOriginal', 'ProfileDateTime']):
        return value

    if isinstance(value, (list, tuple)):
        return ', '.join(str(v) for v in value)

    return value


def convert_encoding_process(value):
    encoding_meanings = {
        0: "Baseline DCT (Huffman Coding)",
        1: "Baseline DCT (Huffman Coding)",
        2: "Extended Sequential DCT (Huffman Coding)",
        3: "Progressive DCT (Huffman Coding)",
        4: "Lossless JPEG (Predictive Coding, may use Huffman or Arithmetic)"
    }
    return encoding_meanings.get(value, "Unknown Encoding Process")


def convert_filesize(file_size_bytes):
    file_size_kb = round(file_size_bytes / 1024)
    return f"{file_size_kb} kB"


def convert_exif_byte_order(byte_order):
    if byte_order == "II":
        return "Little-Endian (Intel byte order)"
    elif byte_order == "MM":
        return "Big-Endian (Motorola byte order)"
    else:
        return "Unknown byte order"


def convert_jfif_version(jfif_version):
    major, minor = jfif_version.split()
    return f"JFIF {major}.{int(minor):02d}"


def convert_exif_orientation(orientation):
    orientation_mapping = {
        1: "Horizontal (normal)",
        2: "Flipped horizontally",
        3: "Rotated 180°",
        4: "Flipped vertically",
        5: "Rotated 90° and flipped horizontally",
        6: "Rotated 90° clockwise",
        7: "Rotated 90° and flipped vertically",
        8: "Rotated 270° clockwise",
    }
    return orientation_mapping.get(orientation, "Unknown orientation")


def convert_file_permissions(permission):
    permission_octal = int(str(permission)[-3:])
    mapping = {
        0: "---", 1: "--x", 2: "-w-", 3: "-wx", 4: "r--", 5: "r-x", 6: "rw-", 7: "rwx"
    }
    owner = mapping[(permission_octal // 100) % 10]
    group = mapping[(permission_octal // 10) % 10]
    others = mapping[permission_octal % 10]
    return f"-{owner}{group}{others}"


def convert_resolution_unit(unit):
    unit_mapping = {
        1: "No absolute unit of measurement",
        2: "Inches",
        3: "Centimeters"
    }
    return unit_mapping.get(unit, "Unknown resolution unit")


def convert_ycbcr_subsampling(subsampling):
    subsampling_mapping = {
        "1 1": "YCbCr4:4:4 (1 1)",
        "1 2": "YCbCr4:4:0 (1 2)",
        "1 4": "YCbCr4:4:1 (1 4)",
        "2 1": "YCbCr4:2:2 (2 1)",
        "2 2": "YCbCr4:2:0 (2 2)",
        "2 4": "YCbCr4:2:1 (2 4)",
        "4 1": "YCbCr4:1:1 (4 1)",
        "4 2": "YCbCr4:1:0 (4 2)",
    }
    return subsampling_mapping.get(subsampling, "Unknown subsampling")


def convert_ycbcr_positioning(positioning):
    positioning_mapping = {
        1: "Centered",
        2: "Co-sited"
    }
    return positioning_mapping.get(positioning, "Unknown positioning")


def convert_exposure_program(program):
    exposure_mapping = {
        0: "Not Defined",
        1: "Manual",
        2: "Program AE",
        3: "Aperture-priority AE",
        4: "Shutter speed priority AE",
        5: "Creative (Slow speed)",
        6: "Action (High speed)",
        7: "Portrait",
        8: "Landscape",
        9: "Bulb"
    }
    return exposure_mapping.get(program, "Unknown exposure program")


def convert_components_configuration(components):
    component_mapping = {
        0: "-",
        1: "Y",
        2: "Cb",
        3: "Cr"
    }
    return ", ".join([component_mapping.get(int(c), "Unknown") for c in components.split()])


def convert_subject_distance(distance):
    return f"{distance} meters"


def convert_metering_mode(mode):
    metering_mapping = {
        0: "Unknown",
        1: "Average",
        2: "Center-weighted average",
        3: "Spot",
        4: "Multi-spot",
        5: "Multi-segment",
        6: "Partial",
        255: "Other"
    }
    return metering_mapping.get(mode, "Unknown metering mode")


def convert_flash_mode(flash):
    flash_mapping = {
        0x0: "No Flash",
        0x1: "Fired",
        0x5: "Fired, Return not detected",
        0x7: "Fired, Return detected",
        0x8: "On, Did not fire",
        0x9: "On, Fired",
        0xd: "On, Return not detected",
        0xf: "On, Return detected",
        0x10: "Off, Did not fire",
        0x14: "Off, Did not fire, Return not detected",
        0x18: "Auto, Did not fire",
        0x19: "Auto, Fired",
        0x1d: "Auto, Fired, Return not detected",
        0x1f: "Auto, Fired, Return detected",
        0x20: "No flash function",
        0x30: "Off, No flash function",
        0x41: "Fired, Red-eye reduction",
        0x45: "Fired, Red-eye reduction, Return not detected",
        0x47: "Fired, Red-eye reduction, Return detected",
        0x49: "On, Red-eye reduction",
        0x4d: "On, Red-eye reduction, Return not detected",
        0x4f: "On, Red-eye reduction, Return detected",
        0x50: "Off, Red-eye reduction",
        0x58: "Auto, Did not fire, Red-eye reduction",
        0x59: "Auto, Fired, Red-eye reduction",
        0x5d: "Auto, Fired, Red-eye reduction, Return not detected",
        0x5f: "Auto, Fired, Red-eye reduction, Return detected",
    }
    return flash_mapping.get(flash, "Unknown flash mode")


def convert_color_space(color_space):
    color_space_mapping = {
        0x1: "sRGB",
        0x2: "Adobe RGB",
        0xfffd: "Wide Gamut RGB",
        0xfffe: "ICC Profile",
        0xffff: "Uncalibrated"
    }
    return color_space_mapping.get(color_space, "Unknown color space")


def convert_interop_index(index):
    interop_mapping = {
        "R03": "R03 - DCF option file (Adobe RGB)",
        "R98": "R98 - DCF basic file (sRGB)",
        "THM": "THM - DCF thumbnail file"
    }
    return interop_mapping.get(index, "Unknown Interop Index")


def convert_sensing_method(method):
    sensing_mapping = {
        1: "Monochrome area",
        2: "One-chip color area",
        3: "Two-chip color area",
        4: "Three-chip color area",
        5: "Color sequential area",
        6: "Monochrome linear",
        7: "Trilinear",
        8: "Color sequential linear"
    }
    return sensing_mapping.get(method, "Unknown sensing method")


def convert_scene_type(scene):
    return "Directly photographed" if scene == 1 else "Unknown scene type"


def convert_custom_rendered(rendered):
    custom_mapping = {
        0: "Normal",
        1: "Custom",
        2: "HDR (no original saved)",
        3: "HDR (original saved)",
        4: "Original (for HDR)",
        6: "Panorama",
        7: "Portrait HDR",
        8: "Portrait"
    }
    return custom_mapping.get(rendered, "Unknown custom rendering")


def convert_exposure_mode(mode):
    mode_mapping = {
        0: "Auto",
        1: "Manual",
        2: "Auto bracket"
    }
    return mode_mapping.get(mode, "Unknown exposure mode")


def convert_white_balance(wb):
    return "Auto" if wb == 0 else "Manual" if wb == 1 else "Unknown white balance"


def convert_scene_capture_type(scene_capture):
    scene_capture_mapping = {
        0: "Standard",
        1: "Landscape",
        2: "Portrait",
        3: "Night",
        4: "Other"
    }
    return scene_capture_mapping.get(scene_capture, "Unknown scene capture type")


def convert_contrast(contrast):
    contrast_mapping = {
        0: "Normal",
        1: "Low",
        2: "High"
    }
    return contrast_mapping.get(contrast, "Unknown contrast value")


def convert_saturation(saturation):
    saturation_mapping = {
        0: "Normal",
        1: "Low",
        2: "High"
    }
    return saturation_mapping.get(saturation, "Unknown saturation value")


def convert_sharpness(sharpness):
    sharpness_mapping = {
        0: "Normal",
        1: "Soft",
        2: "Hard"
    }
    return sharpness_mapping.get(sharpness, "Unknown sharpness value")


def convert_subject_distance_range(distance):
    distance_mapping = {
        0: "Unknown",
        1: "Macro",
        2: "Close",
        3: "Distant"
    }
    return distance_mapping.get(distance, "Unknown subject distance range")


def convert_profile_version(version):
    version_mapping = {
        1024: "ICC Version 4.0",
        512: "ICC Version 2.0"
    }
    return version_mapping.get(version, f"Unknown profile version")


def convert_profile_class(profile_class):
    class_mapping = {
        "abst": "Abstract Profile",
        "cenc": "ColorEncodingSpace Profile",
        "link": "DeviceLink Profile",
        "mid ": "MultiplexIdentification Profile",
        "mlnk": "MultiplexLink Profile",
        "mntr": "Display Device Profile",
        "mvis": "MultiplexVisualization Profile",
        "nkpf": "Nikon Input Device Profile (NON-STANDARD!)",
        "nmcl": "NamedColor Profile",
        "prtr": "Output Device Profile",
        "scnr": "Input Device Profile",
        "spac": "ColorSpace Conversion Profile"
    }
    return class_mapping.get(profile_class, f"Unknown profile class")


def convert_cmm_flags(cmm_flags):
    flags_mapping = {
        0: "Not Embedded, Independent",
        1: "Embedded Profile",
        2: "Dependent on Embedded Profile"
    }
    return flags_mapping.get(cmm_flags, f"Unknown CMM flag")


def convert_device_manufacturer(device_manufacturer):
    manufacturer_mapping = {
        "4d2p": "Erdt Systems GmbH & Co KG",
        "AAMA": "Aamazing Technologies, Inc.",
        "ACER": "Acer Peripherals",
        "ACLT": "Acolyte Color Research",
        "ACTI": "Actix Systems, Inc.",
        "ADAR": "Adara Technology, Inc.",
        "ADBE": "Adobe Systems Inc.",
        "ADI ": "ADI Systems, Inc.",
        "AGFA": "Agfa Graphics N.V.",
        "ALMD": "Alps Electric USA, Inc.",
        "ALPS": "Alps Electric USA, Inc.",
        "ALWN": "Alwan Color Expertise",
        "AMTI": "Amiable Technologies, Inc.",
        "AOC ": "AOC International (U.S.A), Ltd.",
        "APAG": "Apago",
        "APPL": "Apple Computer Inc.",
        "AST ": "AST",
        "AT&T": "AT&T Computer Systems",
        "BAEL": "BARBIERI electronic",
        "BRCO": "Barco NV",
        "BRKP": "Breakpoint Pty Limited",
        "BROT": "Brother Industries, LTD",
        "BULL": "Bull",
        "BUS ": "Bus Computer Systems",
        "C-IT": "C-Itoh",
        "CAMR": "Intel Corporation",
        "CANO": "Canon, Inc. (Canon Development Americas, Inc.)",
        "CARR": "Carroll Touch",
        "CASI": "Casio Computer Co., Ltd.",
        "CBUS": "Colorbus PL",
        "CEL ": "Crossfield",
        "CELx": "Crossfield",
        "CGS ": "CGS Publishing Technologies International GmbH",
        "CHM ": "Rochester Robotics",
        "CIGL": "Colour Imaging Group, London",
        "CITI": "Citizen",
        "CL00": "Candela, Ltd.",
        "CLIQ": "Color IQ",
        "CMCO": "Chromaco, Inc.",
        "CMiX": "CHROMiX",
        "COLO": "Colorgraphic Communications Corporation",
        "COMP": "COMPAQ Computer Corporation",
        "COMp": "Compeq USA/Focus Technology",
        "CONR": "Conrac Display Products",
        "CORD": "Cordata Technologies, Inc.",
        "CPQ ": "Compaq Computer Corporation",
        "CPRO": "ColorPro",
        "CRN ": "Cornerstone",
        "CTX ": "CTX International, Inc.",
        "CVIS": "ColorVision",
        "CWC ": "Fujitsu Laboratories, Ltd.",
        "DARI": "Darius Technology, Ltd.",
        "DATA": "Dataproducts",
        "DCP ": "Dry Creek Photo",
        "DCRC": "Digital Contents Resource Center, Chung-Ang University",
        "DELL": "Dell Computer Corporation",
        "DIC ": "Dainippon Ink and Chemicals",
        "DICO": "Diconix",
        "DIGI": "Digital",
        "DL&C": "Digital Light & Color",
        "DPLG": "Doppelganger, LLC",
        "DS ": "Dainippon Screen",
        "DSOL": "DOOSOL",
        "DUPN": "DuPont",
        "EPSO": "Epson",
        "ESKO": "Esko-Graphics",
        "ETRI": "Electronics and Telecommunications Research Institute",
        "EVER": "Everex Systems, Inc.",
        "EXAC": "ExactCODE GmbH",
        "Eizo": "EIZO NANAO CORPORATION",
        "FALC": "Falco Data Products, Inc.",
        "FF ": "Fuji Photo Film Co.,LTD",
        "FFEI": "FujiFilm Electronic Imaging, Ltd.",
        "FNRD": "fnord software",
        "FORA": "Fora, Inc.",
        "FORE": "Forefront Technology Corporation",
        "FP ": "Fujitsu",
        "FPA ": "WayTech Development, Inc.",
        "FUJI": "Fujitsu",
        "FX ": "Fuji Xerox Co., Ltd.",
        "GCC ": "GCC Technologies, Inc.",
        "GGSL": "Global Graphics Software Limited",
        "GMB ": "Gretagmacbeth",
        "GMG ": "GMG GmbH & Co. KG",
        "GOLD": "GoldStar Technology, Inc.",
        "GOOG": "Google",
        "GPRT": "Giantprint Pty Ltd",
        "GTMB": "Gretagmacbeth",
        "GVC ": "WayTech Development, Inc.",
        "GW2K": "Sony Corporation",
        "HCI ": "HCI",
        "HDM ": "Heidelberger Druckmaschinen AG",
        "HERM": "Hermes",
        "HITA": "Hitachi America, Ltd.",
        "HP ": "Hewlett-Packard",
        "HTC ": "Hitachi, Ltd.",
        "HiTi": "HiTi Digital, Inc.",
        "IBM ": "IBM Corporation",
        "IDNT": "Scitex Corporation, Ltd.",
        "IEC ": "Hewlett-Packard",
        "IIYA": "Iiyama North America, Inc.",
        "IKEG": "Ikegami Electronics, Inc.",
        "IMAG": "Image Systems Corporation",
        "IMI ": "Ingram Micro, Inc.",
        "INTC": "Intel Corporation",
        "INTL": "N/A (INTL)",
        "INTR": "Intra Electronics USA, Inc.",
        "IOCO": "Iocomm International Technology Corporation",
        "IPS ": "InfoPrint Solutions Company",
        "IRIS": "Scitex Corporation, Ltd.",
        "ISL ": "Ichikawa Soft Laboratory",
        "ITNL": "N/A (ITNL)",
        "IVM ": "IVM",
        "IWAT": "Iwatsu Electric Co., Ltd.",
        "Idnt": "Scitex Corporation, Ltd.",
        "Inca": "Inca Digital Printers Ltd.",
        "Iris": "Scitex Corporation, Ltd.",
        "JPEG": "Joint Photographic Experts Group",
        "JSFT": "Jetsoft Development",
        "JVC ": "JVC Information Products Co.",
    }
    return manufacturer_mapping.get(device_manufacturer, f"Unknown device manufacturer")


def convert_device_attributes(device_attributes):
    attributes_mapping = {
        (0, 0): "Reflective, Glossy, Positive Polarity",
        (0, 1): "Reflective, Glossy, Negative Polarity",
        (1, 0): "Transparency, Matte, Positive Polarity",
        (1, 1): "Transparency, Matte, Negative Polarity"
    }
    return attributes_mapping.get(tuple(device_attributes), f"Unknown device attributes")


def convert_rendering_intent(rendering_intent):
    intent_mapping = {
        0: "Perceptual",
        1: "Media-Relative Colorimetric",
        2: "Saturation",
        3: "ICC-Absolute Colorimetric"
    }
    return intent_mapping.get(rendering_intent, f"Unknown Rendering Intent")


def convert_profile_creator(profile_creator):
    return convert_device_manufacturer(profile_creator)


def format_profile_id(profile_id):
    if not isinstance(profile_id, (list, tuple)) or len(profile_id) != 16:
        return "Invalid Profile ID format"

    return "".join(f"{byte:02x}" for byte in profile_id)


def format_image_size(image_size):
    if isinstance(image_size, str):
        parts = image_size.strip().split()
        if len(parts) == 2:
            try:
                width = int(parts[0])
                height = int(parts[1])
                return f"{width}x{height}"
            except ValueError:
                return "Invalid Image Size format"
        return "Invalid Image Size format"

    elif isinstance(image_size, (list, tuple)) and len(image_size) == 2:
        return f"{image_size[0]}x{image_size[1]}"

    return "Invalid Image Size format"


def round_megapixels(megapixels):
    if not isinstance(megapixels, (int, float)):
        return "Invalid Megapixel value"

    return round(megapixels, 1)


def round_scale_factor(scale_factor):
    if not isinstance(scale_factor, (int, float)):
        return "Invalid Scale Factor"

    return round(scale_factor, 2)


def format_shutter_speed(shutter_speed):
    if not isinstance(shutter_speed, (int, float)) or shutter_speed <= 0:
        return "Invalid Shutter Speed"

    return f"1/{round(1 / shutter_speed)} sec"


def format_circle_of_confusion(value):
    if not isinstance(value, (int, float)):
        return value

    return f"{round(value, 4)} mm"


def format_fov(value):
    if not isinstance(value, (int, float)):
        return "Invalid FOV value"

    return f"{round(value, 1)}°"


def format_focal_length_35efl(value):
    if not isinstance(value, (int, float)):
        return "Invalid Focal Length value"

    return f"{round(value)} mm"


def format_hyperfocal_distance(value):
    if not isinstance(value, (int, float)):
        return "Invalid Hyperfocal Distance value"

    return f"{round(value, 2)} m"


def format_light_value(value):
    if not isinstance(value, (int, float)):
        return "Invalid Light Value"

    return f"LV {round(value, 1)}"


def convert_to_actual_focal_length(equivalent_focal_length, crop_factor):
    if isinstance(equivalent_focal_length, str):
        equivalent_focal_length = float(
            equivalent_focal_length.replace('mm', '').strip())
    else:
        equivalent_focal_length = float(equivalent_focal_length)

    if isinstance(crop_factor, str):

        crop_factor = float(crop_factor.replace('mm', '').strip())
    else:
        crop_factor = float(crop_factor)

    if crop_factor <= 0:
        raise ValueError("Crop factor must be greater than zero")

    actual_focal_length = equivalent_focal_length / crop_factor
    return round(actual_focal_length, 2)
