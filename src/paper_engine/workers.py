from PySide6.QtCore import QThread, Signal

from .engine import MetaEngine


class SearchThread(QThread):

    finished = Signal(set)

    def __init__(
        self,
        parent = None,
        keywords: str = None,
    ) -> None:
        super().__init__(parent)
        self.keywords = keywords or ''

    def run(self) -> None:
        result = MetaEngine.search(self.keywords)
        self.finished.emit(result)

    def set_keywords(self, keywords: str) -> None:
        self.keywords = keywords
