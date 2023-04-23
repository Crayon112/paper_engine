from PySide6.QtWidgets import (
    QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView
)
from PySide6.QtCore import Qt


class ShowWidget(QTableWidget):
    """结果展示组件.

    Args:
        parent (QWidget): 父组件.
        name (str, optional): 组件名称. Defaults to "".
        data (dict, optional): 组件数据. Defaults to None.
        style (str, optional): 组件样式. Defaults to None.
    """

    def __init__(
        self, parent,
        name: str = "",
        data: dict = None,
        style: str = None,
    ) -> None:
        super(ShowWidget, self).__init__(parent)
        self.name = name
        self.setObjectName(name)
        self.data = data or {}
        self.style = self.load_style(style)
        self.setup_ui()

    def load_style(self, style: str):
        with open(style, "r") as f:
            return f.read()

    def setup_ui(self):
        self.clear()

        self.setMinimumWidth(self.width())
        # 表头居中对齐
        headers = self.data.get("headers", [])
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)

        # 隐藏行头
        self.verticalHeader().setVisible(False)

        # 设置列宽
        header = self.horizontalHeader()

        # 交互式调整列宽
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        for i, item in enumerate(self.data.get("result", [])):
            self.insertRow(i)

            if isinstance(item, (list, tuple)):
                for j, text in enumerate(item):
                    text = str(text)
                    item = QTableWidgetItem(text)
                    if j == 0:
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    else:
                        item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
                    self.setItem(i, j, item)
            else:
                item = str(item)
                item = QTableWidgetItem(item)
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
                self.setItem(i, 0, item)

        # 禁止编辑
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # 多选行
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

        # 不显示网格
        self.setShowGrid(False)

        if self.style:
            self.setStyleSheet(self.style)

    def update_data(self, data: dict):
        self.data = data
        self.setup_ui()
