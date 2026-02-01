#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔═══════════════════════════════════════════════════════════════╗
║                         HIG-OSINT                             ║
║              Advanced OSINT Intelligence Tool                 ║
║                                                               ║
║  Developer    : Halil Gercek                                  ║
║  Email        : higeryazilim@gmail.com                        ║
║  GitHub       : https://github.com/Higer23/HIG-Osint          ║
║  Version      : 3.0.0                                         ║
║  License      : GNU General Public License v3.0               ║
║                                                               ║
║  Description  : Termux ve CMD uyumlu gelişmiş OSINT aracı    ║
║                 Mr.Holmes ve X-osint'in birleştirilmiş hali  ║
╚═══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import platform
import subprocess
from pathlib import Path

# Renkli çıktı için colorama
try:
    from colorama import Fore, Back, Style, init
    init(autoreset=True)
except ImportError:
    print("[!] colorama modülü yüklenemedi. Yükleniyor...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama", "--break-system-packages"])
    from colorama import Fore, Back, Style, init
    init(autoreset=True)

# Ana dizin
BASE_DIR = Path(__file__).resolve().parent

# Sistem bilgisi
SYSTEM = platform.system()
IS_TERMUX = os.path.exists('/data/data/com.termux')
IS_WINDOWS = SYSTEM == 'Windows'
IS_LINUX = SYSTEM == 'Linux'

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
    if IS_WINDOWS:
        os.system('cls')
    else:
        os.system('clear')

def print_banner():
    """HIG-Osint banner'ını göster"""
    banner = f"""{Colors.HEADER}
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║  ██╗  ██╗██╗ ██████╗        ██████╗ ███████╗██╗███╗   ██╗████████╗      ║
║  ██║  ██║██║██╔════╝       ██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝      ║
║  ███████║██║██║  ███╗█████╗██║   ██║███████╗██║██╔██╗ ██║   ██║         ║
║  ██╔══██║██║██║   ██║╚════╝██║   ██║╚════██║██║██║╚██╗██║   ██║         ║
║  ██║  ██║██║╚██████╔╝      ╚██████╔╝███████║██║██║ ╚████║   ██║         ║
║  ╚═╝  ╚═╝╚═╝ ╚═════╝        ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝         ║
║                                                                           ║
║          ╔══════════════════════════════════════════════════╗            ║
║          ║   Advanced OSINT Intelligence Gathering Tool    ║            ║
║          ╚══════════════════════════════════════════════════╝            ║
║                                                                           ║
║  Developer     : Halil Gercek                                            ║
║  Email         : higeryazilim@gmail.com                                  ║
║  GitHub        : https://github.com/Higer23/HIG-Osint                    ║
║  Version       : 3.0.0                                                   ║
║                                                                           ║
║  Platform      : {('Termux' if IS_TERMUX else 'Windows' if IS_WINDOWS else 'Linux'):^58} ║
║  Python        : {sys.version.split()[0]:^58} ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(banner)

def show_disclaimer():
    """Yasal uyarı göster"""
    disclaimer = f"""{Colors.WARNING}
╔═══════════════════════════════════════════════════════════════════════════╗
║                            YASAL UYARI / DISCLAIMER                       ║
╚═══════════════════════════════════════════════════════════════════════════╝

Bu araç sadece yasal ve etik OSINT (Open Source Intelligence) araştırmaları 
için tasarlanmıştır. 

⚠️  ÖNEMLİ UYARILAR:
   • Bu aracı kullanarak yaptığınız tüm işlemlerden SİZ sorumlusunuz
   • İzinsiz veri toplama, takip veya istihbarat faaliyeti YASAKTIR
   • Sadece kendinize ait veya izniniz olan verileri araştırın
   • Yerel yasalara ve düzenlemelere uygun hareket edin

📜 Geliştirici (Halil Gercek), bu aracın kötüye kullanımından sorumlu değildir.

Bu uyarıyı kabul ediyor musunuz? (E/H): {Colors.RESET}"""
    
    acceptance_file = BASE_DIR / '.disclaimer_accepted'
    
    if not acceptance_file.exists():
        print(disclaimer, end='')
        choice = input().strip().upper()
        
        if choice in ['E', 'Y', 'EVET', 'YES']:
            acceptance_file.write_text('accepted')
            print(f"\n{Colors.SUCCESS}✓ Uyarı kabul edildi. Araç başlatılıyor...{Colors.RESET}")
            import time
            time.sleep(2)
        else:
            print(f"\n{Colors.ERROR}✗ Uyarı kabul edilmedi. Araç kapatılıyor...{Colors.RESET}")
            sys.exit(0)

def check_dependencies():
    """Gerekli bağımlılıkları kontrol et"""
    print(f"{Colors.INFO}[*] Bağımlılıklar kontrol ediliyor...{Colors.RESET}")
    
    required_modules = [
        'requests', 'beautifulsoup4', 'colorama', 'phonenumbers',
        'googlesearch-python', 'pillow', 'flask', 'cryptography',
        'ping3', 'python-whois', 'dnspython', 'shodan', 'tweepy',
        'instagram-scraper', 'tiktok-scraper', 'opencv-python'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module.replace('-', '_').split('-')[0])
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"{Colors.WARNING}[!] Eksik modüller bulundu: {', '.join(missing_modules)}{Colors.RESET}")
        print(f"{Colors.INFO}[*] Modüller yükleniyor...{Colors.RESET}")
        
        for module in missing_modules:
            try:
                if IS_TERMUX or IS_LINUX:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", module, "--break-system-packages"])
                else:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", module])
                print(f"{Colors.SUCCESS}✓ {module} yüklendi{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.ERROR}✗ {module} yüklenemedi: {e}{Colors.RESET}")
    else:
        print(f"{Colors.SUCCESS}✓ Tüm bağımlılıklar mevcut{Colors.RESET}")

def main_menu():
    """Ana menü"""
    while True:
        clear_screen()
        print_banner()
        
        menu = f"""{Colors.MENU}
