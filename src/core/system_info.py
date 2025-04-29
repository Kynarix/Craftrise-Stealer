import os
import socket
import platform
from datetime import datetime

def get_system_info():
    try:
        return {
            "hostname": socket.gethostname(),
            "os": platform.system() + " " + platform.release(),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "username": os.getlogin(),
            "computer_name": platform.node()
        }
    except Exception as e:
        return {
            "error": str(e),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        } 