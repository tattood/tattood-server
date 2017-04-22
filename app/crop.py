import cv2
import json
import numpy as np
import sys
import subprocess


def crop(path, points):
    image = cv2.imread(path, -1)
    roi_corners = np.array([points], dtype=np.int32)
    mask = np.zeros(image.shape, dtype=np.uint8)
    channel_count = image.shape[2]  # i.e. 3 or 4 depending on your image
    ignore_mask_color = (255,)*channel_count
    cv2.fillPoly(mask, roi_corners, ignore_mask_color)
    masked_image = cv2.bitwise_and(image, mask)
    cv2.imwrite(path, masked_image)


def tags():
    THRESHOLD = 0.2
    tags = np.array([])
    try:
        subprocess.check_output(["python",
                                 "./models-master/tutorials/image/imagenet/classify_image.py",
                                 "--image_file", "image_masked.png"])
    except subprocess.CalledProcessError as e:
        splittedOutput = e.output.split("|")
        for asd in splittedOutput:
            tags = np.append(tags, asd)
        finalTags = np.array([])
    for i in range(1, len(tags)):
        if i % 2 == 1 and float(tags[i]) > THRESHOLD:
            if "," in tags[i-1]:
                splitted = tags[i-1].split(",")
                for str in splitted:
                    finalTags = np.append(finalTags, str.strip())
            else:
                finalTags = np.append(finalTags, tags[i-1].strip())
    return finalTags