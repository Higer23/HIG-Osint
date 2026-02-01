#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advanced Tools Module - Gelişmiş OSINT Araçları
Bu modül çeşitli gelişmiş OSINT araçlarını içerir
"""

import os
import sys
import json
import hashlib
import base64
import socket
import ssl
import whois
import dns.resolver
import requests
from datetime import datetime
from colorama import Fore, Style
from pathlib import Path

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
║                    GELİŞMİŞ ARAÇLAR MOD��LÜ                       ║
║                  Advanced OSINT Tools Module                     ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(header)

def save_result(filename, data):
    """Sonuçları kaydet"""
    try:
        reports_dir = Path('reports')
        reports_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = reports_dir / f"{filename}_{timestamp}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"{Colors.SUCCESS}[+] Sonuçlar kaydedildi: {filepath}{Colors.RESET}")
        return True
    except Exception as e:
        print(f"{Colors.ERROR}[-] Kayıt hatası: {e}{Colors.RESET}")
        return False

def check_ssl_certificate(domain):
    """SSL sertifika bilgilerini al"""
    print(f"\n{Colors.INFO}[*] SSL sertifikası kontrol ediliyor: {domain}{Colors.RESET}")
    
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                
                result = {
                    'domain': domain,
                    'issuer': dict(x[0] for x in cert['issuer']),
                    'subject': dict(x[0] for x in cert['subject']),
                    'version': cert['version'],
                    'serial_number': cert['serialNumber'],
                    'not_before': cert['notBefore'],
                    'not_after': cert['notAfter'],
                    'san': cert.get('subjectAltName', [])
                }
                
                print(f"{Colors.SUCCESS}[+] SSL Sertifika Bilgileri:{Colors.RESET}")
                print(f"  - Verilen: {result['issuer'].get('organizationName', 'N/A')}")
                print(f"  - Konu: {result['subject'].get('commonName', 'N/A')}")
                print(f"  - Geçerlilik: {result['not_before']} → {result['not_after']}")
                print(f"  - SAN: {len(result['san'])} domain")
                
                return result
                
    except Exception as e:
        print(f"{Colors.ERROR}[-] SSL hatası: {e}{Colors.RESET}")
        return None

def dns_enumeration(domain):
    """DNS kayıtlarını sorgula"""
    print(f"\n{Colors.INFO}[*] DNS kayıtları sorgulanıyor: {domain}{Colors.RESET}")
    
    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME']
    results = {}
    
    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            results[record_type] = [str(rdata) for rdata in answers]
            print(f"{Colors.SUCCESS}[+] {record_type} kayıtları: {len(results[record_type])} adet{Colors.RESET}")
            for record in results[record_type]:
                print(f"    {record}")
        except dns.resolver.NoAnswer:
            results[record_type] = []
        except Exception as e:
            results[record_type] = [f"Hata: {str(e)}"]
    
    return results

def reverse_ip_lookup(ip):
    """Reverse IP lookup - aynı IP'deki diğer domainleri bul"""
    print(f"\n{Colors.INFO}[*] Reverse IP lookup yapılıyor: {ip}{Colors.RESET}")
    
    try:
        # HackerTarget API kullanarak
        url = f"https://api.hackertarget.com/reverseiplookup/?q={ip}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            domains = response.text.strip().split('\n')
            if domains and domains[0] != "error check your search parameter":
                print(f"{Colors.SUCCESS}[+] Bulunan domainler: {len(domains)} adet{Colors.RESET}")
                for domain in domains[:20]:  # İlk 20'yi göster
                    print(f"    {domain}")
                return domains
            else:
                print(f"{Colors.WARNING}[!] Sonuç bulunamadı{Colors.RESET}")
                return []
        else:
            print(f"{Colors.ERROR}[-] API hatası: {response.status_code}{Colors.RESET}")
            return []
            
    except Exception as e:
        print(f"{Colors.ERROR}[-] Hata: {e}{Colors.RESET}")
        return []

