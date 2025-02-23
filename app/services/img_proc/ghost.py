import cv2


def ghost(image_path, quality_range=(75, 100), threshold=30):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image at path {image_path} could not be loaded.")
    
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    diff_maps = []

    for quality in range(quality_range[0], quality_range[1] + 1, 5):
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        _, encoded_img = cv2.imencode('.jpg', gray_image, encode_param)
        recompressed = cv2.imdecode(encoded_img, cv2.IMREAD_GRAYSCALE)

        if recompressed is None or recompressed.shape != gray_image.shape:
            continue

        diff = cv2.absdiff(gray_image, recompressed)
        diff_normalized = cv2.normalize(diff, None, 0, 255, cv2.NORM_MINMAX)
        _, diff_thresholded = cv2.threshold(
            diff_normalized, threshold, 255, cv2.THRESH_BINARY)

        diff_maps.append((quality, diff_thresholded))

    return diff_maps
