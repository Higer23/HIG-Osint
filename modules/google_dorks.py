#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Google Dorks Module - Google Dork OSINT Araştırma Modülü
"""

import os
import sys
import json
import webbrowser
from datetime import datetime
from colorama import Fore, Style
from pathlib import Path
from urllib.parse import quote

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

def clear_screen():
    """Ekranı temizle"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Modül başlığını göster"""
    header = f"""{Colors.HEADER}
╔═══════════════════════════════════════════════════════════════════╗
║                   GOOGLE DORKS MODÜLÜ                            ║
║               Advanced Google Dork Search Module                 ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(header)

def save_result(filename, data):
    """Sonuçları kaydet"""
    try:
        reports_dir = Path('reports')
        reports_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = reports_dir / f"google_dorks_{filename}_{timestamp}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"{Colors.SUCCESS}[+] Sonuçlar kaydedildi: {filepath}{Colors.RESET}")
        return True
    except Exception as e:
        print(f"{Colors.ERROR}[-] Kayıt hatası: {e}{Colors.RESET}")
        return False

def create_dork_url(dork):
    """Google dork URL'i oluştur"""
    base_url = "https://www.google.com/search?q="
    return base_url + quote(dork)

def security_dorks():
    """Güvenlik açıkları için Google Dork'ları"""
    print(f"\n{Colors.MENU}=== Güvenlik Açığı Dork'ları ==={Colors.RESET}")
    
    dorks = {
        'SQL Injection': [
            'inurl:"index.php?id="',
            'inurl:"product.php?id="',
            'inurl:"item.php?id="',
            'inurl:"page.php?id="',
            'inurl:"news.php?id="'
        ],
        'Admin Panelleri': [
            'intitle:"Admin Login"',
            'inurl:"/admin/login.php"',
            'inurl:"/administrator"',
            'intitle:"Dashboard" inurl:admin',
            'intitle:"control panel" inurl:admin'
        ],
        'Açık Dizinler': [
            'intitle:"Index of /" +.rar',
            'intitle:"Index of /" +.zip',
            'intitle:"Index of /" +.sql',
            'intitle:"Index of /" +password.txt',
            'intitle:"Index of /" +backup'
        ],
        'Hassas Dosyalar': [
            'filetype:sql "password"',
            'filetype:log "password"',
            'filetype:env "DB_PASSWORD"',
            'filetype:conf "password"',
            'filetype:bak inurl:"backup"'
        ],
        'Config Dosyaları': [
            'filetype:xml "configuration"',
            'filetype:yml "configuration"',
            'filetype:ini "configuration"',
            'inurl:wp-config.php',
            'inurl:config.php'
        ]
    }
    
    for category, dork_list in dorks.items():
        print(f"\n{Colors.INFO}[{category}]{Colors.RESET}")
        for i, dork in enumerate(dork_list, 1):
            print(f"  {i}. {dork}")
    
    return dorks

def social_media_dorks():
    """Sosyal medya araştırma Dork'ları"""
    print(f"\n{Colors.MENU}=== Sosyal Medya Dork'ları ==={Colors.RESET}")
    
    print(f"{Colors.INPUT}Hedef kullanıcı adı/email/telefon girin: {Colors.RESET}", end='')
    target = input().strip()
    
    dorks = {
        'LinkedIn': f'site:linkedin.com "{target}"',
        'Twitter': f'site:twitter.com "{target}"',
        'Facebook': f'site:facebook.com "{target}"',
        'Instagram': f'site:instagram.com "{target}"',
        'GitHub': f'site:github.com "{target}"',
        'Reddit': f'site:reddit.com "{target}"',
        'Pinterest': f'site:pinterest.com "{target}"',
        'YouTube': f'site:youtube.com "{target}"'
    }
    
    print(f"\n{Colors.SUCCESS}[+] Sosyal Medya Dork Sorguları:{Colors.RESET}")
    urls = {}
    for platform, dork in dorks.items():
        url = create_dork_url(dork)
        urls[platform] = url
        print(f"  {platform}: {dork}")
    
    choice = input(f"\n{Colors.INPUT}Bu sorguları tarayıcıda açmak ister misiniz? (E/H): {Colors.RESET}").strip().upper()
    if choice in ['E', 'Y', 'EVET', 'YES']:
        for platform, url in urls.items():
            print(f"{Colors.INFO}[*] Açılıyor: {platform}{Colors.RESET}")
            webbrowser.open(url)
    
    return urls