def encode_decode_tool():
    """Base64/Hash encoding/decoding aracı"""
    print(f"\n{Colors.MENU}=== Encode/Decode Aracı ==={Colors.RESET}")
    print(f"{Colors.INPUT}[1]{Colors.RESET} Base64 Encode")
    print(f"{Colors.INPUT}[2]{Colors.RESET} Base64 Decode")
    print(f"{Colors.INPUT}[3]{Colors.RESET} MD5 Hash")
    print(f"{Colors.INPUT}[4]{Colors.RESET} SHA256 Hash")
    print(f"{Colors.INPUT}[5]{Colors.RESET} SHA512 Hash")
    
    choice = input(f"\n{Colors.INPUT}Seçiminiz: {Colors.RESET}").strip()
    text = input(f"{Colors.INPUT}Metni girin: {Colors.RESET}").strip()
    
    try:
        if choice == '1':
            encoded = base64.b64encode(text.encode()).decode()
            print(f"{Colors.SUCCESS}[+] Base64: {encoded}{Colors.RESET}")
        elif choice == '2':
            decoded = base64.b64decode(text).decode()
            print(f"{Colors.SUCCESS}[+] Decoded: {decoded}{Colors.RESET}")
        elif choice == '3':
            hash_md5 = hashlib.md5(text.encode()).hexdigest()
            print(f"{Colors.SUCCESS}[+] MD5: {hash_md5}{Colors.RESET}")
        elif choice == '4':
            hash_sha256 = hashlib.sha256(text.encode()).hexdigest()
            print(f"{Colors.SUCCESS}[+] SHA256: {hash_sha256}{Colors.RESET}")
        elif choice == '5':
            hash_sha512 = hashlib.sha512(text.encode()).hexdigest()
            print(f"{Colors.SUCCESS}[+] SHA512: {hash_sha512}{Colors.RESET}")
        else:
            print(f"{Colors.ERROR}[-] Geçersiz seçim{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.ERROR}[-] Hata: {e}{Colors.RESET}")

def whois_lookup(domain):
    """WHOIS sorgusu"""
    print(f"\n{Colors.INFO}[*] WHOIS sorgusu yapılıyor: {domain}{Colors.RESET}")
    
    try:
        w = whois.whois(domain)
        
        print(f"{Colors.SUCCESS}[+] WHOIS Bilgileri:{Colors.RESET}")
        print(f"  - Domain Adı: {w.domain_name}")
        print(f"  - Kayıt Şirketi: {w.registrar}")
        print(f"  - Oluşturma Tarihi: {w.creation_date}")
        print(f"  - Son Güncelleme: {w.updated_date}")
        print(f"  - Son Kullanma: {w.expiration_date}")
        print(f"  - Name Servers: {w.name_servers}")
        print(f"  - Durum: {w.status}")
        
        return {
            'domain_name': str(w.domain_name),
            'registrar': str(w.registrar),
            'creation_date': str(w.creation_date),
            'expiration_date': str(w.expiration_date),
            'name_servers': [str(ns) for ns in w.name_servers] if w.name_servers else []
        }
        
    except Exception as e:
        print(f"{Colors.ERROR}[-] WHOIS hatası: {e}{Colors.RESET}")
        return None

