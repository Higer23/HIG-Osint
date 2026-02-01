cat > /home/claude/hig_modules/ip_search.py << 'EOFIP'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import socket
import requests
from pathlib import Path
from colorama import Fore, Style
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent

class Colors:
    HEADER = Fore.CYAN + Style.BRIGHT
    SUCCESS = Fore.GREEN + Style.BRIGHT
    ERROR = Fore.RED + Style.BRIGHT
    INFO = Fore.BLUE + Style.BRIGHT
    INPUT = Fore.WHITE + Style.BRIGHT
    RESET = Style.RESET_ALL

def print_header():
    print(f"""{Colors.HEADER}
╔══════════════════════════════════════════════════════════════╗
║            🌐 IP ADRESİ ARAŞTIRMA MODÜLÜ 🌐                 ║
╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}""")

def analyze_ip(ip):
    print(f"\n{Colors.INFO}[*] IP analizi başlatılıyor...{Colors.RESET}\n")
    
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}', timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"{Colors.SUCCESS}✓ IP Bilgileri:{Colors.RESET}")
            print(f"  IP          : {data.get('query')}")
            print(f"  Ülke        : {data.get('country')} ({data.get('countryCode')})")
            print(f"  Bölge       : {data.get('regionName')}")
            print(f"  Şehir       : {data.get('city')}")
            print(f"  ISP         : {data.get('isp')}")
            print(f"  Organizasyon: {data.get('org')}")
            print(f"  AS          : {data.get('as')}")
            print(f"  Koordinat   : {data.get('lat')}, {data.get('lon')}")
            print(f"  Zaman Dilimi: {data.get('timezone')}")
            return data
    except Exception as e:
        print(f"{Colors.ERROR}✗ Hata: {e}{Colors.RESET}")
    return None

def main():
    os.system('clear' if os.name != 'nt' else 'cls')
    print_header()
    
    ip = input(f"{Colors.INPUT}IP Adresi: {Colors.RESET}").strip()
    if not ip:
        print(f"{Colors.ERROR}[!] IP adresi boş olamaz!{Colors.RESET}")
        return
    
    data = analyze_ip(ip)
    
    if data:
        print(f"\n{Colors.INFO}[*] Online araştırma linkleri:{Colors.RESET}")
        links = {
            "IPinfo": f"https://ipinfo.io/{ip}",
            "AbuseIPDB": f"https://www.abuseipdb.com/check/{ip}",
            "VirusTotal": f"https://www.virustotal.com/gui/ip-address/{ip}",
            "Shodan": f"https://www.shodan.io/host/{ip}",
            "Censys": f"https://search.censys.io/hosts/{ip}",
        }
        for name, url in links.items():
            print(f"{Colors.SUCCESS}→ {name:15} : {url}{Colors.RESET}")
        
        if input(f"\n{Colors.INPUT}Kaydet? (E/H): {Colors.RESET}").strip().upper() in ['E', 'Y', 'EVET', 'YES']:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_dir = BASE_DIR / 'reports' / 'ip_search'
            report_dir.mkdir(parents=True, exist_ok=True)
            report_file = report_dir / f"{ip.replace('.', '_')}_{timestamp}.txt"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(f"IP Araştırma Raporu - {ip}\n" + "="*65 + "\n")
                for k, v in data.items():
                    f.write(f"{k}: {v}\n")
                f.write("\nLinkler:\n")
                for name, url in links.items():
                    f.write(f"{name}: {url}\n")
            print(f"{Colors.SUCCESS}✓ {report_file}{Colors.RESET}")
    
    input(f"\n{Colors.INPUT}Enter...{Colors.RESET}")

if __name__ == "__main__":
    main()
EOFIP

cat > /home/claude/hig_modules/google_dorks.py << 'EOFDORKS'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path
from colorama import Fore, Style
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent

class Colors:
    HEADER = Fore.CYAN + Style.BRIGHT
    SUCCESS = Fore.GREEN + Style.BRIGHT
    ERROR = Fore.RED + Style.BRIGHT
    INFO = Fore.BLUE + Style.BRIGHT
    INPUT = Fore.WHITE + Style.BRIGHT
    RESET = Style.RESET_ALL

DORK_CATEGORIES = {
    "1": ("Dosya Bulma", 'filetype:{ext} "{keyword}"'),
    "2": ("Site İçi Arama", 'site:{domain} "{keyword}"'),
    "3": ("Başlık Arama", 'intitle:"{keyword}"'),
    "4": ("URL Arama", 'inurl:"{keyword}"'),
    "5": ("Cache Arama", 'cache:{domain}'),
    "6": ("Hassas Bilgiler", 'intext:"password" | intext:"username" site:{domain}'),
    "7": ("Dizin Listeleme", 'intitle:"index of" site:{domain}'),
    "8": ("SQL Hataları", 'intext:"sql syntax" site:{domain}'),
    "9": ("Login Sayfaları", 'inurl:login | inurl:signin site:{domain}'),
    "10": ("Admin Panelleri", 'inurl:admin | inurl:administrator site:{domain}'),
}

def print_header():
    print(f"""{Colors.HEADER}
╔══════════════════════════════════════════════════════════════╗
║            🔍 GOOGLE DORKS MODÜLÜ 🔍                         ║
╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}""")

def main():
    os.system('clear' if os.name != 'nt' else 'cls')
    print_header()
    
    print(f"{Colors.INFO}Google Dorks Kategorileri:{Colors.RESET}\n")
    for key, (name, template) in DORK_CATEGORIES.items():
        print(f"{Colors.INPUT}[{key}]{Colors.INFO} {name:20} - {template}{Colors.RESET}")
    
    choice = input(f"\n{Colors.INPUT}Kategori seçin (1-10): {Colors.RESET}").strip()
    
    if choice not in DORK_CATEGORIES:
        print(f"{Colors.ERROR}[!] Geçersiz seçim!{Colors.RESET}")
        return
    
    category_name, dork_template = DORK_CATEGORIES[choice]
    
    if "{keyword}" in dork_template:
        keyword = input(f"{Colors.INPUT}Anahtar kelime: {Colors.RESET}").strip()
        dork_template = dork_template.replace("{keyword}", keyword)
    
    if "{domain}" in dork_template:
        domain = input(f"{Colors.INPUT}Domain: {Colors.RESET}").strip()
        dork_template = dork_template.replace("{domain}", domain)
    
    if "{ext}" in dork_template:
        ext = input(f"{Colors.INPUT}Dosya uzantısı (pdf, doc, xls): {Colors.RESET}").strip()
        dork_template = dork_template.replace("{ext}", ext)
    
    google_url = f"https://www.google.com/search?q={dork_template}"
    
    print(f"\n{Colors.SUCCESS}Google Dork:{Colors.RESET}")
    print(f"{Colors.INFO}{dork_template}{Colors.RESET}")
    print(f"\n{Colors.SUCCESS}URL:{Colors.RESET}")
    print(f"{Colors.INFO}{google_url}{Colors.RESET}")
    
    input(f"\n{Colors.INPUT}Enter...{Colors.RESET}")

if __name__ == "__main__":
    main()
EOFDORKS

echo "IP ve Google Dorks modülleri oluşturuldu"