def document_search_dorks():
    """Doküman arama Dork'ları"""
    print(f"\n{Colors.MENU}=== Doküman Arama Dork'ları ==={Colors.RESET}")
    
    print(f"{Colors.INPUT}Arama terimi girin: {Colors.RESET}", end='')
    keyword = input().strip()
    
    dorks = {
        'PDF Dosyaları': f'filetype:pdf "{keyword}"',
        'Word Dosyaları': f'filetype:doc OR filetype:docx "{keyword}"',
        'Excel Dosyaları': f'filetype:xls OR filetype:xlsx "{keyword}"',
        'PowerPoint': f'filetype:ppt OR filetype:pptx "{keyword}"',
        'Text Dosyaları': f'filetype:txt "{keyword}"',
        'CSV Dosyaları': f'filetype:csv "{keyword}"',
        'SQL Dosyaları': f'filetype:sql "{keyword}"',
        'XML Dosyaları': f'filetype:xml "{keyword}"'
    }
    
    print(f"\n{Colors.SUCCESS}[+] Doküman Arama Sorguları:{Colors.RESET}")
    urls = {}
    for doc_type, dork in dorks.items():
        url = create_dork_url(dork)
        urls[doc_type] = url
        print(f"  {doc_type}: {dork}")
    
    choice = input(f"\n{Colors.INPUT}Bu sorguları tarayıcıda açmak ister misiniz? (E/H): {Colors.RESET}").strip().upper()
    if choice in ['E', 'Y', 'EVET', 'YES']:
        for doc_type, url in urls.items():
            print(f"{Colors.INFO}[*] Açılıyor: {doc_type}{Colors.RESET}")
            webbrowser.open(url)
    
    return urls

def email_search_dorks():
    """E-posta arama Dork'ları"""
    print(f"\n{Colors.MENU}=== E-posta Arama Dork'ları ==={Colors.RESET}")
    
    print(f"{Colors.INPUT}Domain adı girin (örn: example.com): {Colors.RESET}", end='')
    domain = input().strip()
    
    dorks = {
        'Genel E-posta': f'@{domain}',
        'Gmail Hesapları': f'site:gmail.com "{domain}"',
        'E-posta Listesi': f'filetype:xls OR filetype:csv "@{domain}"',
        'Contact Sayfaları': f'site:{domain} intext:"@{domain}"',
        'LinkedIn Profilleri': f'site:linkedin.com "@{domain}"',
        'GitHub Profilleri': f'site:github.com "@{domain}"'
    }
    
    print(f"\n{Colors.SUCCESS}[+] E-posta Arama Sorguları:{Colors.RESET}")
    urls = {}
    for search_type, dork in dorks.items():
        url = create_dork_url(dork)
        urls[search_type] = url
        print(f"  {search_type}: {dork}")
    
    return urls

def web_technology_dorks():
    """Web teknolojisi tespiti Dork'ları"""
    print(f"\n{Colors.MENU}=== Web Teknoloji Tespiti Dork'ları ==={Colors.RESET}")
    
    print(f"{Colors.INPUT}Domain adı girin: {Colors.RESET}", end='')
    domain = input().strip()
    
    dorks = {
        'WordPress': f'site:{domain} inurl:wp-content',
        'Joomla': f'site:{domain} inurl:com_',
        'Drupal': f'site:{domain} inurl:node/',
        'phpMyAdmin': f'site:{domain} inurl:phpmyadmin',
        'Apache': f'site:{domain} "Apache" intitle:"Index of"',
        'Nginx': f'site:{domain} "nginx"',
        'PHP': f'site:{domain} ext:php',
        'ASP.NET': f'site:{domain} ext:aspx'
    }
    
    print(f"\n{Colors.SUCCESS}[+] Teknoloji Tespit Sorguları:{Colors.RESET}")
    for tech, dork in dorks.items():
        print(f"  {tech}: {dork}")
    
    return dorks

