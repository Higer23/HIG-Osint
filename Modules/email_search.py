#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HIG-Osint Email Search Module
E-posta adresi araştırması ve doğrulama
"""

import os
import sys
import re
import dns.resolver
import socket
from pathlib import Path
from colorama import Fore, Style
from datetime import datetime
import requests
import json

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
║              📧 E-POSTA ARAŞTIRMA MODÜLÜ 📧                 ║
╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(header)

def validate_email_format(email):
    """E-posta formatını kontrol et"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def check_mx_record(domain):
    """MX kaydını kontrol et"""
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        return True, [str(mx.exchange) for mx in mx_records]
    except Exception as e:
        return False, str(e)

def check_smtp_server(email):
    """SMTP sunucusunu kontrol et"""
    domain = email.split('@')[1]
    
    try:
        mx_exists, mx_records = check_mx_record(domain)
        
        if not mx_exists:
            return False, "MX kaydı bulunamadı"
        
        mx_host = str(mx_records[0]).rstrip('.')
        
        # SMTP bağlantısı
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.settimeout(10)
        server.connect((mx_host, 25))
        server.recv(1024)
        server.send(b'HELO higosint.com\r\n')
        server.recv(1024)
        server.send(f'MAIL FROM: <verify@higosint.com>\r\n'.encode())
        server.recv(1024)
        server.send(f'RCPT TO: <{email}>\r\n'.encode())
        response = server.recv(1024).decode()
        server.send(b'QUIT\r\n')
        server.close()
        
        if '250' in response or '251' in response:
            return True, "E-posta adresi geçerli görünüyor"
        else:
            return False, "E-posta adresi bulunamadı"
            
    except Exception as e:
        return None, f"SMTP kontrolü başarısız: {str(e)}"

