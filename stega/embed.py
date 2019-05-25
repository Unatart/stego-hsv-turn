import cv2 as cv
import numpy as np
from utils.bit_manage import str2bits_list, lsb


def hide(img, encoded, msg_bits, ind, row, col):
    rgb = img[row][col]
    hsv = cv.cvtColor(np.uint8([[rgb]]), cv.COLOR_RGB2HSV)[0][0]
    h = hsv[0]
    s = hsv[1]
    v = hsv[2]

    v = lsb(v, msg_bits[ind])

    rgb = cv.cvtColor(np.uint8([[[h, s, v]]]), cv.COLOR_HSV2RGB)[0][0]
    encoded[row][col] = rgb


def embed(img, msg, angle):
    if len(msg) == 0:
        return img.copy()
    msg = str(len(msg)) + "/" + str(msg)
    msg_bits = "".join(str2bits_list(msg, "UTF-8"))
    encoded = img.copy()
    height, width, channels = img.shape
    height, width = height - 1, width - 1
    if len(msg_bits) > height * width:
        return -1
    ind = 0
    if angle == 0:
        for row in range(0, height):
            for col in range(0, width):
                if ind <= len(msg_bits) - 1:
                    hide(img, encoded, msg_bits, ind, row, col)
                    ind += 1
                else:
                    break
    elif angle == 1:
        for row in range(0, height):
            for col in range(width, 0, -1):
                if ind <= len(msg_bits) - 1:
                    hide(img, encoded, msg_bits, ind, row, col)
                    ind += 1
                else:
                    break
    elif angle == 2:
        for row in range(height, 0, -1):
            for col in range(0, width):
                if ind <= len(msg_bits) - 1:
                    hide(img, encoded, msg_bits, ind, row, col)
                    ind += 1
                else:
                    break
    else:
        for row in range(height, 0, -1):
            for col in range(width, 0, -1):
                if ind <= len(msg_bits) - 1:
                    hide(img, encoded, msg_bits, ind, row, col)
                    ind += 1
                else:
                    break

    return encoded

