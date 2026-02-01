cat > /home/claude/hig_modules/instagram_search.py << 'EOFINSTA'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HIG-Osint Instagram Search Module
"""

import os
import sys
from pathlib import Path
from colorama import Fore, Style
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent

class Colors:
    HEADER = Fore.CYAN + Style.BRIGHT
    SUCCESS = Fore.GREEN + Style.BRIGHT
    WARNING = Fore.YELLOW + Style.BRIGHT
    ERROR = Fore.RED + Style.BRIGHT
    INFO = Fore.BLUE + Style.BRIGHT
    INPUT = Fore.WHITE + Style.BRIGHT
    RESET = Style.RESET_ALL

def print_header():
    header = f"""{Colors.HEADER}
╔══════════════════════════════════════════════════════════════╗
║            📷 INSTAGRAM ARAŞTIRMA MODÜLÜ 📷                  ║
╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(header)

def search_instagram(username):
    print(f"\n{Colors.INFO}[*] Instagram araştırması...{Colors.RESET}\n")
    
    links = {
        "Profil": f"https://www.instagram.com/{username}/",
        "Profil (Web)": f"https://www.instagram.com/{username}/?hl=tr",
        "Picuki": f"https://www.picuki.com/profile/{username}",
        "Dumpor": f"https://dumpor.com/v/{username}",
        "InstaDP": f"https://www.instadp.com/fullsize/{username}",
        "StoriesIG": f"https://storiesig.net/stories/{username}",
        "ImgInn": f"https://imginn.com/{username}/",
        "Google": f"https://www.google.com/search?q=site:instagram.com+{username}",
        "SocialBlade": f"https://socialblade.com/instagram/user/{username}",
        "Instagram Wayback": f"https://web.archive.org/web/*/instagram.com/{username}*",
    }
    
    for name, url in links.items():
        print(f"{Colors.SUCCESS}→ {name:20} : {url}{Colors.RESET}")
    return links

def save_report(username, links):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = BASE_DIR / 'reports' / 'instagram_search'
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir / f"{username}_{timestamp}.txt"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("╔═══════════════════════════════════════════════════════════════╗\n")
        f.write("║            HIG-OSINT INSTAGRAM ARAŞTIRMA RAPORU               ║\n")
        f.write("╚═══════════════════════════════════════════════════════════════╝\n\n")
        f.write(f"Kullanıcı: @{username}\nTarih: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n")
        f.write("LİNKLER:\n" + "-"*65 + "\n")
        for name, url in links.items():
            f.write(f"→ {name:20} : {url}\n")
        f.write(f"\nRapor: {report_file}\n")
    return report_file

def main():
    os.system('clear' if os.name != 'nt' else 'cls')
    print_header()
    
    username = input(f"{Colors.INPUT}Instagram kullanıcı adı: {Colors.RESET}").strip().replace('@', '')
    if not username:
        print(f"{Colors.ERROR}[!] Kullanıcı adı boş olamaz!{Colors.RESET}")
        return
    
    links = search_instagram(username)
    
    print(f"\n{Colors.HEADER}╔════════════════════ ÖZET ══════════════════════╗{Colors.RESET}")
    print(f"{Colors.SUCCESS}Linkler: {len(links)} adet{Colors.RESET}")
    print(f"{Colors.HEADER}╚════════════════════════════════════════════════╝{Colors.RESET}\n")
    
    save = input(f"{Colors.INPUT}Rapor kaydet? (E/H): {Colors.RESET}").strip().upper()
    if save in ['E', 'Y', 'EVET', 'YES']:
        print(f"\n{Colors.SUCCESS}✓ {save_report(username, links)}{Colors.RESET}")
    
    input(f"\n{Colors.INPUT}Enter...{Colors.RESET}")

if __name__ == "__main__":
    main()
EOFINSTA

cat > /home/claude/hig_modules/tiktok_search.py << 'EOFTIKTOK'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HIG-Osint TikTok Search Module
"""

import os
import sys
from pathlib import Path
from colorama import Fore, Style
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent

class Colors:
    HEADER = Fore.CYAN + Style.BRIGHT
    SUCCESS = Fore.GREEN + Style.BRIGHT
    WARNING = Fore.YELLOW + Style.BRIGHT
    ERROR = Fore.RED + Style.BRIGHT
    INFO = Fore.BLUE + Style.BRIGHT
    INPUT = Fore.WHITE + Style.BRIGHT
    RESET = Style.RESET_ALL

def print_header():
    header = f"""{Colors.HEADER}
╔══════════════════════════════════════════════════════════════╗
║            📱 TIKTOK ARAŞTIRMA MODÜLÜ 📱                     ║
╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(header)

def search_tiktok(username):
    print(f"\n{Colors.INFO}[*] TikTok araştırması...{Colors.RESET}\n")
    
    links = {
        "Profil": f"https://www.tiktok.com/@{username}",
        "Google": f"https://www.google.com/search?q=site:tiktok.com+@{username}",
        "TikTok Search": f"https://www.tiktok.com/search/user?q={username}",
        "Urlebird": f"https://urlebird.com/user/{username}/",
        "TikStats": f"https://tikstats.org/@{username}",
        "Mavekite": f"https://mavekite.com/user/{username}",
        "Social Blade": f"https://socialblade.com/tiktok/user/{username}",
        "TikBuddy": f"https://app.tikbuddy.com/@{username}",
    }
    
    for name, url in links.items():
        print(f"{Colors.SUCCESS}→ {name:20} : {url}{Colors.RESET}")
    return links

def save_report(username, links):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = BASE_DIR / 'reports' / 'tiktok_search'
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir / f"{username}_{timestamp}.txt"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("╔═══════════════════════════════════════════════════════════════╗\n")
        f.write("║              HIG-OSINT TIKTOK ARAŞTIRMA RAPORU                ║\n")
        f.write("╚═══════════════════════════════════════════════════════════════╝\n\n")
        f.write(f"Kullanıcı: @{username}\nTarih: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n")
        for name, url in links.items():
            f.write(f"→ {name:20} : {url}\n")
        f.write(f"\nRapor: {report_file}\n")
    return report_file

def main():
    os.system('clear' if os.name != 'nt' else 'cls')
    print_header()
    
    username = input(f"{Colors.INPUT}TikTok kullanıcı adı (@'sız): {Colors.RESET}").strip().replace('@', '')
    if not username:
        print(f"{Colors.ERROR}[!] Boş olamaz!{Colors.RESET}")
        return
    
    links = search_tiktok(username)
    print(f"\n{Colors.SUCCESS}✓ {len(links)} link bulundu{Colors.RESET}\n")
    
    if input(f"{Colors.INPUT}Kaydet? (E/H): {Colors.RESET}").strip().upper() in ['E', 'Y', 'EVET', 'YES']:
        print(f"{Colors.SUCCESS}✓ {save_report(username, links)}{Colors.RESET}")
    
    input(f"\n{Colors.INPUT}Enter...{Colors.RESET}")

if __name__ == "__main__":
    main()
EOFTIKTOK

echo "Instagram ve TikTok modülleri oluşturuldu"
