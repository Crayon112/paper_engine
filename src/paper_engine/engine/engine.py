from typing import Set
from ..meta import Meta

import logging


class MetaEngine(type):
    """搜索引擎元类.

    registry: 用于存储所有搜索引擎的字典.

    search: 搜索方法, 用于从所有搜索引擎获取搜索结果.

    """

    registry = {}

    exclude = {"Engine"}

    def __new__(cls, name, bases, dct):
        new_cls = super().__new__(cls, name, bases, dct)
        if new_cls.__name__ in cls.exclude:
            return new_cls

        if not hasattr(new_cls, "name"):
            raise NotImplementedError("Engine must have a name.")
        cls.registry[new_cls.name] = new_cls

        return new_cls

    @classmethod
    def is_excluded(cls, engine):
        return (
            engine.__name__ in cls.exclude
            or
            engine.name in cls.exclude
        )

    @classmethod
    def get(cls, name) -> "Engine":
        return cls.registry[name]

    @classmethod
    def search(cls, keyword: str) -> Set[Meta]:
        result = set()
        for engine in cls.registry.values():
            if cls.is_excluded(engine):
                continue
            result = result.union(engine.search(keyword))
        return result

    @classmethod
    def names(cls) -> Set[str]:
        res = set()
        for cls_ in cls.registry.values():
            if cls.is_excluded(cls_):
                continue
            res.add(cls_.name)
        return res

    @classmethod
    def engines(cls) -> Set["Engine"]:
        res = set()
        for cls_ in cls.registry.values():
            if cls.is_excluded(cls_):
                continue
            res.add(cls_)
        return res

    @classmethod
    def add_exclude(cls, *names):
        names = set(names)
        cls.exclude = cls.exclude.union(names)


class Engine(metaclass=MetaEngine):
    """搜索引擎基类."""

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                    " AppleWebKit/537.36 (KHTML, like Gecko)"
                    " Chrome/87.0.4280.88 Safari/537.36",
    }

    @classmethod
    def log(cls, message: str, level: int = logging.INFO):
        logger = logging.getLogger(cls.__name__)
        logger.log(level, message)

    @staticmethod
    def to_http(url, ssl: bool = False):
        remove_http = url.replace("http://", "").replace("https://", "").strip("/\\")

        if not ssl:
            return "http://" + remove_http
        else:
            return "https://" + remove_http

    @classmethod
    def search(cls, keyword: str) -> Set[Meta]:  # noqa: E501
        return set()
