cat > /home/claude/hig_modules/twitter_search.py << 'EOFTWITTER'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HIG-Osint Twitter/X Search Module
Twitter/X profil araştırması
"""

import os
import sys
import requests
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
║            🐦 TWITTER/X ARAŞTIRMA MODÜLÜ 🐦                 ║
╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(header)

def search_twitter(username):
    print(f"\n{Colors.INFO}[*] Twitter/X araştırması yapılıyor...{Colors.RESET}\n")
    
    links = {
        "Profil": f"https://twitter.com/{username}",
        "Medya": f"https://twitter.com/{username}/media",
        "Beğeniler": f"https://twitter.com/{username}/likes",
        "Takipçiler": f"https://twitter.com/{username}/followers",
        "Takip": f"https://twitter.com/{username}/following",
        "Yanıtlar": f"https://twitter.com/{username}/with_replies",
        "Google Arama": f"https://www.google.com/search?q=site:twitter.com+{username}",
        "TweetDeck": f"https://tweetdeck.twitter.com",
        "Wayback Machine": f"https://web.archive.org/web/*/twitter.com/{username}*",
        "Social Bearing": f"https://socialbearing.com/search/user/{username}",
    }
    
    for name, url in links.items():
        print(f"{Colors.SUCCESS}→ {name:20} : {url}{Colors.RESET}")
    
    return links

def save_report(username, links):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = BASE_DIR / 'reports' / 'twitter_search'
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir / f"{username}_{timestamp}.txt"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("╔═══════════════════════════════════════════════════════════════╗\n")
        f.write("║              HIG-OSINT TWITTER/X ARAŞTIRMA RAPORU             ║\n")
        f.write("╚═══════════════════════════════════════════════════════════════╝\n\n")
        f.write(f"Kullanıcı: @{username}\n")
        f.write(f"Tarih: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n")
        f.write("ARAŞTIRMA LİNKLERİ:\n" + "-"*65 + "\n")
        for name, url in links.items():
            f.write(f"→ {name:20} : {url}\n")
        f.write(f"\nRapor: {report_file}\n")
    return report_file

def main():
    os.system('clear' if os.name != 'nt' else 'cls')
    print_header()
    
    username = input(f"{Colors.INPUT}Twitter kullanıcı adı (@'sız): {Colors.RESET}").strip().replace('@', '')
    if not username:
        print(f"{Colors.ERROR}[!] Kullanıcı adı boş olamaz!{Colors.RESET}")
        return
    
    links = search_twitter(username)
    
    print(f"\n{Colors.HEADER}╔════════════════════ ÖZET ══════════════════════╗{Colors.RESET}")
    print(f"{Colors.SUCCESS}Araştırma Linkleri: {len(links)} adet{Colors.RESET}")
    print(f"{Colors.HEADER}╚════════════════════════════════════════════════╝{Colors.RESET}\n")
    
    save = input(f"{Colors.INPUT}Rapor kaydet? (E/H): {Colors.RESET}").strip().upper()
    if save in ['E', 'Y', 'EVET', 'YES']:
        report_file = save_report(username, links)
        print(f"\n{Colors.SUCCESS}✓ Rapor: {report_file}{Colors.RESET}")
    
    input(f"\n{Colors.INPUT}Ana menüye dönmek için Enter...{Colors.RESET}")

if __name__ == "__main__":
    main()
EOFTWITTER
echo "Twitter modülü oluşturuldu"
