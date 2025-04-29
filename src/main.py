import sys
import os
import subprocess
import pkg_resources
from PyQt5.QtWidgets import QApplication, QMessageBox

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.gui.main_window import MainWindow

def check_python_version():
    required_version = (3, 8)
    current_version = sys.version_info[:2]
    
    if current_version < required_version:
        QMessageBox.critical(None, "Hata ⚠️", 
                           f"Python sürümü çok eski!\nGerekli: {required_version[0]}.{required_version[1]}+\nMevcut: {current_version[0]}.{current_version[1]}")
        return False
    return True

def check_dependencies():
    try:
        requirements_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'requirements.txt')
        with open(requirements_path, 'r') as f:
            required = {line.split('==')[0].lower() for line in f if line.strip()}
        
        installed = {pkg.key for pkg in pkg_resources.working_set}
        missing = required - installed
        
        if missing:
            QMessageBox.information(None, "Bilgi ℹ️", 
                                  "Eksik kütüphaneler yükleniyor...\nBu işlem biraz zaman alabilir.")
            
            for package in missing:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            
            QMessageBox.information(None, "Başarılı ✅", 
                                  "Tüm kütüphaneler başarıyla yüklendi!")
        
        return True
    except Exception as e:
        QMessageBox.critical(None, "Hata ⚠️", 
                           f"Kütüphane kontrolü sırasında hata oluştu:\n{str(e)}")
        return False

def main():
    if not check_python_version():
        sys.exit(1)
        
    if not check_dependencies():
        sys.exit(1)
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 