from PySide6 import QtGui
from PySide6.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QListWidget,
    QListWidgetItem,
)
from PySide6 import QtGui
from PySide6.QtCore import Qt

from .widget import Widget


class SideBar(Widget):

    def __init__(
        self, parent,
        f: Qt.WindowType = Qt.WindowType.Widget,
        name: str = "",
        data: dict = None,
        style: str = None,
    ) -> None:
        super().__init__(parent, f, name=name, data=data, style=style)

    def setup_ui(self):
        self.layout = QVBoxLayout(self)

        self.view = QListWidget(self)
        # 禁止滚动条
        self.view.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # 选项之间的间隔
        self.view.setSpacing(5)

        # 去除边框
        self.view.setFrameShape(QListWidget.Shape.NoFrame)

        # 允许多选
        self.view.setSelectionMode(QListWidget.SelectionMode.MultiSelection)

        self.items = []
        for website in self.data:
            item = QListWidgetItem(website, self.view)

            # 设置字体大小
            item.setFont(QtGui.QFont(
                "Roboto, Arial, sans-serif", 12, QtGui.QFont.Bold))

            # 设置居中
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.items.append(item)

        self.layout.addWidget(self.view)

        self.check_btn = QPushButton("Enable All")
        self.layout.addWidget(self.check_btn)

        self.layout.setSpacing(0)

        if self.style:
            self.setStyleSheet(self.style)
