import cv2
import numpy as np


def crop(path, points):
    image = cv2.imread(path, -1)
    roi_corners = np.array([points], dtype=np.int32)
    mask = np.zeros(image.shape, dtype=np.uint8)
    channel_count = image.shape[2]
    ignore_mask_color = (255,)*channel_count
    cv2.fillPoly(mask, roi_corners, ignore_mask_color)
    masked_image = cv2.bitwise_and(image, mask)
    cv2.imwrite(path, masked_image, params=[cv2.IMWRITE_PNG_COMPRESSION])
