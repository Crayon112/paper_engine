from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QLineEdit,
)

from .widget import Widget


class SearchWidget(Widget):

    def __init__(
        self, parent,
        f: Qt.WindowType = Qt.WindowType.Widget,
        name: str = "",
        data: dict = None,
        style: str = None,
    ) -> None:
        super().__init__(parent, f, name=name, data=data, style=style)

    def setup_ui(self):
        self.layout = QHBoxLayout(self)

        self.search_box = QLineEdit(self)
        self.search_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.search_box)

        self.search_btn = QPushButton("Search", self)
        self.layout.addWidget(self.search_btn)

        if self.style:
            self.setStyleSheet(self.style)
