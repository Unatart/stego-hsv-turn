from typing import List

ENCODINGS = {"UTF-8": 8, "UTF-32LE": 32}


def str2bits_list(chars: str, encoding: str = "UTF-8") -> List[str]:
    return [bin(ord(x))[2:].rjust(ENCODINGS[encoding], "0") for x in chars]


def lsb(component: int, bit: str) -> int:
    return component & ~1 | int(bit)
