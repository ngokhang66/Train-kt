# random password generator example
import string
import secrets
import sys


def random_pwd():
    letters = string.ascii_letters.lower()
    letters_up = letters.upper()
    numbers = string.digits
    special_chars = string.punctuation

    alphabet = letters + numbers + letters_up + numbers

    pwd_len = 8
    pwd = ''.join((secrets.choice(alphabet) for i in range(pwd_len)))

    return pwd


sys.modules[__name__] = random_pwd
