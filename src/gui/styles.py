"""Centralized color palette and QSS stylesheet generator."""

from __future__ import annotations


class Colors:
    """Aspire Leaders / PheXora inspired dark palette.

    Deep blacks with blood-red accents and silver typography.
    """

    # ── Base ──
    BACKGROUND = "#050505"
    SURFACE = "#0c0c0c"
    SURFACE_HOVER = "#141414"
    SURFACE_LIGHT = "#1a1a1a"
    BORDER = "#2a2a2a"
    BORDER_FOCUS = "#5c0000"

    # ── Primary accent (blood red) ──
    PRIMARY = "#d90429"
    PRIMARY_HOVER = "#ff0a1a"
    PRIMARY_ACTIVE = "#a8001c"
    PRIMARY_GLOW = "#4a0000"

    # ── Typography ──
    TEXT = "#e8e8e8"
    TEXT_SECONDARY = "#a0a0a0"
    TEXT_MUTED = "#666666"

    # ── Feedback ──
    SUCCESS = "#00d084"
    ERROR = "#ff3333"
    WARNING = "#ff9500"
    INFO = "#3b82f6"

    # ── Inline checkbox SVG (white check on red) ──
    CHECK_SVG = (
        "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmci"
        "IHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjZmFmYWZhIiBzdHJva2Utd2lk"
        "dGg9IjMiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCI+PHBvbHls"
        "aW5lIHBvaW50cz0iMjAgNiA5IDE3IDQgMTIiLz48L3N2Zz4="
    )


def get_stylesheet(colors: Colors) -> str:
    """Generate the application-wide QSS stylesheet.

    Args:
        colors: An instance of :class:`Colors`.

    Returns:
        A complete QSS string for PyQt5.
    """
    return f"""
        /* ── Global ── */
        QMainWindow {{
            background-color: {colors.BACKGROUND};
        }}
        QWidget {{
            background-color: {colors.BACKGROUND};
            color: {colors.TEXT};
            font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
        }}

        /* ── Typography ── */
        QLabel {{
            color: {colors.TEXT};
            font-size: 14px;
            background: transparent;
        }}
        QLabel#TitleLabel {{
            font-size: 34px;
            font-weight: 700;
            color: {colors.TEXT};
            padding-bottom: 4px;
            letter-spacing: 1px;
        }}
        QLabel#SubtitleLabel {{
            font-size: 13px;
            color: {colors.TEXT_SECONDARY};
            background: transparent;
        }}
        QLabel#SectionLabel {{
            font-size: 11px;
            font-weight: 700;
            color: {colors.PRIMARY};
            text-transform: uppercase;
            letter-spacing: 1.2px;
            padding-bottom: 6px;
        }}
        QLabel#FooterLabel {{
            font-size: 12px;
            color: {colors.TEXT_MUTED};
            background: transparent;
        }}

        /* ── Cards (QFrame) ── */
        QFrame#Card {{
            background-color: {colors.SURFACE};
            border: 1px solid {colors.BORDER};
            border-radius: 14px;
        }}

        /* ── Inputs ── */
        QLineEdit {{
            padding: 12px 14px;
            border: 1px solid {colors.BORDER};
            border-radius: 10px;
            background-color: {colors.SURFACE};
            color: {colors.TEXT};
            font-size: 14px;
            selection-background-color: {colors.PRIMARY};
            selection-color: #ffffff;
        }}
        QLineEdit:focus {{
            border: 1.5px solid {colors.PRIMARY};
            background-color: {colors.SURFACE_HOVER};
        }}
        QLineEdit::placeholder {{
            color: {colors.TEXT_MUTED};
        }}

        /* ── Buttons ── */
        QPushButton {{
            padding: 10px 24px;
            background-color: {colors.PRIMARY};
            color: #ffffff;
            border: none;
            border-radius: 10px;
            font-size: 14px;
            font-weight: 700;
            min-height: 42px;
            letter-spacing: 0.4px;
        }}
        QPushButton:hover {{
            background-color: {colors.PRIMARY_HOVER};
        }}
        QPushButton:pressed {{
            background-color: {colors.PRIMARY_ACTIVE};
        }}
        QPushButton:disabled {{
            background-color: {colors.SURFACE_LIGHT};
            color: {colors.TEXT_MUTED};
        }}
        QPushButton#DangerButton {{
            background-color: {colors.ERROR};
            color: #ffffff;
        }}
        QPushButton#DangerButton:hover {{
            background-color: #ff6666;
        }}

        /* ── Log Console ── */
        QTextEdit {{
            background-color: {colors.SURFACE};
            color: {colors.TEXT};
            border: 1px solid {colors.BORDER};
            border-radius: 10px;
            font-size: 13px;
            font-family: "Consolas", "Monaco", "Courier New", monospace;
            padding: 10px;
            selection-background-color: {colors.PRIMARY};
            selection-color: #ffffff;
        }}
        QTextEdit:focus {{
            border: 1.5px solid {colors.PRIMARY};
        }}

        /* ── Progress ── */
        QProgressBar {{
            border: none;
            border-radius: 4px;
            text-align: center;
            background-color: {colors.SURFACE};
            color: transparent;
            max-height: 6px;
        }}
        QProgressBar::chunk {{
            background-color: {colors.PRIMARY};
            border-radius: 4px;
        }}

        /* ── Checkbox ── */
        QCheckBox {{
            color: {colors.TEXT};
            font-size: 14px;
            spacing: 10px;
            background: transparent;
        }}
        QCheckBox::indicator {{
            width: 22px;
            height: 22px;
            border: 2px solid {colors.BORDER};
            border-radius: 6px;
            background-color: {colors.SURFACE};
        }}
        QCheckBox::indicator:hover {{
            border-color: {colors.PRIMARY};
        }}
        QCheckBox::indicator:checked {{
            background-color: {colors.PRIMARY};
            border-color: {colors.PRIMARY};
            image: url({colors.CHECK_SVG});
        }}

        /* ── Scrollbars ── */
        QScrollBar:vertical {{
            background: transparent;
            width: 8px;
            border-radius: 4px;
        }}
        QScrollBar::handle:vertical {{
            background: {colors.BORDER};
            border-radius: 4px;
            min-height: 30px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {colors.PRIMARY};
        }}
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {{
            height: 0px;
        }}

        /* ── MessageBox ── */
        QMessageBox {{
            background-color: {colors.BACKGROUND};
        }}
        QMessageBox QLabel {{
            color: {colors.TEXT};
            font-size: 13px;
        }}
        QMessageBox QPushButton {{
            padding: 8px 20px;
            background-color: {colors.PRIMARY};
            color: #ffffff;
            border: none;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 700;
            min-width: 80px;
            min-height: 32px;
        }}
    """
