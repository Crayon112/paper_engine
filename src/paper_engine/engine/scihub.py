import re
import requests

from .engine import Engine
from ..meta import Meta


class SciHub(Engine):
    """Sci-Hub 搜索引擎."""

    api = 'https://sci-hub.ru'

    name = "Sci-Hub"

    @classmethod
    def search(cls, meta: Meta):
        response = requests.post(
            cls.api, data={'request': meta.title or meta.doi},
            headers=cls.headers, timeout=5,
        )
        cls.log(f'Search "{meta.title}" from {response.url}.')

        results = set()
        try:
            response.raise_for_status()

            text = response.text
            pattern = re.compile(r'//.+?\.pdf')

            for match in pattern.finditer(text):
                link = match.group(0)
                link = cls.to_http(link)
                results.add(link)
        except requests.exceptions.HTTPError:
            cls.log(f'HTTPError: {response.status_code} - {response.reason}')

        cls.log(f'Result: {results}')
        return results