def camera_iot_dorks():
    """Kamera ve IoT cihaz Dork'ları"""
    print(f"\n{Colors.MENU}=== Kamera ve IoT Cihaz Dork'ları ==={Colors.RESET}")
    
    dorks = {
        'IP Kameralar': [
            'intitle:"Live View / - AXIS"',
            'inurl:view/view.shtml',
            'intitle:"webcamXP 5"',
            'inurl:"ViewerFrame?Mode="',
            'inurl:"/view/index.shtml"'
        ],
        'Web Kameralar': [
            'intitle:"webcam 7"',
            'inurl:8080 intitle:"webcam"',
            'intitle:"live view" intitle:axis',
            'inurl:"/cgi-bin/camera"',
            'intitle:"Network Camera NetworkCamera"'
        ],
        'DVR/NVR': [
            'intitle:"DVR Login"',
            'inurl:"DVR.htm"',
            'intitle:"NVR Web Client"',
            'inurl:"/doc/page/login.asp"',
            'intitle:"Yawcam" inurl:"8081"'
        ],
        'Router/Modem': [
            'intitle:"Router Setup"',
            'intitle:"Wireless Router"',
            'intitle:"ADSL Router"',
            'inurl:"/cgi-bin/luci"',
            'intitle:"DD-WRT" "Status"'
        ]
    }
    
    for category, dork_list in dorks.items():
        print(f"\n{Colors.INFO}[{category}]{Colors.RESET}")
        for i, dork in enumerate(dork_list, 1):
            print(f"  {i}. {dork}")
    
    print(f"\n{Colors.WARNING}[!] UYARI: Bu dork'ları sadece yasal amaçlarla kullanın!{Colors.RESET}")
    
    return dorks

def custom_dork_builder():
    """Özel Google Dork oluşturucu"""
    print(f"\n{Colors.MENU}=== Özel Google Dork Oluşturucu ==={Colors.RESET}")
    
    print(f"\n{Colors.INFO}[*] Google Dork Operatörleri:{Colors.RESET}")
    print(f"  - site:        Belirli bir sitede arama")
    print(f"  - inurl:       URL'de kelime arama")
    print(f"  - intitle:     Başlıkta kelime arama")
    print(f"  - intext:      İçerikte kelime arama")
    print(f"  - filetype:    Dosya tipi arama")
    print(f"  - ext:         Uzantı arama")
    print(f"  - cache:       Önbellek versiyonu")
    print(f"  - link:        Belirli siteye link verenler")
    print(f"  - related:     Benzer siteler")
    print(f"  - info:        Site bilgisi")
    print(f"  - OR:          Veya operatörü")
    print(f"  - AND:         Ve operatörü")
    print(f"  - -:           Hariç tut")
    print(f"  - *:           Joker karakter")
    print(f"  - \"..\":        Tam eşleşme")
    
    dork_parts = []
    
    while True:
        print(f"\n{Colors.INPUT}Operatör seçin (çıkmak için 'q'):  {Colors.RESET}", end='')
        operator = input().strip()
        
        if operator.lower() == 'q':
            break
        
        value = input(f"{Colors.INPUT}Değer girin: {Colors.RESET}").strip()
        
        if operator in ['site', 'inurl', 'intitle', 'intext', 'filetype', 'ext']:
            dork_parts.append(f'{operator}:{value}')
        else:
            dork_parts.append(value)
    
    if dork_parts:
        custom_dork = ' '.join(dork_parts)
        url = create_dork_url(custom_dork)
        
        print(f"\n{Colors.SUCCESS}[+] Oluşturulan Dork: {custom_dork}{Colors.RESET}")
        print(f"{Colors.SUCCESS}[+] URL: {url}{Colors.RESET}")
        
        choice = input(f"\n{Colors.INPUT}Tarayıcıda açmak ister misiniz? (E/H): {Colors.RESET}").strip().upper()
        if choice in ['E', 'Y', 'EVET', 'YES']:
            webbrowser.open(url)
        
        return {'dork': custom_dork, 'url': url}
    
    return None

