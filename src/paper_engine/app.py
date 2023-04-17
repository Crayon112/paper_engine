import os
import logging
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QProgressBar,
)

from .components import (
    Widget, SideBar, SearchWidget, ShowWidget,
)
from .downloader import download
from .engine import MetaEngine
from .utils import build_meta


logger = logging.getLogger("APP")


curdir = os.path.dirname(os.path.abspath(__file__))


QSS = {
    "PaperEngine": f"{curdir}/qss/paperengine.css",
    "SideBar": f"{curdir}/qss/sidebar.css",
    "Show": f"{curdir}/qss/show.css",
    "Search": f"{curdir}/qss/search.css",
    "MainAPP": f"{curdir}/qss/mainapp.css",
}


class MainApp(QWidget):

    def __init__(
        self, parent,
        f: Qt.WindowType = Qt.WindowType.Widget,
        name: str = "MainApp",
        data: dict = None,
        style: str = None,
    ) -> None:
        super().__init__(parent, f)
        self.name = name
        self.setObjectName(name)
        self.data = data or {}
        self.style = self.load_style(style)
        self.setup_ui()

    def load_style(self, style: str):
        with open(style, "r") as f:
            return f.read()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)

        self.search = SearchWidget(
            self,
            name="Search",
            style=QSS["Search"],
        )
        self.search.search_btn.clicked.connect(self.search_btn_clicked)
        self.layout.addWidget(self.search)

        self.showres = ShowWidget(
            self,
            name="Show",
            style=QSS["Show"],
        )
        self.layout.addWidget(self.showres, stretch=1)

        self.bottom_layout = QHBoxLayout()

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.bottom_layout.addWidget(self.progress, stretch=3)

        self.download = QPushButton("Download")
        self.download.clicked.connect(self.download_btn_clicked)
        self.bottom_layout.addWidget(self.download, stretch=1)

        self.layout.addLayout(self.bottom_layout)

        if self.style:
            self.setStyleSheet(self.style)

    def download_btn_clicked(self):
        selected_links = [
            item.text()
            for item in self.showres.selectedItems()
        ]
        if not selected_links:
            return
        directory = QFileDialog.getExistingDirectory(self)

        self.progress.setValue(0)

        for i, url in enumerate(selected_links):
            download(url, directory)
            self.progress.setValue(i * 100 // len(selected_links))

        self.progress.setValue(100)

    def search_btn_clicked(self):
        keyword = self.search.search_box.text()
        meta = build_meta(keyword)
        result = list(MetaEngine.search(meta))
        data = {
            "headers": ["Result"],
            "result": result,
        }
        self.showres.update_data(data)


class PaperEngine(QMainWindow):

    def __init__(
        self,
        name="PaperEngine",
        width: int = 1100,
        height: int = 650,
        style: str = QSS["PaperEngine"],
    ):
        super().__init__()
        self.name = name
        self.setObjectName(name)
        self.width = width
        self.height = height
        self.style = self.load_style(style)
        self.setup_ui()

    def load_style(self, style: str):
        with open(style, "r") as f:
            return f.read()

    def setup_ui(self):
        self.setWindowTitle(self.name)
        self.resize(self.width, self.height)
        self._app_init()

    def _app_init(self):
        self.app = Widget(self)
        self.setCentralWidget(self.app)

        self.layout = QHBoxLayout(self.app)

        # 侧边栏
        self.side_bar = SideBar(
            self,
            name="SideBar",
            style=QSS["SideBar"],
            data=MetaEngine.registry.copy(),
        )
        self.side_bar.check_btn.clicked.connect(self.enable_all_engines)
        self.side_bar.view.itemSelectionChanged.connect(self.item_select)
        self.layout.addWidget(self.side_bar, stretch=1)

        # 主程序
        self.main = MainApp(
            self,
            name="MainApp",
            style=QSS["MainAPP"],
        )
        self.layout.addWidget(self.main, stretch=3)

        if self.style:
            self.setStyleSheet(self.style)

        self._load()

    def _load(self):
        self.item_select()

    def enable_all_engines(self):
        self.side_bar.check_btn.clicked.disconnect()
        self.side_bar.check_btn.clicked.connect(self.disable_all_engines)
        for i in range(self.side_bar.view.count()):
            item = self.side_bar.view.item(i)
            item.setSelected(True)
        self.side_bar.check_btn.setText("Disable All")

    def disable_all_engines(self):
        self.side_bar.check_btn.clicked.disconnect()
        self.side_bar.check_btn.clicked.connect(self.enable_all_engines)
        for i in range(self.side_bar.view.count()):
            item = self.side_bar.view.item(i)
            item.setSelected(False)
        self.side_bar.check_btn.setText("Enable All")

    def item_select(self):
        names = [item.text() for item in self.side_bar.items]
        MetaEngine.add_exclude(*names)
        for item in self.side_bar.view.selectedItems():
            name = item.text()
            if name in MetaEngine.exclude:
                MetaEngine.exclude.remove(name)
        logging.info(f"Excluded Engines -> {MetaEngine.exclude}")
