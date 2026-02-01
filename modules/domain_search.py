#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HIG-Osint Domain Search Module
Domain/Website araştırması, WHOIS, DNS, SSL analizi
"""

import os
import sys
import socket
import ssl
import requests
from pathlib import Path
from colorama import Fore, Style
from datetime import datetime
from urllib.parse import urlparse

try:
    import whois
    import dns.resolver
except ImportError:
    print("[!] Gerekli modüller yükleniyor...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-whois", "dnspython", "--break-system-packages"])
    import whois
    import dns.resolver

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
║           🏢 DOMAIN/WEBSITE ARAŞTIRMA MODÜLÜ 🏢            ║
╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(header)

def clean_domain(domain):
    """Domain adresini temizle"""
    domain = domain.strip().lower()
    if domain.startswith('http://') or domain.startswith('https://'):
        parsed = urlparse(domain)
        domain = parsed.netloc or parsed.path
    if domain.startswith('www.'):
        domain = domain[4:]
    if '/' in domain:
        domain = domain.split('/')[0]
    return domain

def get_whois_info(domain):
    """WHOIS bilgilerini al"""
    print(f"{Colors.INFO}[1/6] WHOIS bilgileri alınıyor...{Colors.RESET}")
    try:
        w = whois.whois(domain)
        whois_data = {
            'domain_name': w.domain_name if isinstance(w.domain_name, str) else (w.domain_name[0] if w.domain_name else None),
            'registrar': w.registrar,
            'creation_date': w.creation_date if isinstance(w.creation_date, datetime) else (w.creation_date[0] if isinstance(w.creation_date, list) else None),
            'expiration_date': w.expiration_date if isinstance(w.expiration_date, datetime) else (w.expiration_date[0] if isinstance(w.expiration_date, list) else None),
            'name_servers': w.name_servers if isinstance(w.name_servers, list) else [w.name_servers] if w.name_servers else [],
            'org': w.org,
            'country': w.country,
        }
        print(f"{Colors.SUCCESS}✓ WHOIS bilgileri alındı{Colors.RESET}")
        print(f"  → Kayıt Şirketi: {whois_data['registrar']}")
        return True, whois_data
    except Exception as e:
        print(f"{Colors.ERROR}✗ WHOIS başarısız: {e}{Colors.RESET}")
        return False, None

def get_dns_records(domain):
    """DNS kayıtlarını al"""
    print(f"\n{Colors.INFO}[2/6] DNS kayıtları sorgulanıyor...{Colors.RESET}")
    dns_data = {'A': [], 'MX': [], 'NS': [], 'TXT': []}
    for record_type in dns_data.keys():
        try:
            answers = dns.resolver.resolve(domain, record_type)
            for rdata in answers:
                dns_data[record_type].append(str(rdata))
            print(f"{Colors.SUCCESS}✓ {record_type:3} kayıtları: {len(dns_data[record_type])} adet{Colors.RESET}")
        except:
            pass
    return True, dns_data

def get_ip_info(domain):
    """IP ve konum bilgisi"""
    print(f"\n{Colors.INFO}[3/6] IP adresi sorgulanıyor...{Colors.RESET}")
    try:
        ip_address = socket.gethostbyname(domain)
        response = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=10)
        if response.status_code == 200:
            ip_data = response.json()
            print(f"{Colors.SUCCESS}✓ IP: {ip_address} - {ip_data.get('country')}{Colors.RESET}")
            return True, {'ip': ip_address, 'country': ip_data.get('country'), 'city': ip_data.get('city'), 'isp': ip_data.get('isp')}
    except Exception as e:
        print(f"{Colors.ERROR}✗ IP sorgulaması başarısız{Colors.RESET}")
    return False, None

def analyze_domain(domain):
    """Domain analizi"""
    results = {'domain': domain, 'whois': None, 'dns': None, 'ip': None}
    success, data = get_whois_info(domain)
    if success: results['whois'] = data
    success, data = get_dns_records(domain)
    if success: results['dns'] = data
    success, data = get_ip_info(domain)
    if success: results['ip'] = data
    return results

def save_report(results):
    """Raporu kaydet"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = BASE_DIR / 'reports' / 'domain_search'
    report_dir.mkdir(parents=True, exist_ok=True)
    domain_safe = results['domain'].replace('.', '_')
    report_file = report_dir / f"{domain_safe}_{timestamp}.txt"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("╔═══════════════════════════════════════════════════════════════╗\n")
        f.write("║               HIG-OSINT DOMAIN ARAŞTIRMA RAPORU               ║\n")
        f.write("╚═══════════════════════════════════════════════════════════════╝\n\n")
        f.write(f"Domain: {results['domain']}\n")
        f.write(f"Tarih: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n")
        
        if results['whois']:
            f.write("WHOIS:\n" + "-"*65 + "\n")
            w = results['whois']
            if w.get('registrar'): f.write(f"Kayıt Şirketi: {w['registrar']}\n")
            if w.get('creation_date'): f.write(f"Oluşturma: {w['creation_date']}\n")
            f.write("\n")
        
        if results['dns']:
            f.write("DNS KAYITLARI:\n" + "-"*65 + "\n")
            for rtype, records in results['dns'].items():
                if records: f.write(f"{rtype}: {', '.join(records)}\n")
            f.write("\n")
        
        if results['ip']:
            f.write("IP BİLGİSİ:\n" + "-"*65 + "\n")
            ip = results['ip']
            f.write(f"IP: {ip.get('ip')}\nÜlke: {ip.get('country')}\nŞehir: {ip.get('city')}\nISP: {ip.get('isp')}\n")
        
        f.write(f"\nRapor: {report_file}\n")
    return report_file

def main():
    """Ana fonksiyon"""
    os.system('clear' if os.name != 'nt' else 'cls')
    print_header()
    
    domain = input(f"{Colors.INPUT}Domain adresini girin: {Colors.RESET}").strip()
    if not domain:
        print(f"{Colors.ERROR}[!] Domain boş olamaz!{Colors.RESET}")
        return
    
    domain = clean_domain(domain)
    results = analyze_domain(domain)
    
    print(f"\n{Colors.HEADER}╔════════════════════ ÖZET ══════════════════════╗{Colors.RESET}")
    print(f"{Colors.SUCCESS}WHOIS: {'✓' if results['whois'] else '✗'} | DNS: {'✓' if results['dns'] else '✗'} | IP: {'✓' if results['ip'] else '✗'}{Colors.RESET}")
    print(f"{Colors.HEADER}╚════════════════════════════════════════════════╝{Colors.RESET}\n")
    
    save = input(f"{Colors.INPUT}Rapor kaydet? (E/H): {Colors.RESET}").strip().upper()
    if save in ['E', 'Y', 'EVET', 'YES']:
        report_file = save_report(results)
        print(f"\n{Colors.SUCCESS}✓ Rapor: {report_file}{Colors.RESET}")
    
    input(f"\n{Colors.INPUT}Ana menüye dönmek için Enter...{Colors.RESET}")

if __name__ == "__main__":
    main()
