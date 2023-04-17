from PySide6.QtWidgets import (
    QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView
)


class ShowWidget(QTableWidget):
    """结果展示组件.

    Args:
        parent (QWidget): 父组件.
        name (str, optional): 组件名称. Defaults to "".
        data (dict, optional): 组件数据. Defaults to None.
        style (str, optional): 组件样式. Defaults to None.

    Note:
        data 应当至少包含以下字段: res, headers.
        例如：
        data = {
            "res": [
                ("https://www.google.com", "test", "test"),
                ("https://www.baidu.com", "test", "test"),
                ("https://www.bing.com", "test", "test"),
                ("https://www.yahoo.com", "test", "test"),
                ("https://www.yandex.com", "test", "test"),
            ],
            "headers": ["Website", "Resource", "Status"],
        }

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
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        for i, item in enumerate(self.data.get("result", [])):
            self.insertRow(i)

            if isinstance(item, (list, tuple)):
                for j, text in enumerate(item):
                    item = QTableWidgetItem(text)
                    self.setItem(i, j, item)
            else:
                item = QTableWidgetItem(item)
                self.setItem(i, 0, item)

        # 禁止编辑
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # 多选
        self.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

        # 不显示网格
        self.setShowGrid(False)

        if self.style:
            self.setStyleSheet(self.style)

    def update_data(self, data: dict):
        self.data = data
        self.setup_ui()
