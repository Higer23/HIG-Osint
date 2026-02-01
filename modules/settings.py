#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Settings Module - Ayarlar Modülü
"""

import os
import sys
import json
from pathlib import Path
from colorama import Fore, Style

class Colors:
    """Renk tanımlamaları"""
    HEADER = Fore.CYAN + Style.BRIGHT
    INFO = Fore.BLUE + Style.BRIGHT
    SUCCESS = Fore.GREEN + Style.BRIGHT
    WARNING = Fore.YELLOW + Style.BRIGHT
    ERROR = Fore.RED + Style.BRIGHT
    MENU = Fore.MAGENTA + Style.BRIGHT
    INPUT = Fore.WHITE + Style.BRIGHT
    RESET = Style.RESET_ALL

CONFIG_FILE = Path('config/settings.json')

DEFAULT_SETTINGS = {
    'general': {
        'language': 'tr',
        'auto_save': True,
        'show_banner': True,
        'clear_screen': True
    },
    'scanning': {
        'default_timeout': 5,
        'max_threads': 50,
        'verbose_mode': False,
        'save_logs': True
    },
    'api_keys': {
        'shodan': '',
        'virustotal': '',
        'hunter_io': '',
        'censys': '',
        'have_i_been_pwned': ''
    },
    'proxy': {
        'enabled': False,
        'http_proxy': '',
        'https_proxy': '',
        'socks_proxy': ''
    },
    'output': {
        'format': 'json',
        'directory': 'reports',
        'include_timestamp': True,
        'compress_reports': False
    },
    'security': {
        'verify_ssl': True,
        'user_agent': 'HIG-OSINT/3.0',
        'rate_limit': True
    }
}

def clear_screen():
    """Ekranı temizle"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Modül başlığını göster"""
    header = f"""{Colors.HEADER}
╔═══════════════════════════════════════════════════════════════════╗
║                        AYARLAR MODÜLÜ                            ║
║                       Settings Module                            ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(header)

def load_settings():
    """Ayarları yükle"""
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Varsayılan ayarları oluştur
            save_settings(DEFAULT_SETTINGS)
            return DEFAULT_SETTINGS
    except Exception as e:
        print(f"{Colors.ERROR}[-] Ayarlar yüklenemedi: {e}{Colors.RESET}")
        return DEFAULT_SETTINGS

def save_settings(settings):
    """Ayarları kaydet"""
    try:
        CONFIG_FILE.parent.mkdir(exist_ok=True)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
        print(f"{Colors.SUCCESS}[+] Ayarlar kaydedildi{Colors.RESET}")
        return True
    except Exception as e:
        print(f"{Colors.ERROR}[-] Ayarlar kaydedilemedi: {e}{Colors.RESET}")
        return False

def view_settings():
    """Mevcut ayarları görüntüle"""
    print(f"\n{Colors.MENU}=== Mevcut Ayarlar ==={Colors.RESET}")
    
    settings = load_settings()
    
    print(f"\n{Colors.INFO}[Genel Ayarlar]{Colors.RESET}")
    for key, value in settings['general'].items():
        print(f"  - {key}: {value}")
    
    print(f"\n{Colors.INFO}[Tarama Ayarları]{Colors.RESET}")
    for key, value in settings['scanning'].items():
        print(f"  - {key}: {value}")
    
    print(f"\n{Colors.INFO}[API Anahtarları]{Colors.RESET}")
    for key, value in settings['api_keys'].items():
        masked_value = '*' * len(value) if value else 'Ayarlanmamış'
        print(f"  - {key}: {masked_value}")
    
    print(f"\n{Colors.INFO}[Proxy Ayarları]{Colors.RESET}")
    for key, value in settings['proxy'].items():
        print(f"  - {key}: {value}")
    
    print(f"\n{Colors.INFO}[Çıktı Ayarları]{Colors.RESET}")
    for key, value in settings['output'].items():
        print(f"  - {key}: {value}")
    
    print(f"\n{Colors.INFO}[Güvenlik Ayarları]{Colors.RESET}")
    for key, value in settings['security'].items():
        print(f"  - {key}: {value}")

def edit_general_settings():
    """Genel ayarları düzenle"""
    settings = load_settings()
    
    print(f"\n{Colors.MENU}=== Genel Ayarlar ==={Colors.RESET}")
    
    language = input(f"\n{Colors.INPUT}Dil (tr/en) [{settings['general']['language']}]: {Colors.RESET}").strip()
    if language:
        settings['general']['language'] = language
    
    auto_save = input(f"{Colors.INPUT}Otomatik kayıt (True/False) [{settings['general']['auto_save']}]: {Colors.RESET}").strip()
    if auto_save:
        settings['general']['auto_save'] = auto_save.lower() == 'true'
    
    show_banner = input(f"{Colors.INPUT}Banner göster (True/False) [{settings['general']['show_banner']}]: {Colors.RESET}").strip()
    if show_banner:
        settings['general']['show_banner'] = show_banner.lower() == 'true'
    
    clear_screen_opt = input(f"{Colors.INPUT}Ekran temizle (True/False) [{settings['general']['clear_screen']}]: {Colors.RESET}").strip()
    if clear_screen_opt:
        settings['general']['clear_screen'] = clear_screen_opt.lower() == 'true'
    
    save_settings(settings)

def edit_scanning_settings():
    """Tarama ayarlarını düzenle"""
    settings = load_settings()
    
    print(f"\n{Colors.MENU}=== Tarama Ayarları ==={Colors.RESET}")
    
    timeout = input(f"\n{Colors.INPUT}Varsayılan timeout (saniye) [{settings['scanning']['default_timeout']}]: {Colors.RESET}").strip()
    if timeout and timeout.isdigit():
        settings['scanning']['default_timeout'] = int(timeout)
    
    threads = input(f"{Colors.INPUT}Maksimum thread sayısı [{settings['scanning']['max_threads']}]: {Colors.RESET}").strip()
    if threads and threads.isdigit():
        settings['scanning']['max_threads'] = int(threads)
    
    verbose = input(f"{Colors.INPUT}Detaylı mod (True/False) [{settings['scanning']['verbose_mode']}]: {Colors.RESET}").strip()
    if verbose:
        settings['scanning']['verbose_mode'] = verbose.lower() == 'true'
    
    logs = input(f"{Colors.INPUT}Log kaydet (True/False) [{settings['scanning']['save_logs']}]: {Colors.RESET}").strip()
    if logs:
        settings['scanning']['save_logs'] = logs.lower() == 'true'
    
    save_settings(settings)

def edit_api_keys():
    """API anahtarlarını düzenle"""
    settings = load_settings()
    
    print(f"\n{Colors.MENU}=== API Anahtarları ==={Colors.RESET}")
    print(f"{Colors.WARNING}[!] API anahtarları gizli tutulacaktır{Colors.RESET}\n")
    
    apis = [
        ('shodan', 'Shodan API Key'),
        ('virustotal', 'VirusTotal API Key'),
        ('hunter_io', 'Hunter.io API Key'),
        ('censys', 'Censys API Key'),
        ('have_i_been_pwned', 'Have I Been Pwned API Key')
    ]
    
    for api_key, api_name in apis:
        current = '*' * len(settings['api_keys'][api_key]) if settings['api_keys'][api_key] else 'Yok'
        new_key = input(f"{Colors.INPUT}{api_name} [{current}]: {Colors.RESET}").strip()
        if new_key:
            settings['api_keys'][api_key] = new_key
    
    save_settings(settings)

def edit_proxy_settings():
    """Proxy ayarlarını düzenle"""
    settings = load_settings()
    
    print(f"\n{Colors.MENU}=== Proxy Ayarları ==={Colors.RESET}")
    
    enabled = input(f"\n{Colors.INPUT}Proxy kullan (True/False) [{settings['proxy']['enabled']}]: {Colors.RESET}").strip()
    if enabled:
        settings['proxy']['enabled'] = enabled.lower() == 'true'
    
    if settings['proxy']['enabled']:
        http_proxy = input(f"{Colors.INPUT}HTTP Proxy: {Colors.RESET}").strip()
        if http_proxy:
            settings['proxy']['http_proxy'] = http_proxy
        
        https_proxy = input(f"{Colors.INPUT}HTTPS Proxy: {Colors.RESET}").strip()
        if https_proxy:
            settings['proxy']['https_proxy'] = https_proxy
        
        socks_proxy = input(f"{Colors.INPUT}SOCKS Proxy: {Colors.RESET}").strip()
        if socks_proxy:
            settings['proxy']['socks_proxy'] = socks_proxy
    
    save_settings(settings)

def edit_output_settings():
    """Çıktı ayarlarını düzenle"""
    settings = load_settings()
    
    print(f"\n{Colors.MENU}=== Çıktı Ayarları ==={Colors.RESET}")
    
    output_format = input(f"\n{Colors.INPUT}Çıktı formatı (json/xml/csv) [{settings['output']['format']}]: {Colors.RESET}").strip()
    if output_format:
        settings['output']['format'] = output_format
    
    directory = input(f"{Colors.INPUT}Çıktı dizini [{settings['output']['directory']}]: {Colors.RESET}").strip()
    if directory:
        settings['output']['directory'] = directory
    
    timestamp = input(f"{Colors.INPUT}Timestamp ekle (True/False) [{settings['output']['include_timestamp']}]: {Colors.RESET}").strip()
    if timestamp:
        settings['output']['include_timestamp'] = timestamp.lower() == 'true'
    
    compress = input(f"{Colors.INPUT}Raporları sıkıştır (True/False) [{settings['output']['compress_reports']}]: {Colors.RESET}").strip()
    if compress:
        settings['output']['compress_reports'] = compress.lower() == 'true'
    
    save_settings(settings)

def edit_security_settings():
    """Güvenlik ayarlarını düzenle"""
    settings = load_settings()
    
    print(f"\n{Colors.MENU}=== Güvenlik Ayarları ==={Colors.RESET}")
    
    verify_ssl = input(f"\n{Colors.INPUT}SSL doğrula (True/False) [{settings['security']['verify_ssl']}]: {Colors.RESET}").strip()
    if verify_ssl:
        settings['security']['verify_ssl'] = verify_ssl.lower() == 'true'
    
    user_agent = input(f"{Colors.INPUT}User Agent [{settings['security']['user_agent']}]: {Colors.RESET}").strip()
    if user_agent:
        settings['security']['user_agent'] = user_agent
    
    rate_limit = input(f"{Colors.INPUT}Rate limiting (True/False) [{settings['security']['rate_limit']}]: {Colors.RESET}").strip()
    if rate_limit:
        settings['security']['rate_limit'] = rate_limit.lower() == 'true'
    
    save_settings(settings)

def reset_settings():
    """Ayarları sıfırla"""
    print(f"\n{Colors.WARNING}[!] TÜM AYARLAR VARSAYILAN DEĞERLERİNE SIFIRLANACAK!{Colors.RESET}")
    confirm = input(f"{Colors.INPUT}Emin misiniz? (E/H): {Colors.RESET}").strip().upper()
    
    if confirm in ['E', 'Y', 'EVET', 'YES']:
        save_settings(DEFAULT_SETTINGS)
        print(f"{Colors.SUCCESS}[+] Ayarlar sıfırlandı{Colors.RESET}")
    else:
        print(f"{Colors.INFO}[*] İşlem iptal edildi{Colors.RESET}")

def export_settings():
    """Ayarları dışa aktar"""
    settings = load_settings()
    
    filename = input(f"\n{Colors.INPUT}Dışa aktarma dosya adı (örn: backup.json): {Colors.RESET}").strip()
    if filename:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
            print(f"{Colors.SUCCESS}[+] Ayarlar dışa aktarıldı: {filename}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.ERROR}[-] Dışa aktarma hatası: {e}{Colors.RESET}")

def import_settings():
    """Ayarları içe aktar"""
    filename = input(f"\n{Colors.INPUT}İçe aktarma dosya adı: {Colors.RESET}").strip()
    
    if filename and os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            save_settings(settings)
            print(f"{Colors.SUCCESS}[+] Ayarlar içe aktarıldı{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.ERROR}[-] İçe aktarma hatası: {e}{Colors.RESET}")
    else:
        print(f"{Colors.ERROR}[-] Dosya bulunamadı{Colors.RESET}")

def settings_menu():
    """Ayarlar menüsü"""
    while True:
        clear_screen()
        print_header()
        
        menu = f"""{Colors.MENU}