╔═══════════════════════════════════════════════════════════════════════════╗
║                              ANA MENÜ                                     ║
╚═══════════════════════════════════════════════════════════════════════════╝

  {Colors.INPUT}[01]{Colors.MENU} 👤 Kullanıcı Adı Araştırma    {Colors.INPUT}[11]{Colors.MENU} 🌐 IP Adresi Araştırma
  {Colors.INPUT}[02]{Colors.MENU} 📧 E-posta Araştırma          {Colors.INPUT}[12]{Colors.MENU} 🔍 Google Dorks
  {Colors.INPUT}[03]{Colors.MENU} 📱 Telefon Numarası Araştırma {Colors.INPUT}[13]{Colors.MENU} 🗺️  Konum Takibi
  {Colors.INPUT}[04]{Colors.MENU} 🏢 Domain/Website Araştırma   {Colors.INPUT}[14]{Colors.MENU} 📸 Görsel OSINT (EXIF)
  {Colors.INPUT}[05]{Colors.MENU} 👥 Kişi Araştırma             {Colors.INPUT}[15]{Colors.MENU} 🔐 Hash Çözümleme
  {Colors.INPUT}[06]{Colors.MENU} 🐦 Twitter/X Araştırma        {Colors.INPUT}[16]{Colors.MENU} 📡 Port Tarama
  {Colors.INPUT}[07]{Colors.MENU} 📷 Instagram Araştırma        {Colors.INPUT}[17]{Colors.MENU} 🌍 Subdomain Tarama
  {Colors.INPUT}[08]{Colors.MENU} 📱 TikTok Araştırma           {Colors.INPUT}[18]{Colors.MENU} 📄 PDF Metadata Analizi
  {Colors.INPUT}[09]{Colors.MENU} 💼 LinkedIn Araştırma         {Colors.INPUT}[19]{Colors.MENU} 🔧 Gelişmiş Araçlar
  {Colors.INPUT}[10]{Colors.MENU} 📘 Facebook Araştırma         {Colors.INPUT}[20]{Colors.MENU} ⚙️  Ayarlar

  {Colors.INPUT}[00]{Colors.ERROR} ❌ Çıkış

{Colors.INPUT}Seçiminiz: {Colors.RESET}"""
        
        print(menu, end='')
        choice = input().strip()
        
        if choice == '00':
            print(f"\n{Colors.SUCCESS}HIG-Osint kullandığınız için teşekkürler!{Colors.RESET}")
            sys.exit(0)
        elif choice == '01':
            from modules import username_search
            username_search.main()
        elif choice == '02':
            from modules import email_search
            email_search.main()
        elif choice == '03':
            from modules import phone_search
            phone_search.main()
        elif choice == '04':
            from modules import domain_search
            domain_search.main()
        elif choice == '05':
            from modules import person_search
            person_search.main()
        elif choice == '06':
            from modules import twitter_search
            twitter_search.main()
        elif choice == '07':
            from modules import instagram_search
            instagram_search.main()
        elif choice == '08':
            from modules import tiktok_search
            tiktok_search.main()
        elif choice == '09':
            from modules import linkedin_search
            linkedin_search.main()
        elif choice == '10':
            from modules import facebook_search
            facebook_search.main()
        elif choice == '11':
            from modules import ip_search
            ip_search.main()
        elif choice == '12':
            from modules import google_dorks
            google_dorks.main()
        elif choice == '13':
            from modules import location_tracker
            location_tracker.main()
        elif choice == '14':
            from modules import image_osint
            image_osint.main()
        elif choice == '15':
            from modules import hash_decoder
            hash_decoder.main()
        elif choice == '16':
            from modules import port_scanner
            port_scanner.main()
        elif choice == '17':
            from modules import subdomain_scanner
            subdomain_scanner.main()
        elif choice == '18':
            from modules import pdf_metadata
            pdf_metadata.main()
        elif choice == '19':
            from modules import advanced_tools
            advanced_tools.main()
        elif choice == '20':
            from modules import settings
            settings.main()
        else:
            print(f"{Colors.ERROR}[!] Geçersiz seçim!{Colors.RESET}")
            input(f"{Colors.INPUT}Devam etmek için Enter'a basın...{Colors.RESET}")

def main():
    """Ana program"""
    try:
        show_disclaimer()
        clear_screen()
        print_banner()
        check_dependencies()
        input(f"\n{Colors.INPUT}Ana menüye geçmek için Enter'a basın...{Colors.RESET}")
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}[!] Program kullanıcı tarafından sonlandırıldı.{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.ERROR}[!] Beklenmeyen bir hata oluştu: {e}{Colors.RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
