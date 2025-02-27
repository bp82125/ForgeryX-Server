import os
import shutil
import orjson
import torch
import cv2


def prepare_image(image):
    return torch.from_numpy(cv2.cvtColor(image, cv2.COLOR_BGR2RGB).transpose(2, 0, 1))


def ensure_jpeg(image):
    encode_param = [cv2.IMWRITE_JPEG_QUALITY, 95]

    success, encoded_img = cv2.imencode(".jpg", image, encode_param)
    if success:
        decoded_img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
        if decoded_img is not None:
            return prepare_image(decoded_img)

    return cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)


def save_to_json(result, file_dir, file_name="results.json"):
    json_path = os.path.join(file_dir, file_name)

    if os.path.exists(json_path):
        with open(json_path, "rb") as f:
            try:
                data = orjson.loads(f.read())
            except orjson.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(result)

    with open(json_path, "wb") as f:
        f.write(orjson.dumps(data, option=orjson.OPT_INDENT_2))


def save_uploaded_file(file, file_dir):
    os.makedirs(file_dir, exist_ok=True)
    file_extension = os.path.splitext(
        file.filename)[1] if file.filename else ".jpg"
    file_location = os.path.join(file_dir, f"tampered{file_extension}")

    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return file_location
    except Exception as e:
        return None


def resize_image(file_location, max_dimension=2000):
    image = cv2.imread(file_location)

    if image is None:
        return None

    height, width = image.shape[:2]
    if height > max_dimension or width > max_dimension:
        scaling_factor = max_dimension / max(height, width)
        new_size = (int(width * scaling_factor), int(height * scaling_factor))
        image = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)
        cv2.imwrite(file_location, image)

    return image


def convert_json_to_sse_response(json_str):
    return f"data: {json_str}\n\n"
