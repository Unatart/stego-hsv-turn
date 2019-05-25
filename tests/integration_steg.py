from unittest import TestCase
from stega.extract import extract
from stega.embed import embed
import cv2
from utils.for_tests import random_string
import numpy as np

class IntegrationStegano(TestCase):
    def test_embed_correct_png(self):
        img = cv2.imread('test_data/lena.png')
        msg = random_string(100)
        encoded_img = embed(img, msg, 0)

        assert not np.allclose(img, encoded_img)

    def test_embed_correct_jpg(self):
        img = cv2.imread('test_data/2.jpg')
        msg = random_string(100)
        encoded_img = embed(img, msg, 0)

        assert not np.allclose(img, encoded_img)

    def test_embed_big_msg_incorrect(self):
        img = cv2.imread('test_data/lena.png')
        height, width, channels = img.shape
        msg = random_string(height*width*channels)
        encoded_img = embed(img, msg, 0)

        assert not np.allclose(img, encoded_img)

    def test_embed_empty_msg_incorrect(self):
        img = cv2.imread('test_data/lena.png')
        msg = ''
        encoded_img = embed(img, msg, 0)

        assert np.allclose(img, encoded_img)

    def test_extract_correct_png(self):
        img = cv2.imread('test_data/lena.png')
        msg = random_string(100)
        encoded_img = embed(img, msg, 0)

        assert not np.allclose(img, encoded_img)

        result = extract(encoded_img, 0)

        assert result == msg

    def test_extract_correct_jpg(self):
        img = cv2.imread('test_data/2.jpg')
        msg = random_string(100)
        encoded_img = embed(img, msg, 0)

        assert not np.allclose(img, encoded_img)

        result = extract(encoded_img, 0)

        assert result == msg

    def test_extract_incorrect(self):
        img = cv2.imread('test_data/lena.png')
        msg = random_string(100)
        encoded_img = embed(img, msg, 0)

        assert not np.allclose(img, encoded_img)

        result = extract(encoded_img, 1)

        assert result != msg