import random
import string
from typing import Dict


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def random_int() -> int:
    return random.randint(0, 1000)


def random_float() -> float:
    return 10000 * random.random()