def check_data_breaches(email):
    """Veri ihlallerini kontrol et (Have I Been Pwned API)"""
    try:
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
        headers = {
            'User-Agent': 'HIG-Osint',
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            breaches = response.json()
            return True, breaches
        elif response.status_code == 404:
            return False, "Veri ihlali bulunamadı"
        else:
            return None, f"API hatası: {response.status_code}"
            
    except Exception as e:
        return None, f"Kontrol başarısız: {str(e)}"

def search_google(email):
    """Google'da e-posta ara"""
    search_query = f'"{email}"'
    print(f"{Colors.INFO}[*] Google aramasi: {search_query}{Colors.RESET}")
    return f"https://www.google.com/search?q={email}"

def check_social_media(email):
    """Sosyal medya hesaplarını kontrol et"""
    username = email.split('@')[0]
    
    social_sites = {
        "GitHub": f"https://github.com/{username}",
        "Twitter": f"https://twitter.com/{username}",
        "Instagram": f"https://instagram.com/{username}",
        "LinkedIn": f"https://linkedin.com/in/{username}",
    }
    
    found_accounts = []
    
    for site, url in social_sites.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                found_accounts.append((site, url))
        except:
            pass
    
    return found_accounts

def analyze_email(email):
    """E-posta adresini analiz et"""
    print(f"\n{Colors.INFO}[*] E-posta analizi başlatılıyor...{Colors.RESET}\n")
    
    results = {
        'email': email,
        'format_valid': False,
        'mx_valid': False,
        'smtp_valid': None,
        'breaches': None,
        'social_accounts': [],
        'google_search': None
    }
    
    # Format kontrolü
    print(f"{Colors.INFO}[1/6] Format kontrol ediliyor...{Colors.RESET}")
    if validate_email_format(email):
        results['format_valid'] = True
        print(f"{Colors.SUCCESS}✓ E-posta formatı geçerli{Colors.RESET}")
    else:
        print(f"{Colors.ERROR}✗ Geçersiz e-posta formatı{Colors.RESET}")
        return results
    
    # MX kaydı kontrolü
    print(f"{Colors.INFO}[2/6] MX kaydı kontrol ediliyor...{Colors.RESET}")
    domain = email.split('@')[1]
    mx_valid, mx_info = check_mx_record(domain)
    results['mx_valid'] = mx_valid
    
    if mx_valid:
        print(f"{Colors.SUCCESS}✓ MX kaydı bulundu: {', '.join(mx_info)}{Colors.RESET}")
    else:
        print(f"{Colors.ERROR}✗ MX kaydı bulunamadı: {mx_info}{Colors.RESET}")
    
    # SMTP kontrolü
    print(f"{Colors.INFO}[3/6] SMTP sunucusu kontrol ediliyor...{Colors.RESET}")
    smtp_valid, smtp_msg = check_smtp_server(email)
    results['smtp_valid'] = smtp_valid
    
    if smtp_valid is True:
        print(f"{Colors.SUCCESS}✓ {smtp_msg}{Colors.RESET}")
    elif smtp_valid is False:
        print(f"{Colors.WARNING}⚠ {smtp_msg}{Colors.RESET}")
    else:
        print(f"{Colors.ERROR}✗ {smtp_msg}{Colors.RESET}")
    
    # Veri ihlali kontrolü
    print(f"{Colors.INFO}[4/6] Veri ihlalleri kontrol ediliyor...{Colors.RESET}")
    breach_found, breach_info = check_data_breaches(email)
    results['breaches'] = breach_info
    
    if breach_found is True:
        print(f"{Colors.ERROR}⚠ VERİ İHLALİ BULUNDU! {len(breach_info)} ihlal tespit edildi{Colors.RESET}")
    elif breach_found is False:
        print(f"{Colors.SUCCESS}✓ Veri ihlali bulunamadı{Colors.RESET}")
    else:
        print(f"{Colors.WARNING}? {breach_info}{Colors.RESET}")
    
    # Sosyal medya kontrolü
    print(f"{Colors.INFO}[5/6] Sosyal medya hesapları aranıyor...{Colors.RESET}")
    social_accounts = check_social_media(email)
    results['social_accounts'] = social_accounts
    
    if social_accounts:
        print(f"{Colors.SUCCESS}✓ {len(social_accounts)} sosyal medya hesabı bulundu{Colors.RESET}")
        for site, url in social_accounts:
            print(f"  → {site}: {url}")
    else:
        print(f"{Colors.WARNING}✗ Sosyal medya hesabı bulunamadı{Colors.RESET}")
    
    # Google arama linki
    print(f"{Colors.INFO}[6/6] Google arama linki oluşturuluyor...{Colors.RESET}")
    results['google_search'] = search_google(email)
    print(f"{Colors.SUCCESS}✓ Google arama: {results['google_search']}{Colors.RESET}")
    
    return results

def save_report(results):
    """Raporu kaydet"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = BASE_DIR / 'reports' / 'email_search'
    report_dir.mkdir(parents=True, exist_ok=True)
    
    email_safe = results['email'].replace('@', '_at_').replace('.', '_')
    report_file = report_dir / f"{email_safe}_{timestamp}.txt"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("╔═══════════════════════════════════════════════════════════════╗\n")
        f.write("║                HIG-OSINT E-POSTA RAPORU                       ║\n")
        f.write("╚═══════════════════════════════════════════════════════════════╝\n\n")
        f.write(f"E-posta Adresi: {results['email']}\n")
        f.write(f"Tarih: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n")
        f.write("="*65 + "\n\n")
        
        f.write("DOĞRULAMA SONUÇLARI:\n")
        f.write(f"Format Geçerli    : {'✓ Evet' if results['format_valid'] else '✗ Hayır'}\n")
        f.write(f"MX Kaydı Geçerli  : {'✓ Evet' if results['mx_valid'] else '✗ Hayır'}\n")
        
        if results['smtp_valid'] is True:
            f.write(f"SMTP Geçerli      : ✓ Evet\n")
        elif results['smtp_valid'] is False:
            f.write(f"SMTP Geçerli      : ✗ Hayır\n")
        else:
            f.write(f"SMTP Geçerli      : ? Bilinmiyor\n")
        
        f.write("\n" + "-"*65 + "\n\n")
        
        if isinstance(results['breaches'], list) and results['breaches']:
            f.write("VERİ İHLALLERİ:\n")
            for breach in results['breaches']:
                f.write(f"  • {breach.get('Name', 'Bilinmeyen')}\n")
                f.write(f"    Tarih: {breach.get('BreachDate', 'Bilinmiyor')}\n")
                f.write(f"    Açıklama: {breach.get('Description', 'Yok')}\n\n")
        
        if results['social_accounts']:
            f.write("-"*65 + "\n\n")
            f.write("SOSYAL MEDYA HESAPLARI:\n")
            for site, url in results['social_accounts']:
                f.write(f"  ✓ {site}: {url}\n")
        
        f.write("\n" + "-"*65 + "\n\n")
        f.write(f"Google Arama: {results['google_search']}\n")
        f.write(f"\nRapor Dosyası: {report_file}\n")
    
    return report_file

def main():
    """Ana fonksiyon"""
    os.system('clear' if os.name != 'nt' else 'cls')
    print_header()
    
    email = input(f"{Colors.INPUT}Araştırılacak e-posta adresini girin: {Colors.RESET}").strip()
    
    if not email:
        print(f"{Colors.ERROR}[!] E-posta adresi boş olamaz!{Colors.RESET}")
        return
    
    results = analyze_email(email)
    
    # Özet
    print(f"\n{Colors.HEADER}╔════════════════════ SONUÇ ÖZETİ ══════════════════════╗{Colors.RESET}")
    print(f"{Colors.SUCCESS}Format Geçerli     : {'✓ Evet' if results['format_valid'] else '✗ Hayır'}{Colors.RESET}")
    print(f"{Colors.SUCCESS}MX Kaydı Var       : {'✓ Evet' if results['mx_valid'] else '✗ Hayır'}{Colors.RESET}")
    
    smtp_status = "✓ Geçerli" if results['smtp_valid'] is True else ("✗ Geçersiz" if results['smtp_valid'] is False else "? Bilinmiyor")
    print(f"{Colors.SUCCESS}SMTP Durumu        : {smtp_status}{Colors.RESET}")
    
    if isinstance(results['breaches'], list):
        breach_count = len(results['breaches'])
        color = Colors.ERROR if breach_count > 0 else Colors.SUCCESS
        print(f"{color}Veri İhlali        : {breach_count} adet{Colors.RESET}")
    
    print(f"{Colors.SUCCESS}Sosyal Medya       : {len(results['social_accounts'])} hesap bulundu{Colors.RESET}")
    print(f"{Colors.HEADER}╚════════════════════════════════════════════════════════╝{Colors.RESET}\n")
    
    save = input(f"{Colors.INPUT}Raporu kaydetmek ister misiniz? (E/H): {Colors.RESET}").strip().upper()
    if save in ['E', 'Y', 'EVET', 'YES']:
        report_file = save_report(results)
        print(f"\n{Colors.SUCCESS}✓ Rapor kaydedildi: {report_file}{Colors.RESET}")
    
    input(f"\n{Colors.INPUT}Ana menüye dönmek için Enter'a basın...{Colors.RESET}")

if __name__ == "__main__":
    main()
