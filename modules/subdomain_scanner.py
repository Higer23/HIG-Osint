cat > /home/claude/hig_modules/subdomain_scanner.py << 'EOFSUB'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import socket
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

COMMON_SUBDOMAINS = [
    "www", "mail", "ftp", "localhost", "webmail", "smtp", "pop", "ns1", "webdisk",
    "ns2", "cpanel", "whm", "autodiscover", "autoconfig", "m", "imap", "test",
    "ns", "blog", "pop3", "dev", "www2", "admin", "forum", "news", "vpn", "ns3",
    "mail2", "new", "mysql", "old", "lists", "support", "mobile", "mx", "static",
    "docs", "beta", "shop", "sql", "secure", "demo", "cp", "calendar", "wiki",
    "web", "media", "email", "images", "img", "www1", "intranet", "portal", "video",
    "sip", "dns2", "api", "cdn", "stats", "dns1", "ns4", "www3", "dns", "search"
]

def print_header():
    print(f"""{Colors.HEADER}
╔══════════════════════════════════════════════════════════════╗
║            🌍 SUBDOMAIN TARAMA MODÜLÜ 🌍                     ║
╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}""")

def check_subdomain(subdomain, domain):
    try:
        full_domain = f"{subdomain}.{domain}"
        socket.gethostbyname(full_domain)
        return True, full_domain
    except:
        return False, None

def main():
    os.system('clear' if os.name != 'nt' else 'cls')
    print_header()
    
    domain = input(f"{Colors.INPUT}Domain (örn: example.com): {Colors.RESET}").strip()
    if not domain:
        print(f"{Colors.ERROR}[!] Domain boş olamaz!{Colors.RESET}")
        return
    
    print(f"\n{Colors.INFO}[*] Subdomain taraması başlatılıyor...{Colors.RESET}\n")
    
    found_subdomains = []
    total = len(COMMON_SUBDOMAINS)
    
    for i, subdomain in enumerate(COMMON_SUBDOMAINS, 1):
        print(f"{Colors.INFO}[{i}/{total}] {subdomain}.{domain} kontrol ediliyor...{Colors.RESET}", end='\r')
        exists, full_domain = check_subdomain(subdomain, domain)
        
        if exists:
            found_subdomains.append(full_domain)
            print(f"{Colors.SUCCESS}✓ {full_domain:50} - BULUNDU!{Colors.RESET}")
    
    print(f"\n\n{Colors.HEADER}╔════════════════════ SONUÇ ══════════════════════╗{Colors.RESET}")
    print(f"{Colors.SUCCESS}Bulunan Subdomain: {len(found_subdomains)}{Colors.RESET}")
    print(f"{Colors.HEADER}╚═════════════════════════════════════════════════╝{Colors.RESET}\n")
    
    if found_subdomains:
        if input(f"{Colors.INPUT}Kaydet? (E/H): {Colors.RESET}").strip().upper() in ['E', 'Y', 'EVET', 'YES']:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_dir = BASE_DIR / 'reports' / 'subdomain_scanner'
            report_dir.mkdir(parents=True, exist_ok=True)
            report_file = report_dir / f"{domain.replace('.', '_')}_{timestamp}.txt"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(f"Subdomain Tarama - {domain}\n" + "="*65 + "\n")
                for sub in found_subdomains:
                    f.write(f"{sub}\n")
            print(f"{Colors.SUCCESS}✓ {report_file}{Colors.RESET}")
    
    input(f"\n{Colors.INPUT}Enter...{Colors.RESET}")

if __name__ == "__main__":
    main()
EOFSUB

cat > /home/claude/hig_modules/pdf_metadata.py << 'EOFPDF'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path
from colorama import Fore, Style

try:
    from PyPDF2 import PdfReader
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF2", "--break-system-packages"])
    from PyPDF2 import PdfReader

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
║            📄 PDF METADATA ANALİZİ MODÜLÜ 📄                ║
╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}""")

def extract_pdf_metadata(pdf_path):
    print(f"\n{Colors.INFO}[*] PDF metadata çıkarılıyor...{Colors.RESET}\n")
    
    try:
        reader = PdfReader(pdf_path)
        metadata = reader.metadata
        
        if not metadata:
            print(f"{Colors.ERROR}✗ Metadata bulunamadı!{Colors.RESET}")
            return None
        
        print(f"{Colors.SUCCESS}✓ PDF Bilgileri:{Colors.RESET}\n")
        print(f"{Colors.INFO}  Sayfa Sayısı    : {len(reader.pages)}{Colors.RESET}")
        
        meta_fields = {
            '/Title': 'Başlık',
            '/Author': 'Yazar',
            '/Subject': 'Konu',
            '/Creator': 'Oluşturan',
            '/Producer': 'Üretici',
            '/CreationDate': 'Oluşturma Tarihi',
            '/ModDate': 'Değiştirilme Tarihi',
        }
        
        for key, label in meta_fields.items():
            if key in metadata:
                print(f"{Colors.INFO}  {label:20} : {metadata[key]}{Colors.RESET}")
        
        return metadata
        
    except Exception as e:
        print(f"{Colors.ERROR}✗ Hata: {e}{Colors.RESET}")
        return None

def main():
    os.system('clear' if os.name != 'nt' else 'cls')
    print_header()
    
    pdf_path = input(f"{Colors.INPUT}PDF dosya yolu: {Colors.RESET}").strip()
    
    if not os.path.exists(pdf_path):
        print(f"{Colors.ERROR}[!] Dosya bulunamadı!{Colors.RESET}")
        return
    
    metadata = extract_pdf_metadata(pdf_path)
    
    if metadata:
        print(f"\n{Colors.SUCCESS}✓ Metadata başarıyla çıkarıldı.{Colors.RESET}")
    
    input(f"\n{Colors.INPUT}Enter...{Colors.RESET}")

if __name__ == "__main__":
    main()
EOFPDF

cat > /home/claude/hig_modules/advanced_tools.py << 'EOFADV'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path
from colorama import Fore, Style

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
║            🔧 GELİŞMİŞ ARAÇLAR MODÜLÜ 🔧                    ║
╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}""")