╔═══════════════════════════════════════════════════════════════╗
║                      AYARLAR MENÜSÜ                          ║
╚═══════════════════════════════════════════════════════════════╝

  {Colors.INPUT}[1]{Colors.RESET} 👁️  Ayarları Görüntüle
  {Colors.INPUT}[2]{Colors.RESET} ⚙️  Genel Ayarlar
  {Colors.INPUT}[3]{Colors.RESET} 🔍 Tarama Ayarları
  {Colors.INPUT}[4]{Colors.RESET} 🔑 API Anahtarları
  {Colors.INPUT}[5]{Colors.RESET} 🌐 Proxy Ayarları
  {Colors.INPUT}[6]{Colors.RESET} 📁 Çıktı Ayarları
  {Colors.INPUT}[7]{Colors.RESET} 🔒 Güvenlik Ayarları
  {Colors.INPUT}[8]{Colors.RESET} 🔄 Ayarları Sıfırla
  {Colors.INPUT}[9]{Colors.RESET} 📤 Ayarları Dışa Aktar
  {Colors.INPUT}[10]{Colors.RESET} 📥 Ayarları İçe Aktar
  {Colors.INPUT}[0]{Colors.RESET} 🔙 Ana Menüye Dön

{Colors.INPUT}Seçiminiz: {Colors.RESET}"""
        
        print(menu, end='')
        choice = input().strip()
        
        if choice == '0':
            break
        elif choice == '1':
            view_settings()
        elif choice == '2':
            edit_general_settings()
        elif choice == '3':
            edit_scanning_settings()
        elif choice == '4':
            edit_api_keys()
        elif choice == '5':
            edit_proxy_settings()
        elif choice == '6':
            edit_output_settings()
        elif choice == '7':
            edit_security_settings()
        elif choice == '8':
            reset_settings()
        elif choice == '9':
            export_settings()
        elif choice == '10':
            import_settings()
        else:
            print(f"{Colors.ERROR}[-] Geçersiz seçim!{Colors.RESET}")
        
        input(f"\n{Colors.INPUT}Devam etmek için Enter'a basın...{Colors.RESET}")

def main():
    """Ana fonksiyon"""
    try:
        settings_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}[!] İşlem iptal edildi{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.ERROR}[-] Beklenmeyen hata: {e}{Colors.RESET}")

if __name__ == "__main__":
    main()
