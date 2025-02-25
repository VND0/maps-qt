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


def to_api_ll(p1: float, p2: float) -> str:
    return f"{p2},{p1}"


def to_api_spn(spn: float) -> str:
    return f"{spn},{spn}"


def get_image(apikey: str, ll: str, spn: str) -> QByteArray:
    url = "https://static-maps.yandex.ru/v1"
    params = {
        "apikey": apikey,
        "ll": ll,
        "spn": spn
    }
    resp = requests.get(url, params)
    if resp.status_code != 200:
        raise ApiException(resp.status_code, resp.content)

    return QByteArray(resp.content)