def dork_templates():
    """Hazır dork şablonları"""
    print(f"\n{Colors.MENU}=== Hazır Google Dork Şablonları ==={Colors.RESET}")
    
    templates = {
        'Kişisel Bilgi Araştırma': {
            'description': 'Bir kişi hakkında bilgi toplama',
            'dorks': [
                '"{isim}" site:linkedin.com',
                '"{isim}" site:twitter.com',
                '"{isim}" filetype:pdf',
                '"{isim}" "@gmail.com"'
            ]
        },
        'Şirket Araştırma': {
            'description': 'Şirket bilgileri ve çalışanlar',
            'dorks': [
                'site:{domain} filetype:pdf',
                'site:linkedin.com "{şirket_adı}"',
                '"{şirket_adı}" site:github.com',
                'inurl:"{şirket_adı}" "email"'
            ]
        },
        'Veri Sızıntısı Tespiti': {
            'description': 'Açıkta kalan veriler',
            'dorks': [
                'site:{domain} filetype:sql',
                'site:{domain} filetype:log',
                'site:{domain} ext:bak',
                'intitle:"Index of" site:{domain}'
            ]
        },
        'Subdomain Keşfi': {
            'description': 'Alt domain tespiti',
            'dorks': [
                'site:*.{domain}',
                'site:{domain} -www',
                'inurl:"{domain}"',
                'site:{domain} filetype:xml'
            ]
        }
    }
    
    for i, (template_name, template_data) in enumerate(templates.items(), 1):
        print(f"\n{Colors.INFO}[{i}] {template_name}{Colors.RESET}")
        print(f"  Açıklama: {template_data['description']}")
        print(f"  Dork'lar:")
        for dork in template_data['dorks']:
            print(f"    - {dork}")

def google_dorks_menu():
    """Google Dorks menüsü"""
    while True:
        clear_screen()
        print_header()
        
        menu = f"""{Colors.MENU}
╔═══════════════════════════════════════════════════════════════╗
║                   GOOGLE DORKS MENÜSÜ                        ║
╚═══════════════════════════════════════════════════════════════╝

  {Colors.INPUT}[1]{Colors.RESET} 🔒 Güvenlik Açıkları Dork'ları
  {Colors.INPUT}[2]{Colors.RESET} 📱 Sosyal Medya Araştırma
  {Colors.INPUT}[3]{Colors.RESET} 📄 Doküman Arama
  {Colors.INPUT}[4]{Colors.RESET} 📧 E-posta Arama
  {Colors.INPUT}[5]{Colors.RESET} 💻 Web Teknoloji Tespiti
  {Colors.INPUT}[6]{Colors.RESET} 📹 Kamera ve IoT Cihazlar
  {Colors.INPUT}[7]{Colors.RESET} 🛠️  Özel Dork Oluşturucu
  {Colors.INPUT}[8]{Colors.RESET} 📋 Hazır Dork Şablonları
  {Colors.INPUT}[0]{Colors.RESET} 🔙 Ana Menüye Dön

{Colors.INPUT}Seçiminiz: {Colors.RESET}"""
        
        print(menu, end='')
        choice = input().strip()
        
        if choice == '0':
            break
        elif choice == '1':
            result = security_dorks()
            save_result("security_dorks", result)
        elif choice == '2':
            result = social_media_dorks()
            if result:
                save_result("social_media_dorks", result)
        elif choice == '3':
            result = document_search_dorks()
            if result:
                save_result("document_search", result)
        elif choice == '4':
            result = email_search_dorks()
            if result:
                save_result("email_search", result)
        elif choice == '5':
            result = web_technology_dorks()
            save_result("web_tech_dorks", result)
        elif choice == '6':
            result = camera_iot_dorks()
            save_result("camera_iot_dorks", result)
        elif choice == '7':
            result = custom_dork_builder()
            if result:
                save_result("custom_dork", result)
        elif choice == '8':
            dork_templates()
        else:
            print(f"{Colors.ERROR}[-] Geçersiz seçim!{Colors.RESET}")
        
        input(f"\n{Colors.INPUT}Devam etmek için Enter'a basın...{Colors.RESET}")

def main():
    """Ana fonksiyon"""
    try:
        google_dorks_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}[!] İşlem iptal edildi{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.ERROR}[-] Beklenmeyen hata: {e}{Colors.RESET}")

if __name__ == "__main__":
    main()
