#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HIG-Osint Person Search Module
Kişi araştırması - İsim, soyisim ile arama
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
    """Modül başlığını yazdır"""
    header = f"""{Colors.HEADER}
╔══════════════════════════════════════════════════════════════╗
║              👥 KİŞİ ARAŞTIRMA MODÜLÜ 👥                     ║
╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(header)

def search_person_online(first_name, last_name):
    """Kişiyi online platformlarda ara"""
    print(f"\n{Colors.INFO}[*] '{first_name} {last_name}' aranıyor...{Colors.RESET}\n")
    
    full_name = f"{first_name} {last_name}"
    search_links = {
        "Google": f"https://www.google.com/search?q=%22{full_name}%22",
        "LinkedIn": f"https://www.linkedin.com/search/results/people/?keywords={full_name}",
        "Facebook": f"https://www.facebook.com/search/people/?q={full_name}",
        "Twitter": f"https://twitter.com/search?q={full_name}&f=user",
        "Instagram": f"https://www.instagram.com/explore/tags/{first_name}{last_name}/",
        "TruePeopleSearch": f"https://www.truepeoplesearch.com/results?name={first_name}%20{last_name}",
        "WhitePages": f"https://www.whitepages.com/name/{first_name}-{last_name}",
        "Spokeo": f"https://www.spokeo.com/{first_name}-{last_name}",
        "Pipl": f"https://pipl.com/search/?q={full_name}",
        "192.com": f"https://www.192.com/people/{first_name}-{last_name}",
        "GitHub": f"https://github.com/search?q={full_name}&type=users",
        "YouTube": f"https://www.youtube.com/results?search_query={full_name}",
        "Reddit": f"https://www.reddit.com/search/?q={full_name}",
        "Medium": f"https://medium.com/search?q={full_name}",
        "Quora": f"https://www.quora.com/search?q={full_name}",
    }
    
    for site, url in search_links.items():
        print(f"{Colors.SUCCESS}→ {site:20} : {url}{Colors.RESET}")
    
    return search_links

def generate_possible_usernames(first_name, last_name):
    """Olası kullanıcı adları oluştur"""
    print(f"\n{Colors.INFO}[*] Olası kullanıcı adları oluşturuluyor...{Colors.RESET}\n")
    
    first = first_name.lower()
    last = last_name.lower()
    
    usernames = [
        f"{first}{last}",
        f"{first}.{last}",
        f"{first}_{last}",
        f"{first}-{last}",
        f"{last}{first}",
        f"{last}.{first}",
        f"{last}_{first}",
        f"{first}{last[0]}",
        f"{first[0]}{last}",
        f"{first}",
        f"{last}",
        f"{first}{last}123",
        f"{first}.{last}.official",
        f"_{first}{last}_",
    ]
    
    print(f"{Colors.SUCCESS}Oluşturulan {len(usernames)} olası kullanıcı adı:{Colors.RESET}")
    for i, username in enumerate(usernames, 1):
        print(f"{Colors.INFO}  {i:2}. {username}{Colors.RESET}")
    
    return usernames

def generate_possible_emails(first_name, last_name):
    """Olası e-posta adresleri oluştur"""
    print(f"\n{Colors.INFO}[*] Olası e-posta adresleri oluşturuluyor...{Colors.RESET}\n")
    
    first = first_name.lower()
    last = last_name.lower()
    
    domains = ['gmail.com', 'hotmail.com', 'yahoo.com', 'outlook.com', 'icloud.com', 'protonmail.com']
    
    email_patterns = []
    for domain in domains:
        email_patterns.extend([
            f"{first}.{last}@{domain}",
            f"{first}_{last}@{domain}",
            f"{first}{last}@{domain}",
            f"{first}@{domain}",
            f"{first[0]}{last}@{domain}",
        ])
    
    print(f"{Colors.SUCCESS}Oluşturulan {len(email_patterns)} olası e-posta:{Colors.RESET}")
    for i, email in enumerate(email_patterns[:20], 1):  # İlk 20'yi göster
        print(f"{Colors.INFO}  {i:2}. {email}{Colors.RESET}")
    
    if len(email_patterns) > 20:
        print(f"{Colors.WARNING}  ... ve {len(email_patterns) - 20} e-posta daha{Colors.RESET}")
    
    return email_patterns

def search_person(first_name, last_name):
    """Kapsamlı kişi araştırması"""
    results = {
        'first_name': first_name,
        'last_name': last_name,
        'search_links': None,
        'usernames': None,
        'emails': None,
        'timestamp': datetime.now()
    }
    
    # Online araştırma linkleri
    results['search_links'] = search_person_online(first_name, last_name)
    
    # Olası kullanıcı adları
    results['usernames'] = generate_possible_usernames(first_name, last_name)
    
    # Olası e-posta adresleri
    results['emails'] = generate_possible_emails(first_name, last_name)
    
    return results

def save_report(results):
    """Raporu kaydet"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = BASE_DIR / 'reports' / 'person_search'
    report_dir.mkdir(parents=True, exist_ok=True)
    
    name_safe = f"{results['first_name']}_{results['last_name']}"
    report_file = report_dir / f"{name_safe}_{timestamp}.txt"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("╔═══════════════════════════════════════════════════════════════╗\n")
        f.write("║                HIG-OSINT KİŞİ ARAŞTIRMA RAPORU                ║\n")
        f.write("╚═══════════════════════════════════════════════════════════════╝\n\n")
        f.write(f"Ad      : {results['first_name']}\n")
        f.write(f"Soyad   : {results['last_name']}\n")
        f.write(f"Tarih   : {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n")
        f.write("="*65 + "\n\n")
        
        # Arama linkleri
        f.write("ONLINE ARAŞTIRMA LİNKLERİ:\n")
        f.write("-"*65 + "\n")
        for site, url in results['search_links'].items():
            f.write(f"→ {site:20} : {url}\n")
        f.write("\n")
        
        # Kullanıcı adları
        f.write("OLASI KULLANICI ADLARI:\n")
        f.write("-"*65 + "\n")
        for i, username in enumerate(results['usernames'], 1):
            f.write(f"{i:2}. {username}\n")
        f.write("\n")
        
        # E-posta adresleri
        f.write("OLASI E-POSTA ADRESLERİ:\n")
        f.write("-"*65 + "\n")
        for i, email in enumerate(results['emails'], 1):
            f.write(f"{i:2}. {email}\n")
        
        f.write("\n" + "="*65 + "\n")
        f.write(f"\nRapor Dosyası: {report_file}\n")
    
    return report_file

