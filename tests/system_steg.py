from unittest import TestCase
from manager import encode, decode
from utils.for_tests import random_string
import os


class SystemManager(TestCase):
    def test_correct_encode_png(self):
        img = 'test_data/lena.png'
        msg = random_string(100)
        result = encode(img, msg, 5, 8, 'test_data/output.png')

        assert 'Встраивание прошло успешно.<br>' in result

        os.remove('test_data/output.png')
        os.remove('test_data/key')

    def test_correct_encode_jpg(self):
        img = 'test_data/2.jpg'
        msg = random_string(100)
        result = encode(img, msg, 5, 8, 'test_data/output.png')

        assert 'Встраивание прошло успешно.<br>' in result

        os.remove('test_data/output.png')
        os.remove('test_data/key')

    def test_incorrect_tss_encode(self):
        img = 'test_data/2.jpg'
        msg = random_string(100)
        result = encode(img, msg, 0, 0, 'test_data/output.png')

        assert not ('Встраивание прошло успешно.<br>' in result)

    def test_incorrect_embed_encode(self):
        img = 'test_data/2.jpg'
        msg = random_string(360000)
        result = encode(img, msg, 5, 8, 'test_data/output.png')

        assert not ('Встраивание прошло успешно.<br>' in result)

    def test_correct_decode_png(self):
        img = 'test_data/lena.png'
        msg = random_string(100)
        result = encode(img, msg, 5, 8, 'test_data/output.png')

        assert 'Встраивание прошло успешно.<br>' in result

        text = decode('test_data/output.png', 'test_data/key', 'test_data/msg')
        os.remove('test_data/output.png')
        os.remove('test_data/key')

        assert 'Расшифровка прошла успешно.<br>' in text

    def test_correct_decode_jpg(self):
        img = 'test_data/2.jpg'
        msg = random_string(100)

        result = encode(img, msg, 5, 8, 'test_data/output.png')

        assert 'Встраивание прошло успешно.<br>' in result

        text = decode('test_data/output.png', 'test_data/key', 'test_data/msg')
        os.remove('test_data/output.png')
        os.remove('test_data/key')

        assert 'Расшифровка прошла успешно.<br>' in text

    def test_incorrect_tss_decode(self):
        img = 'test_data/2.jpg'
        msg = random_string(100)
        result = encode(img, msg, 0, 0, 'test_data/output.png')
        f = None

        assert not ('Встраивание прошло успешно.<br>' in result)
        try:
            f = open('test_data/output.png')
        except FileNotFoundError:
            assert f is None

    def test_incorrect_extract_decode(self):
        img = 'test_data/2.jpg'
        msg = random_string(360000)
        result = encode(img, msg, 5, 8, 'test_data/output.png')
        f = None

        assert not ('Встраивание прошло успешно.<br>' in result)
        try:
            f = open('test_data/output.png')
        except FileNotFoundError:
            assert f is None