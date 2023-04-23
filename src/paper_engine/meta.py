from typing import List


class Meta(dict):
    """元数据."""

    def __init__(
        self,
        title: str = None,
        authors: List[str] = None,
        date: str = None,
        keywords: List[str] = None,
        doi: str = None,
        download_link: str = None,
        *args,
        **kwargs,
    ):
        self.title = title or ""
        self.authors = authors or []
        self.date = date
        self.keywords = keywords or []
        self.doi = doi
        self.download_link = download_link
        super().__init__(*args, **kwargs)

    @property
    def has_author(self):
        if self.authors is None:
            return False
        return len(self.authors) > 0

    @property
    def has_doi(self):
        if self.doi is None:
            return False
        return len(self.doi) > 0

    @classmethod
    def from_doi(cls, doi: str):
        return cls(doi=doi)

    @classmethod
    def from_title(cls, title: str):
        return cls(title=title)

    def __hash__(self) -> int:
        return hash(
            str(self.doi) + '-' +
            str(self.authors) + '-' +
            str(self.date) + '-' +
            str(self.title) + '-' +
            str(self.download_link)
        )

    def __str__(self) -> str:
        return f'{self.title or "title"}-{self.authors or "author"}-' + \
            f'{self.date or "YYYY-MM-DD"}-{self.doi or "doi"}-' + \
            f'{self.download_link or ""}'

    __repr__ = __str__
