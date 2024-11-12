from random import randint

from template_python.cryptography import decrypt_text, encrypt_text, obscure, unobscure


def test_obscure_unobscure():

    words_to_check: list[str] = [
        "Hello World!",
        "This is a lengthy sentence with numbers: 1234",
        "Punctuations?!@#$%^&*()",
    ]

    for words in words_to_check:
        obscured: str = obscure(words)
        obscured2: str = obscure(words)
        unobscured: str = unobscure(obscured)
        unobscured2: str = unobscure(obscured2)
        assert unobscured == words
        assert words != obscured
        assert obscured == obscured2
        assert unobscured == unobscured2


def random_text(length: int) -> bytes:
    def rand_lower():
        return chr(randint(ord("a"), ord("z")))

    string = "".join([rand_lower() for _ in range(length)])
    return bytes(string, encoding="utf-8")


def test_encoding():
    string = random_text(100)
    assert string.decode() != string
    assert string.decode().encode() == string


def test_encryption():
    string = random_text(100).decode()
    password = random_text(20).decode()
    assert encrypt_text(string, password) != string
    assert decrypt_text(encrypt_text(string, password), password) == string
