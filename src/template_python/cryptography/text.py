import random
import string
import zlib
from base64 import urlsafe_b64decode, urlsafe_b64encode
from pathlib import Path


def generate_seed() -> int:
    letter_collection: str = string.ascii_letters + string.digits + string.punctuation
    lib_name: str = Path(__file__).parent.parent.name
    sum = 0

    for letter in lib_name:
        sum += letter_collection.index(letter) + 1
    return sum ** len(lib_name)


RANDOM_SEED: int = generate_seed()


def obscure(text: str) -> str:
    values = text_soup()

    def rotate_list(text: str, num: int) -> str:
        return text[num:] + text[:num]

    text = urlsafe_b64encode(zlib.compress(text.encode(), 9)).decode()
    letter_collection: str = string.ascii_letters + string.digits + string.punctuation
    result = ""
    for i, letter in enumerate(text):
        mapper = {
            k: v for k, v in zip(letter_collection, rotate_list(text=values, num=i))
        }
        result += mapper[letter]
    return result


def unobscure(obscured: str) -> str:
    values = text_soup()

    def rotate_list(text: str, num: int) -> str:
        return text[num:] + text[:num]

    original = ""
    letter_collection: str = string.ascii_letters + string.digits + string.punctuation
    for i, letter in enumerate(obscured):
        mapper = {
            v: k for k, v in zip(letter_collection, rotate_list(text=values, num=i))
        }
        original += mapper[letter]
    return zlib.decompress(urlsafe_b64decode(original.encode())).decode()


def text_soup(seed: int = RANDOM_SEED) -> str:
    letter_base = list(string.ascii_letters + string.digits + string.punctuation)
    random.seed(seed)
    random.shuffle(letter_base)
    return "".join(letter_base)
