"""System information collector."""

from __future__ import annotations

import os
import socket
import platform
from datetime import datetime
from typing import Dict


def get_system_info() -> Dict[str, str]:
    """Gather basic system metadata.

    Returns:
        A dictionary with hostname, os, date, username and computer_name.
        On failure an "error" key is included with the exception message.
    """
    try:
        return {
            "hostname": socket.gethostname(),
            "os": f"{platform.system()} {platform.release()}",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "username": os.getlogin(),
            "computer_name": platform.node(),
        }
    except Exception as exc:  # pragma: no cover
        return {
            "error": str(exc),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
