import cv2
import numpy as np


def crop(path, points):
    image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    roi_corners = np.array([points], dtype=np.int32)
    mask = np.zeros(image.shape, dtype=np.uint8)
    channel_count = image.shape[2]
    ignore_mask_color = (255,)*channel_count
    cv2.fillPoly(mask, roi_corners, ignore_mask_color)
    white = np.full(mask.shape, 255, dtype=mask.dtype)
    result_white = white.copy()
    if mask.shape[2] == 4:
        a,b,c,d = cv2.split(mask)
    else:
        a, b, c = cv2.split(mask)
    cv2.bitwise_and(white, image, result_white, a)
    return result_white


def make_transparent(masked_image):
    if masked_image.shape[2] == 4:
        return masked_image
    b_channel, g_channel, r_channel = cv2.split(masked_image)
    alpha_channel = np.full(b_channel.shape, 255, dtype=b_channel.dtype)
    mat = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            m = mat[i, j]
            if m[0] > 230 and m[1] > 230 and m[2] > 230:
                mat[i, j] = [255, 255, 255, 0]
    return mat
