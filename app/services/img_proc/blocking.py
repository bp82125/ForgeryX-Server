import cv2
import numpy as np


def extract_blocking_artifact(image, diff_threshold=50, accumulator_size=33, block_size=8):
    luminance = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)[:, :, 0]

    vertical_edges, horizontal_edges = compute_edge_artifacts(
        luminance, diff_threshold, accumulator_size)

    vertical_edges = cv2.resize(
        vertical_edges, (luminance.shape[1], luminance.shape[0]))
    horizontal_edges = cv2.resize(
        horizontal_edges, (luminance.shape[1], luminance.shape[0]))

    block_diff = vertical_edges + horizontal_edges
    block_artifact_map = process_blocks(block_diff, block_size)

    normalized_map = cv2.normalize(
        block_artifact_map, None, 0, 255, cv2.NORM_MINMAX)
    heatmap = cv2.applyColorMap(
        normalized_map.astype(np.uint8), cv2.COLORMAP_JET)

    return heatmap


def compute_edge_artifacts(luminance, diff_threshold, accumulator_size):
    vertical_diff = compute_diff(
        luminance, diff_threshold, axis=0, accumulator_size=accumulator_size)
    horizontal_diff = compute_diff(
        luminance, diff_threshold, axis=1, accumulator_size=accumulator_size)

    vertical_edges = process_edge_map(vertical_diff, accumulator_size, axis=0)
    horizontal_edges = process_edge_map(
        horizontal_diff, accumulator_size, axis=1)

    return vertical_edges, horizontal_edges


def compute_diff(image, diff_threshold, axis, accumulator_size):
    pad_width = ((accumulator_size // 2, accumulator_size // 2), (0, 0)) if axis == 1 else \
                ((0, 0), (accumulator_size // 2, accumulator_size // 2))
    padded_image = np.pad(image, pad_width, mode='reflect')

    if axis == 0:
        diff = np.abs(2 * padded_image[1:-1, :] -
                      padded_image[:-2, :] - padded_image[2:, :])
    else:
        diff = np.abs(2 * padded_image[:, 1:-1] -
                      padded_image[:, :-2] - padded_image[:, 2:])

    return np.clip(diff, 0, diff_threshold)


def process_edge_map(edge_diff, accumulator_size, axis):
    summed_edges = cv2.boxFilter(edge_diff, -1, (accumulator_size, 1) if axis == 0 else
                                 (1, accumulator_size), normalize=False)

    mid_filtered = cv2.medianBlur(
        summed_edges.astype(np.uint8), accumulator_size)
    return summed_edges - mid_filtered


def process_blocks(image, block_size):
    blocks = (image.shape[0] // block_size, image.shape[1] // block_size)
    block_scores = np.zeros(blocks)

    for i in range(blocks[0]):
        for j in range(blocks[1]):
            block = image[(i * block_size):((i + 1) * block_size),
                          (j * block_size):((j + 1) * block_size)]
            block_scores[i, j] = compute_block_score(block)

    return block_scores


def compute_block_score(block):
    block = block.astype(np.float64)

    row_sum = np.sum(block[1:-1, 1:-1], axis=1)
    col_sum = np.sum(block[1:-1, 1:-1], axis=0)
    row_edge = [np.sum(block[1:-1, 0]), np.sum(block[1:-1, -1])]
    col_edge = [np.sum(block[0, 1:-1]), np.sum(block[-1, 1:-1])]

    return np.max(row_sum) + np.max(col_sum) - np.min(row_edge) - np.min(col_edge)
