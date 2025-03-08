from copy import deepcopy
from decimal import Decimal
from typing import Literal, Callable, Any

import requests
from PyQt6.QtCore import QByteArray


class ApiException(Exception):
    def __init__(self, code: int, content: bytes):
        super().__init__()
        self.code, self.content = code, content

    def __str__(self):
        return f"{self.code}: {self.content.decode()}"

    def __repr__(self):
        return f"ApiException({self.code}, {str(self.content)})"


def cache_images(func: Callable[[Any], Any]):
    cache = dict()

    def wrapper(*args, **kwargs):
        nonlocal cache
        key = args, tuple(kwargs.items())
        print(key)
        already = cache.get(key)
        if already is not None:
            return already
        else:
            result = func(*args, **kwargs)
            cache[key] = result

            keys = cache.keys()
            if len(keys) > 100:
                del cache[tuple(keys)[0]]

            return result

    return deepcopy(wrapper)


def to_api_spn(spn: Decimal) -> str:
    spn = round(spn, 4).to_eng_string()
    return f"{spn},{spn}"


def to_api_ll(lat: Decimal, lon: Decimal) -> str:
    lat = round(lat, 6).to_eng_string()
    lon = round(lon, 6).to_eng_string()
    return f"{lon},{lat}"


@cache_images
def get_image(apikey: str, ll: str, spn: str, theme: Literal["light", "dark"]) -> QByteArray:
    url = "https://static-maps.yandex.ru/v1"
    params = {
        "apikey": apikey,
        "ll": ll,
        "spn": spn,
        "theme": theme
    }
    resp = requests.get(url, params)
    if resp.status_code != 200:
        raise ApiException(resp.status_code, resp.content)

    return QByteArray(resp.content)
