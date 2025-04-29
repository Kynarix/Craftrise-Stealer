class Colors:
    BACKGROUND = '#0f0f0f'
    SURFACE = '#1e1e1e'
    SURFACE_LIGHT = '#2d2d2d'
    PRIMARY = '#4f46e5'
    PRIMARY_HOVER = '#4338ca'
    TEXT = '#ffffff'
    TEXT_SECONDARY = '#94a3b8'
    BORDER = '#2e2e2e'
    SUCCESS = '#22c55e'
    ERROR = '#ef4444'
    WARNING = '#f59e0b'

def get_stylesheet(colors):
    return f"""
        QMainWindow {{
            background-color: {colors.BACKGROUND};
        }}
        QLabel {{
            color: {colors.TEXT};
            font-size: 14px;
        }}
        QLineEdit {{
            padding: 12px;
            border: 1px solid {colors.BORDER};
            border-radius: 6px;
            background-color: {colors.SURFACE};
            color: {colors.TEXT};
            font-size: 13px;
            selection-background-color: {colors.PRIMARY};
        }}
        QLineEdit:focus {{
            border: 2px solid {colors.PRIMARY};
            background-color: {colors.SURFACE_LIGHT};
        }}
        QPushButton {{
            padding: 8px 16px;
            background-color: {colors.PRIMARY};
            color: {colors.TEXT};
            border: none;
            border-radius: 4px;
            font-size: 13px;
            font-weight: 600;
            min-height: 32px;
            max-height: 32px;
        }}
        QPushButton:hover {{
            background-color: {colors.PRIMARY_HOVER};
        }}
        QPushButton:pressed {{
            background-color: {colors.PRIMARY};
            padding-top: 9px;
        }}
        QPushButton:disabled {{
            background-color: {colors.SURFACE_LIGHT};
            color: {colors.TEXT_SECONDARY};
        }}
        QTextEdit {{
            background-color: {colors.SURFACE};
            color: {colors.TEXT};
            border: 1px solid {colors.BORDER};
            border-radius: 6px;
            font-size: 13px;
            padding: 8px;
            selection-background-color: {colors.PRIMARY};
        }}
        QProgressBar {{
            border: none;
            border-radius: 3px;
            text-align: center;
            background-color: {colors.SURFACE};
            color: {colors.TEXT};
            height: 6px;
        }}
        QProgressBar::chunk {{
            background-color: {colors.PRIMARY};
            border-radius: 3px;
        }}
        QCheckBox {{
            color: {colors.TEXT};
            font-size: 13px;
            spacing: 8px;
        }}
        QCheckBox::indicator {{
            width: 20px;
            height: 20px;
            border: 2px solid {colors.BORDER};
            border-radius: 4px;
            background-color: {colors.SURFACE};
        }}
        QCheckBox::indicator:hover {{
            border-color: {colors.PRIMARY};
        }}
        QCheckBox::indicator:checked {{
            background-color: {colors.PRIMARY};
            border: none;
            image: url(check.png);
        }}
        QFrame {{
            background-color: {colors.SURFACE};
            border: 1px solid {colors.BORDER};
            border-radius: 8px;
        }}
        QMessageBox {{
            background-color: {colors.BACKGROUND};
            color: {colors.TEXT};
        }}
        QMessageBox QLabel {{
            color: {colors.TEXT};
            font-size: 13px;
        }}
        QMessageBox QPushButton {{
            padding: 8px 16px;
            background-color: {colors.PRIMARY};
            color: {colors.TEXT};
            border: none;
            border-radius: 4px;
            font-size: 13px;
            font-weight: bold;
            min-width: 80px;
            min-height: 30px;
        }}
    """ 