"""Alternative entry point (``python -m src``)."""

from __future__ import annotations

import sys


def main() -> int:
    """Launch the CraftRise Stealer GUI."""
    from PyQt5.QtWidgets import QApplication
    from src.gui.main_window import MainWindow

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
