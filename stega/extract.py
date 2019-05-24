import cv2 as cv
import numpy as np
from utils.bit_manage import ENCODINGS


def reveal(img, count, buff, row, col):
    rgb = img[row][col]
    hsv = cv.cvtColor(np.uint8([[rgb]]), cv.COLOR_RGB2HSV)[0][0]
    v = hsv[2]
    buff += (v & 1) << (ENCODINGS["UTF-8"] - 1 - count)
    count += 1
    return buff, count


def extract(img, angle):
    height, width, channels = img.shape
    height, width = height - 1, width - 1
    buff, count = 0, 0
    bit_msg = []
    limit = None

    if angle == 0:
        for row in range(0, height):
            for col in range(0, width):
                buff, count = reveal(img, count, buff, row, col)
                if count == ENCODINGS["UTF-8"]:
                    bit_msg.append(chr(buff))
                    buff, count = 0, 0
                    if bit_msg[-1] == "/" and limit is None:
                        try:
                            limit = int("".join(bit_msg[:-1]))
                        except:
                            pass

                if len(bit_msg) - len(str(limit)) - 1 == limit:
                    return "".join(bit_msg)[len(str(limit)) + 1:]
    elif angle == 1:
        for row in range(0, height):
            for col in range(width, 0, -1):
                buff, count = reveal(img, count, buff, row, col)
                if count == ENCODINGS["UTF-8"]:
                    bit_msg.append(chr(buff))
                    buff, count = 0, 0
                    if bit_msg[-1] == "/" and limit is None:
                        try:
                            limit = int("".join(bit_msg[:-1]))
                        except:
                            pass

                if len(bit_msg) - len(str(limit)) - 1 == limit:
                    return "".join(bit_msg)[len(str(limit)) + 1:]
    elif angle == 2:
        for row in range(height, 0, -1):
            for col in range(0, width):
                buff, count = reveal(img, count, buff, row, col)
                if count == ENCODINGS["UTF-8"]:
                    bit_msg.append(chr(buff))
                    buff, count = 0, 0
                    if bit_msg[-1] == "/" and limit is None:
                        try:
                            limit = int("".join(bit_msg[:-1]))
                        except:
                            pass

                if len(bit_msg) - len(str(limit)) - 1 == limit:
                    return "".join(bit_msg)[len(str(limit)) + 1:]
    else:
        for row in range(height, 0, -1):
            for col in range(width, 0, -1):
                buff, count = reveal(img, count, buff, row, col)
                if count == ENCODINGS["UTF-8"]:
                    bit_msg.append(chr(buff))
                    buff, count = 0, 0
                    if bit_msg[-1] == "/" and limit is None:
                        try:
                            limit = int("".join(bit_msg[:-1]))
                        except:
                            pass

                if len(bit_msg) - len(str(limit)) - 1 == limit:
                    return "".join(bit_msg)[len(str(limit)) + 1:]