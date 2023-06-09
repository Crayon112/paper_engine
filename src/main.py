import sys
from paper_engine.app import PaperEngine
from PySide6.QtWidgets import QApplication

import logging
logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PaperEngine()
    window.show()
    sys.exit(app.exec())