def main():
    """Ana fonksiyon"""
    os.system('clear' if os.name != 'nt' else 'cls')
    print_header()
    
    print(f"{Colors.INFO}Bu modül kişi ismi ile online araştırma yapar ve olası kullanıcı adları/e-postalar üretir.{Colors.RESET}\n")
    
    first_name = input(f"{Colors.INPUT}Ad: {Colors.RESET}").strip()
    last_name = input(f"{Colors.INPUT}Soyad: {Colors.RESET}").strip()
    
    if not first_name or not last_name:
        print(f"{Colors.ERROR}[!] Ad ve soyad boş olamaz!{Colors.RESET}")
        return
    
    # Araştırma
    results = search_person(first_name, last_name)
    
    # Özet
    print(f"\n{Colors.HEADER}╔════════════════════ SONUÇ ÖZETİ ══════════════════════╗{Colors.RESET}")
    print(f"{Colors.SUCCESS}Araştırma Linkleri : {len(results['search_links'])} adet{Colors.RESET}")
    print(f"{Colors.SUCCESS}Olası Kullanıcı Adı: {len(results['usernames'])} adet{Colors.RESET}")
    print(f"{Colors.SUCCESS}Olası E-posta      : {len(results['emails'])} adet{Colors.RESET}")
    print(f"{Colors.HEADER}╚════════════════════════════════════════════════════════╝{Colors.RESET}\n")
    
    save = input(f"{Colors.INPUT}Raporu kaydetmek ister misiniz? (E/H): {Colors.RESET}").strip().upper()
    if save in ['E', 'Y', 'EVET', 'YES']:
        report_file = save_report(results)
        print(f"\n{Colors.SUCCESS}✓ Rapor kaydedildi: {report_file}{Colors.RESET}")
    
    input(f"\n{Colors.INPUT}Ana menüye dönmek için Enter'a basın...{Colors.RESET}")

if __name__ == "__main__":
    main()