def http_header_analysis(url):
    """HTTP header analizi"""
    print(f"\n{Colors.INFO}[*] HTTP header analizi yapılıyor: {url}{Colors.RESET}")
    
    try:
        response = requests.get(url, timeout=10, allow_redirects=False)
        
        print(f"{Colors.SUCCESS}[+] HTTP Başlıkları:{Colors.RESET}")
        print(f"  - Status Code: {response.status_code}")
        print(f"  - Server: {response.headers.get('Server', 'N/A')}")
        print(f"  - Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        print(f"  - X-Powered-By: {response.headers.get('X-Powered-By', 'N/A')}")
        print(f"  - X-Frame-Options: {response.headers.get('X-Frame-Options', 'N/A')}")
        
        # Güvenlik başlıkları kontrolü
        security_headers = [
            'Strict-Transport-Security',
            'Content-Security-Policy',
            'X-Content-Type-Options',
            'X-XSS-Protection'
        ]
        
        print(f"\n{Colors.INFO}[*] Güvenlik Başlıkları:{Colors.RESET}")
        for header in security_headers:
            if header in response.headers:
                print(f"  {Colors.SUCCESS}✓ {header}: {response.headers[header]}{Colors.RESET}")
            else:
                print(f"  {Colors.WARNING}✗ {header}: Yok{Colors.RESET}")
        
        return dict(response.headers)
        
    except Exception as e:
        print(f"{Colors.ERROR}[-] HTTP hatası: {e}{Colors.RESET}")
        return None

def advanced_tools_menu():
    """Gelişmiş araçlar menüsü"""
    while True:
        clear_screen()
        print_header()
        
        menu = f"""{Colors.MENU}
╔═══════════════════════════════════════════════════════════════╗
║                   GELİŞMİŞ ARAÇLAR MENÜSÜ                    ║
╚═══════════════════════════════════════════════════════════════╝

  {Colors.INPUT}[1]{Colors.RESET} 🔒 SSL Sertifika Analizi
  {Colors.INPUT}[2]{Colors.RESET} 🌐 DNS Kayıt Sorgulaması
  {Colors.INPUT}[3]{Colors.RESET} 🔄 Reverse IP Lookup
  {Colors.INPUT}[4]{Colors.RESET} 🔐 Encode/Decode Araçları
  {Colors.INPUT}[5]{Colors.RESET} 📋 WHOIS Sorgusu
  {Colors.INPUT}[6]{Colors.RESET} 📡 HTTP Header Analizi
  {Colors.INPUT}[0]{Colors.RESET} 🔙 Ana Menüye Dön

{Colors.INPUT}Seçiminiz: {Colors.RESET}"""
        
        print(menu, end='')
        choice = input().strip()
        
        if choice == '0':
            break
        elif choice == '1':
            domain = input(f"\n{Colors.INPUT}Domain adı girin: {Colors.RESET}").strip()
            if domain:
                result = check_ssl_certificate(domain)
                if result:
                    save_result(f"ssl_{domain}", result)
        elif choice == '2':
            domain = input(f"\n{Colors.INPUT}Domain adı girin: {Colors.RESET}").strip()
            if domain:
                result = dns_enumeration(domain)
                save_result(f"dns_{domain}", result)
        elif choice == '3':
            ip = input(f"\n{Colors.INPUT}IP adresi girin: {Colors.RESET}").strip()
            if ip:
                result = reverse_ip_lookup(ip)
                if result:
                    save_result(f"reverseip_{ip}", {'ip': ip, 'domains': result})
        elif choice == '4':
            encode_decode_tool()
        elif choice == '5':
            domain = input(f"\n{Colors.INPUT}Domain adı girin: {Colors.RESET}").strip()
            if domain:
                result = whois_lookup(domain)
                if result:
                    save_result(f"whois_{domain}", result)
        elif choice == '6':
            url = input(f"\n{Colors.INPUT}URL girin (http://... veya https://...): {Colors.RESET}").strip()
            if url:
                result = http_header_analysis(url)
                if result:
                    save_result(f"http_headers_{url.replace('://', '_').replace('/', '_')}", result)
        else:
            print(f"{Colors.ERROR}[-] Geçersiz seçim!{Colors.RESET}")
        
        input(f"\n{Colors.INPUT}Devam etmek için Enter'a basın...{Colors.RESET}")

def main():
    """Ana fonksiyon"""
    try:
        advanced_tools_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}[!] İşlem iptal edildi{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.ERROR}[-] Beklenmeyen hata: {e}{Colors.RESET}")

if __name__ == "__main__":
    main()
