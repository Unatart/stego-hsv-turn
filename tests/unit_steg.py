from unittest import TestCase
from secret_sharing.secret_sharing import share_secret, reconstruct_secret
from aes.aes import AESCipher
from utils.for_tests import random_string, correct_id, correct_string


class UnitTSS(TestCase):
    def test_tss_correct_share(self):
        msg = correct_string
        n = 8
        k = 4
        id = correct_id
        result = share_secret(k, n, msg, id)

        assert len(result) == n

    def test_tss_invalid_n(self):
        msg = correct_string
        n = 0
        k = 4
        id = correct_id
        result = []
        try:
            result = share_secret(k, n, msg, id)
        except:
            assert len(result) == 0


    def test_tss_invalid_k(self):
        msg = correct_string
        n = 8
        k = 0
        id = correct_id
        result = []
        try:
            result = share_secret(k, n, msg, id)
        except:
            assert len(result) == 0

    def test_tss_invalid_msg_small(self):
        msg = ''
        n = 0
        k = 4
        id = correct_id
        result = []
        try:
            result = share_secret(k, n, msg, id)
        except:
            assert len(result) == 0

    def test_tss_invalid_msg_large(self):
        msg = random_string(65635)
        n = 0
        k = 4
        id = correct_id
        result = []
        try:
            result = share_secret(k, n, msg, id)
        except:
            assert len(result) == 0

    def test_tss_correct_reconstruct(self):
        msg = correct_string
        n = 8
        k = 4
        id = correct_id
        result = share_secret(k, n, msg, id)

        assert len(result) == n

        str_reconstruct = reconstruct_secret(result)

        assert str_reconstruct.decode() == msg

    def test_tss_incorrect_reconstruct_empty_shares(self):
        msg = correct_string
        n = 8
        k = 4
        id = correct_id
        result = share_secret(k, n, msg, id)

        assert len(result) == n
        str_reconstruct = ''
        result = []
        try:
            str_reconstruct = reconstruct_secret(result)
        except:
            assert str_reconstruct != msg

    def test_tss_incorrect_reconstruct_incomplete_shares(self):
        msg = correct_string
        n = 8
        k = 4
        id = correct_id
        result = share_secret(k, n, msg, id)

        assert len(result) == n

        str_reconstruct = ''
        try:
            str_reconstruct = reconstruct_secret(result[:2])
        except:
            assert str_reconstruct != msg

    def test_tss_extended(self):
        msg = correct_string
        n = 8
        k = 4
        id = correct_id
        result = share_secret(k, n, msg, id)

        assert len(result) == n

        new_result = result[:4] + result
        str_reconstruct = ''
        try:
            str_reconstruct = reconstruct_secret(new_result)
        except:
            assert str_reconstruct == msg


class UnitAES(TestCase):
    def test_aes_correct_encode(self):
        str = random_string(10)
        aes = AESCipher()
        key = aes.encrypt(str)

        assert len(key) != 0

    def test_aes_incorrect_encode(self):
        str = random_string(10)
        aes = AESCipher()
        key = ''
        try:
            key = aes.encrypt(str)
        except:
            assert len(key) == 0

    def test_aes_correct_decode(self):
        str = random_string(10)
        aes = AESCipher()
        key = aes.encrypt(str)
        str_encoded = aes.decrypt(key)

        assert str == str_encoded

    def test_aes_incorrect_decode(self):
        str = random_string(10)
        aes = AESCipher()
        key = b'247'
        str_encoded = ''
        try:
            str_encoded = aes.decrypt(key)
        except:
            assert str != str_encoded

