import re

from .meta import Meta


def is_doi(text: str):
    return bool(re.match(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", text, re.I))


def build_meta(text: str):
    if is_doi(text):
        return Meta.from_doi(text)
    return Meta.from_title(text)
