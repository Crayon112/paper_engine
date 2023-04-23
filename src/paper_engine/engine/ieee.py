import requests
from typing import Set


from .engine import Engine
from ..meta import Meta


class IEEE(Engine):

    name = "IEEE"

    host = "https://ieeexplore.ieee.org"

    api = "https://ieeexplore.ieee.org/rest/search"

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/json',
        'Origin': 'https://ieeexplore.ieee.org',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    @classmethod
    def _get_pdf(cls, link: str) -> str:
        if not link:
            return ''
        if link.startswith('http'):
            return link
        return cls.host.strip('/') + '/' + link.strip('/')

    @classmethod
    def search(cls, keyword: str, max_number: int = 3) -> Set[Meta]:
        cls.log(f'Searching {keyword} for {cls.host}')

        response = requests.post(
            cls.api,
            json={
                "queryText": keyword,
                "highlight": True,
                "returnFacets": ["ALL"],
                "returnType": "SEARCH",
                'matchPubs': True,
            },
            headers=cls.headers,
            timeout=10,
        )

        results = set()

        try:
            response.raise_for_status()
            resp_data = response.json()
            records = resp_data.get('records', [])
            if not records:
                return set()

            for record in records[:max_number]:
                title = record.get("articleTitle", None)
                doi = record.get("doi", None)
                date = record.get("publicationDate", None)

                download_link = record.get("pdfLink", None)
                download_link = cls._get_pdf(download_link)

                authors = record.get("authors", [])
                authors = [author.get("preferredName", None) for author in authors]
                authors = [author for author in authors if author is not None]

                results.add(Meta(
                    title=title,
                    authors=authors,
                    date=date,
                    doi=doi,
                    download_link=cls._get_pdf(download_link),
                ))
        except requests.exceptions.HTTPError:
            cls.log(f'HTTPError: {response.status_code} - {response.reason}')
        except Exception as e:
            cls.log(f'Exception: {e}')

        cls.log(f'Result: {results}')
        return results
