import requests
from typing import Set

# from .engine import Engine
from ..meta import Meta


class BaiduXueShu:
    """百度学术搜索引擎."""

    api = "https://xueshu.baidu.com/s"

    name = "百度学术"

    @classmethod
    def search(cls, meta: Meta) -> Set[str]:
        response = requests.get(
            cls.api,
            params={
                "wd": meta.title,
            },
            headers=cls.headers,
            timeout=5,
        )
        cls.log(f'Search "{meta.title}" from {response.url}.')

        result = set()
        try:
            response.raise_for_status()
            text = response.text
            result.add(text)
        except requests.exceptions.HTTPError:
            cls.log(f'HTTPError: {response.status_code} - {response.reason}')

        cls.log(f'Result: {result}')
        return result
