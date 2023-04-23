import requests
from typing import Set
from bs4 import BeautifulSoup

from .engine import Engine
from ..meta import Meta


class SciHub(Engine):
    """Sci-Hub 搜索引擎."""

    api = 'https://sci-hub.ru'

    name = "Sci-Hub"

    @classmethod
    def is_date(cls, date: str):
        """判断是否为日期."""
        if not date:
            return False
        return date.strip('()').isdigit()

    @classmethod
    def _parse_citation(cls, citation: str):
        """解析引文.
        单个引文格式如：
            'Muehlich, M., Friedrich, D., & Aach, T. (2012). '
            'Design and Implementation of Multisteerable Matched Filters. '
            'IEEE Transactions on Pattern Analysis and Machine Intelligence, 34(2), 279–291. '
            'doi:10.1109/tpami.2011.143\xa0'
        """
        authors = []

        is_date, date, date_id = False, None, -1

        segments = citation.split('.')
        for idx, segment in enumerate(segments):
            segment = segment.strip()
            if "doi:" in segment:
                break

            is_date = is_date or cls.is_date(segment)
            if not is_date:
                segment = segment.strip('& ')
                authors.append(segment)
                continue
            elif is_date and not date:
                date = segment.strip('()')
                date_id = idx
                continue
            elif is_date and date and idx == date_id + 1:
                title = segment

        doi = '.'.join(segments[idx:]).replace('doi:', '').strip()
        return authors, date, title, doi

    @classmethod
    def _parse_pdf_link(cls, pdf_link: str) -> str:
        """解析 PDF 链接."""
        if not pdf_link:
            return ''
        link = cls.to_http(pdf_link)
        valid_index = link.find('.pdf')
        if valid_index == -1:
            return ''
        return link[:valid_index + 4]

    @classmethod
    def search(cls, keyword: str) -> Set[Meta]:
        cls.log(f'Search "{keyword}" from {cls.api}.')

        response = requests.post(
            cls.api, data={'request': keyword},
            headers=cls.headers, timeout=5,
        )

        results = set()
        try:
            response.raise_for_status()

            page_text = response.text
            cls.log(page_text)

            soup = BeautifulSoup(page_text, 'html.parser')
            citation = soup.find('div', id="citation")
            if citation is None:
                return set()
            citation = citation.text

            pdf = soup.find("embed", type="application/pdf")
            if pdf is None:
                return set()
            pdf_link = cls._parse_pdf_link(pdf.get('src'))

            authors, date, title, doi = cls._parse_citation(citation)
            results.add(Meta(
                doi=doi,
                date=date,
                title=title,
                authors=authors,
                download_link=pdf_link,
            ))
        except requests.exceptions.HTTPError:
            cls.log(f'HTTPError: {response.status_code} - {response.reason}')

        cls.log(f'Result: {results}')
        return results