TOOLS = {
    "1": ("Shodan Search", "https://www.shodan.io/"),
    "2": ("Censys", "https://search.censys.io/"),
    "3": ("VirusTotal", "https://www.virustotal.com/"),
    "4": ("Have I Been Pwned", "https://haveibeenpwned.com/"),
    "5": ("Hunter.io", "https://hunter.io/"),
    "6": ("Maltego", "https://www.maltego.com/"),
    "7": ("SpiderFoot", "https://www.spiderfoot.net/"),
    "8": ("TheHarvester", "https://github.com/laramies/theHarvester"),
    "9": ("Recon-ng", "https://github.com/lanmaster53/recon-ng"),
    "10": ("OSINT Framework", "https://osintframework.com/"),
}

def main():
    os.system('clear' if os.name != 'nt' else 'cls')
    print_header()
    
    print(f"{Colors.INFO}Gelişmiş OSINT Araçları:{Colors.RESET}\n")
    
    for key, (name, url) in TOOLS.items():
        print(f"{Colors.INPUT}[{key:2}]{Colors.INFO} {name:25} - {url}{Colors.RESET}")
    
    print(f"\n{Colors.WARNING}Not: Bu araçlar harici web servisleridir.{Colors.RESET}")
    print(f"{Colors.WARNING}Her birinin kendi kullanım koşulları vardır.{Colors.RESET}")
    
    input(f"\n{Colors.INPUT}Enter...{Colors.RESET}")

if __name__ == "__main__":
    main()
EOFADV

cat > /home/claude/hig_modules/settings.py << 'EOFSET'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path
from colorama import Fore, Style

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
║            ⚙️  AYARLAR MODÜLÜ ⚙️                             ║
╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}""")

def clear_reports():
    report_dir = BASE_DIR / 'reports'
    count = 0
    
    if report_dir.exists():
        for subdir in report_dir.iterdir():
            if subdir.is_dir():
                for file in subdir.glob('*.txt'):
                    file.unlink()
                    count += 1
    
    print(f"{Colors.SUCCESS}✓ {count} rapor dosyası silindi.{Colors.RESET}")

def show_info():
    print(f"\n{Colors.INFO}HIG-Osint Bilgileri:{Colors.RESET}\n")
    print(f"{Colors.SUCCESS}Versiyon       : 3.0.0{Colors.RESET}")
    print(f"{Colors.SUCCESS}Geliştirici    : Halil Gercek{Colors.RESET}")
    print(f"{Colors.SUCCESS}E-posta        : higeryazilim@gmail.com{Colors.RESET}")
    print(f"{Colors.SUCCESS}GitHub         : https://github.com/Higer23/HIG-Osint{Colors.RESET}")
    print(f"{Colors.SUCCESS}Lisans         : GNU GPL v3.0{Colors.RESET}")

def main():
    os.system('clear' if os.name != 'nt' else 'cls')
    print_header()
    
    print(f"{Colors.INFO}Ayarlar:{Colors.RESET}\n")
    print(f"{Colors.INPUT}[1]{Colors.INFO} Tüm Raporları Temizle")
    print(f"{Colors.INPUT}[2]{Colors.INFO} Hakkında Bilgi")
    print(f"{Colors.INPUT}[0]{Colors.INFO} Geri Dön{Colors.RESET}\n")
    
    choice = input(f"{Colors.INPUT}Seçim: {Colors.RESET}").strip()
    
    if choice == '1':
        confirm = input(f"{Colors.ERROR}Tüm raporlar silinecek! Emin misiniz? (E/H): {Colors.RESET}").strip().upper()
        if confirm in ['E', 'Y', 'EVET', 'YES']:
            clear_reports()
    elif choice == '2':
        show_info()
    
    input(f"\n{Colors.INPUT}Enter...{Colors.RESET}")

if __name__ == "__main__":
    main()
EOFSET

echo "Tüm kalan modüller oluşturuldu!"
