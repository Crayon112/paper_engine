from typing import List


class Meta(dict):
    """元数据."""

    def __init__(
        self,
        title: str = None,
        author: List[str] = None,
        date: str = None,
        keywords: List[str] = None,
        doi: str = None,
        *args,
        **kwargs,
    ):
        self.title = title or ""
        self.author = author or []
        self.date = date
        self.keywords = keywords or []
        self.doi = doi
        super().__init__(*args, **kwargs)

    @property
    def has_author(self):
        if self.author is None:
            return False
        return len(self.author) > 0

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
