from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget


class Widget(QWidget):

    def __init__(
        self, parent,
        f: Qt.WindowType = Qt.WindowType.Widget,
        name: str = "",
        data: dict = None,
        style: str = None,
    ) -> None:
        super().__init__(parent, f)
        self.setObjectName(name)
        self.data = data or {}
        if style is not None:
            self.style = self.load_style(style)
        else:
            self.style = ''
        self.setup_ui()

    def setup_ui(self):
        pass

    def load_style(self, style: str):
        with open(style, "r") as f:
            return f.read()
