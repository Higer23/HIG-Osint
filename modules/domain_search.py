#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Domain Search Module - Kapsamlı Domain/Website Araştırma Modülü
Gelişmiş domain analizi, WHOIS, DNS, SSL, subdomain, teknoloji tespiti
"""

import os
import sys
import json
import socket
import ssl
import requests
import dns.resolver
import dns.zone
import dns.query
from datetime import datetime
from pathlib import Path
from colorama import Fore, Style
import re
import hashlib
import base64
from urllib.parse import urlparse, urljoin
import threading
from queue import Queue
import time

try:
    import whois
except ImportError:
    print("[!] python-whois modülü yükleniyor...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-whois", "--break-system-packages"])
    import whois

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("[!] beautifulsoup4 modülü yükleniyor...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4", "--break-system-packages"])
    from bs4 import BeautifulSoup

class Colors:
    HEADER = Fore.CYAN + Style.BRIGHT
    INFO = Fore.BLUE + Style.BRIGHT
    SUCCESS = Fore.GREEN + Style.BRIGHT
    WARNING = Fore.YELLOW + Style.BRIGHT
    ERROR = Fore.RED + Style.BRIGHT
    MENU = Fore.MAGENTA + Style.BRIGHT
    INPUT = Fore.WHITE + Style.BRIGHT
    RESET = Style.RESET_ALL

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    header = f"""{Colors.HEADER}
╔═══════════════════════════════════════════════════════════════════╗
║                  DOMAIN ARAŞTIRMA MODÜLÜ                         ║
║            Advanced Domain/Website Research Module               ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(header)

def save_result(filename, data):
    try:
        reports_dir = Path('reports')
        reports_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = reports_dir / f"domain_{filename}_{timestamp}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"{Colors.SUCCESS}[+] Sonuçlar kaydedildi: {filepath}{Colors.RESET}")
        return filepath
    except Exception as e:
        print(f"{Colors.ERROR}[-] Kayıt hatası: {e}{Colors.RESET}")
        return None

def whois_lookup(domain):
    """Detaylı WHOIS sorgusu"""
    print(f"\n{Colors.INFO}[*] WHOIS sorgusu yapılıyor: {domain}{Colors.RESET}")
    try:
        w = whois.whois(domain)
        result = {
            'domain_name': str(w.domain_name) if w.domain_name else 'N/A',
            'registrar': str(w.registrar) if w.registrar else 'N/A',
            'whois_server': str(w.whois_server) if hasattr(w, 'whois_server') and w.whois_server else 'N/A',
            'creation_date': str(w.creation_date) if w.creation_date else 'N/A',
            'expiration_date': str(w.expiration_date) if w.expiration_date else 'N/A',
            'updated_date': str(w.updated_date) if w.updated_date else 'N/A',
            'name_servers': [str(ns) for ns in w.name_servers] if w.name_servers else [],
            'status': [str(s) for s in w.status] if w.status else [],
            'emails': [str(e) for e in w.emails] if w.emails else [],
            'org': str(w.org) if hasattr(w, 'org') and w.org else 'N/A',
            'country': str(w.country) if hasattr(w, 'country') and w.country else 'N/A',
            'state': str(w.state) if hasattr(w, 'state') and w.state else 'N/A',
            'city': str(w.city) if hasattr(w, 'city') and w.city else 'N/A',
            'address': str(w.address) if hasattr(w, 'address') and w.address else 'N/A',
            'zipcode': str(w.zipcode) if hasattr(w, 'zipcode') and w.zipcode else 'N/A',
            'registrant_name': str(w.name) if hasattr(w, 'name') and w.name else 'N/A'
        }
        
        print(f"{Colors.SUCCESS}[+] WHOIS Bilgileri:{Colors.RESET}")
        print(f"  - Domain: {result['domain_name']}")
        print(f"  - Kayıt Şirketi: {result['registrar']}")
        print(f"  - Oluşturma: {result['creation_date']}")
        print(f"  - Son Kullanma: {result['expiration_date']}")
        print(f"  - Güncelleme: {result['updated_date']}")
        print(f"  - Organizasyon: {result['org']}")
        print(f"  - Ülke: {result['country']}")
        print(f"  - Name Servers: {len(result['name_servers'])} adet")
        for ns in result['name_servers']:
            print(f"    • {ns}")
        print(f"  - E-postalar: {', '.join(result['emails']) if result['emails'] else 'Yok'}")
        print(f"  - Durum: {', '.join(result['status'][:3]) if result['status'] else 'Yok'}")
        
        return result
    except Exception as e:
        print(f"{Colors.ERROR}[-] WHOIS hatası: {e}{Colors.RESET}")
        return None

def dns_enumeration(domain):
    """Kapsamlı DNS kayıt sorgulaması"""
    print(f"\n{Colors.INFO}[*] DNS kayıtları sorgulanıyor: {domain}{Colors.RESET}")
    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME', 'PTR', 'SRV', 'CAA']
    results = {}
    
    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            results[record_type] = []
            for rdata in answers:
                if record_type == 'MX':
                    results[record_type].append({
                        'priority': rdata.preference,
                        'exchange': str(rdata.exchange)
                    })
                elif record_type == 'SOA':
                    results[record_type].append({
                        'mname': str(rdata.mname),
                        'rname': str(rdata.rname),
                        'serial': rdata.serial,
                        'refresh': rdata.refresh,
                        'retry': rdata.retry,
                        'expire': rdata.expire,
                        'minimum': rdata.minimum
                    })
                elif record_type == 'SRV':
                    results[record_type].append({
                        'priority': rdata.priority,
                        'weight': rdata.weight,
                        'port': rdata.port,
                        'target': str(rdata.target)
                    })
                else:
                    results[record_type].append(str(rdata))
            
            print(f"{Colors.SUCCESS}[+] {record_type}: {len(results[record_type])} kayıt{Colors.RESET}")
            for record in results[record_type][:5]:
                if isinstance(record, dict):
                    print(f"    • {record}")
                else:
                    print(f"    • {record}")
        except dns.resolver.NoAnswer:
            results[record_type] = []
        except dns.resolver.NXDOMAIN:
            print(f"{Colors.ERROR}[-] Domain bulunamadı!{Colors.RESET}")
            return None
        except Exception as e:
            results[record_type] = []
    
    return results

def ssl_certificate_info(domain):
    """Detaylı SSL sertifika analizi"""
    print(f"\n{Colors.INFO}[*] SSL sertifikası analiz ediliyor: {domain}{Colors.RESET}")
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                
                result = {
                    'version': cert.get('version', 'N/A'),
                    'serial_number': cert.get('serialNumber', 'N/A'),
                    'issuer': dict(x[0] for x in cert.get('issuer', [])),
                    'subject': dict(x[0] for x in cert.get('subject', [])),
                    'not_before': cert.get('notBefore', 'N/A'),
                    'not_after': cert.get('notAfter', 'N/A'),
                    'san': [x[1] for x in cert.get('subjectAltName', [])],
                    'signature_algorithm': cert.get('signatureAlgorithm', 'N/A'),
                    'cipher': ssock.cipher(),
                    'tls_version': ssock.version()
                }
                
                print(f"{Colors.SUCCESS}[+] SSL/TLS Bilgileri:{Colors.RESET}")
                print(f"  - Sertifika Veren: {result['issuer'].get('organizationName', 'N/A')}")
                print(f"  - Konu CN: {result['subject'].get('commonName', 'N/A')}")
                print(f"  - Geçerlilik: {result['not_before']} → {result['not_after']}")
                print(f"  - TLS Versiyon: {result['tls_version']}")
                print(f"  - Cipher: {result['cipher']}")
                print(f"  - SAN Domains: {len(result['san'])} adet")
                for san in result['san'][:10]:
                    print(f"    • {san}")
                
                return result
    except Exception as e:
        print(f"{Colors.ERROR}[-] SSL hatası: {e}{Colors.RESET}")
        return None

def web_technology_detection(url):
    """Web teknolojisi ve framework tespiti"""
    print(f"\n{Colors.INFO}[*] Web teknolojileri tespit ediliyor: {url}{Colors.RESET}")
    
    technologies = {
        'cms': [],
        'web_servers': [],
        'frameworks': [],
        'analytics': [],
        'javascript_libraries': [],
        'programming_languages': []
    }
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10, verify=False, allow_redirects=True)
        
        # Response headers analizi
        server = response.headers.get('Server', '')
        if server:
            technologies['web_servers'].append(server)
        
        powered_by = response.headers.get('X-Powered-By', '')
        if powered_by:
            technologies['programming_languages'].append(powered_by)
        
        # HTML içerik analizi
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Meta tag'ler
        meta_generator = soup.find('meta', attrs={'name': 'generator'})
        if meta_generator:
            technologies['cms'].append(meta_generator.get('content', ''))
        
        # WordPress tespiti
        if 'wp-content' in response.text or 'wp-includes' in response.text:
            technologies['cms'].append('WordPress')
        
        # Joomla tespiti
        if 'joomla' in response.text.lower() or '/components/com_' in response.text:
            technologies['cms'].append('Joomla')
        
        # Drupal tespiti
        if 'Drupal' in response.text or '/sites/default/' in response.text:
            technologies['cms'].append('Drupal')
        
        # JavaScript kütüphaneleri
        scripts = soup.find_all('script', src=True)
        for script in scripts:
            src = script.get('src', '').lower()
            if 'jquery' in src:
                technologies['javascript_libraries'].append('jQuery')
            elif 'angular' in src:
                technologies['javascript_libraries'].append('AngularJS')
            elif 'react' in src:
                technologies['javascript_libraries'].append('React')
            elif 'vue' in src:
                technologies['javascript_libraries'].append('Vue.js')
            elif 'bootstrap' in src:
                technologies['javascript_libraries'].append('Bootstrap')
        
        # Analytics tespiti
        if 'google-analytics.com' in response.text or 'gtag' in response.text:
            technologies['analytics'].append('Google Analytics')
        if 'googletagmanager.com' in response.text:
            technologies['analytics'].append('Google Tag Manager')
        if 'facebook.com/tr' in response.text:
            technologies['analytics'].append('Facebook Pixel')
        
        # PHP tespiti
        if '.php' in response.url or 'PHPSESSID' in response.cookies:
            technologies['programming_languages'].append('PHP')
        
        # ASP.NET tespiti
        if '.aspx' in response.url or 'ASP.NET' in response.headers.get('X-Powered-By', ''):
            technologies['programming_languages'].append('ASP.NET')
        
        # Tekrarları kaldır
        for key in technologies:
            technologies[key] = list(set(technologies[key]))
        
        print(f"{Colors.SUCCESS}[+] Tespit Edilen Teknolojiler:{Colors.RESET}")
        for tech_type, tech_list in technologies.items():
            if tech_list:
                print(f"  - {tech_type.replace('_', ' ').title()}: {', '.join(tech_list)}")
        
        return technologies
        
    except Exception as e:
        print(f"{Colors.ERROR}[-] Teknoloji tespit hatası: {e}{Colors.RESET}")
        return technologies

def http_security_headers(url):
    """HTTP güvenlik başlıkları analizi"""
    print(f"\n{Colors.INFO}[*] Güvenlik başlıkları analiz ediliyor: {url}{Colors.RESET}")
    
    security_headers = {
        'Strict-Transport-Security': 'HSTS - HTTPS zorlaması',
        'Content-Security-Policy': 'CSP - XSS koruması',
        'X-Frame-Options': 'Clickjacking koruması',
        'X-Content-Type-Options': 'MIME sniffing koruması',
        'X-XSS-Protection': 'XSS filtresi',
        'Referrer-Policy': 'Referrer bilgisi kontrolü',
        'Permissions-Policy': 'Tarayıcı özellik izinleri',
        'Cross-Origin-Embedder-Policy': 'COEP koruması',
        'Cross-Origin-Opener-Policy': 'COOP koruması',
        'Cross-Origin-Resource-Policy': 'CORP koruması'
    }
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        
        results = {
            'present': {},
            'missing': [],
            'score': 0,
            'total': len(security_headers)
        }
        
        print(f"\n{Colors.SUCCESS}[+] Güvenlik Başlıkları:{Colors.RESET}")
        for header, description in security_headers.items():
            if header in response.headers:
                results['present'][header] = {
                    'value': response.headers[header],
                    'description': description
                }
                results['score'] += 1
                print(f"  {Colors.SUCCESS}✓ {header}{Colors.RESET}")
                print(f"    {description}")
                print(f"    Değer: {response.headers[header][:80]}")
            else:
                results['missing'].append({
                    'header': header,
                    'description': description
                })
                print(f"  {Colors.ERROR}✗ {header}{Colors.RESET}")
                print(f"    {description} - EKSİK")
        
        percentage = (results['score'] / results['total']) * 100
        print(f"\n{Colors.INFO}[*] Güvenlik Skoru: {results['score']}/{results['total']} ({percentage:.1f}%){Colors.RESET}")
        
        return results
        
    except Exception as e:
        print(f"{Colors.ERROR}[-] HTTP analiz hatası: {e}{Colors.RESET}")
        return None

def subdomain_enumeration(domain, wordlist=None):
    """Subdomain keşfi"""
    print(f"\n{Colors.INFO}[*] Subdomain keşfi yapılıyor: {domain}{Colors.RESET}")
    
    # Varsayılan subdomain listesi
    default_subdomains = [
        'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'ns2',
        'webdisk', 'ns', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'm', 'mobile',
        'dev', 'test', 'staging', 'beta', 'admin', 'api', 'blog', 'shop', 'forum',
        'news', 'help', 'support', 'portal', 'secure', 'vpn', 'remote', 'cloud',
        'cdn', 'assets', 'static', 'media', 'files', 'download', 'upload', 'img',
        'images', 'video', 'chat', 'gitlab', 'git', 'svn', 'demo', 'app', 'apps'
    ]
    
    subdomains = wordlist if wordlist else default_subdomains
    found = []
    
    def check_subdomain(sub):
        subdomain = f"{sub}.{domain}"
        try:
            answers = dns.resolver.resolve(subdomain, 'A')
            ips = [str(rdata) for rdata in answers]
            found.append({
                'subdomain': subdomain,
                'ips': ips
            })
            print(f"{Colors.SUCCESS}[+] Bulundu: {subdomain} → {', '.join(ips)}{Colors.RESET}")
        except:
            pass
    
    threads = []
    for sub in subdomains:
        thread = threading.Thread(target=check_subdomain, args=(sub,))
        thread.start()
        threads.append(thread)
        time.sleep(0.01)
    
    for thread in threads:
        thread.join()
    
    print(f"\n{Colors.INFO}[*] Toplam {len(found)} subdomain bulundu{Colors.RESET}")
    return found

def reverse_ip_lookup(domain):
    """Aynı IP'deki diğer domainler"""
    print(f"\n{Colors.INFO}[*] Reverse IP lookup yapılıyor: {domain}{Colors.RESET}")
    
    try:
        # Domain'in IP'sini al
        ip = socket.gethostbyname(domain)
        print(f"{Colors.INFO}[*] IP Adresi: {ip}{Colors.RESET}")
        
        # HackerTarget API
        url = f"https://api.hackertarget.com/reverseiplookup/?q={ip}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200 and "error" not in response.text.lower():
            domains = [d.strip() for d in response.text.strip().split('\n')]
            print(f"{Colors.SUCCESS}[+] Aynı IP'de {len(domains)} domain bulundu:{Colors.RESET}")
            for d in domains[:20]:
                print(f"    • {d}")
            return {'ip': ip, 'domains': domains}
        else:
            print(f"{Colors.WARNING}[!] API'den sonuç alınamadı{Colors.RESET}")
            return {'ip': ip, 'domains': []}
            
    except Exception as e:
        print(f"{Colors.ERROR}[-] Reverse IP hatası: {e}{Colors.RESET}")
        return None

def wayback_machine_check(domain):
    """Wayback Machine arşiv kontrolü"""
    print(f"\n{Colors.INFO}[*] Wayback Machine arşivi kontrol ediliyor: {domain}{Colors.RESET}")
    
    try:
        url = f"http://archive.org/wayback/available?url={domain}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if 'archived_snapshots' in data and data['archived_snapshots']:
            closest = data['archived_snapshots'].get('closest', {})
            if closest:
                print(f"{Colors.SUCCESS}[+] Arşiv bulundu:{Colors.RESET}")
                print(f"    URL: {closest.get('url', 'N/A')}")
                print(f"    Tarih: {closest.get('timestamp', 'N/A')}")
                print(f"    Durum: {closest.get('status', 'N/A')}")
                return closest
        
        print(f"{Colors.WARNING}[!] Arşiv bulunamadı{Colors.RESET}")
        return None
        
    except Exception as e:
        print(f"{Colors.ERROR}[-] Wayback Machine hatası: {e}{Colors.RESET}")
        return None

def comprehensive_domain_scan(domain):
    """Kapsamlı domain taraması - tüm analizler"""
    print(f"\n{Colors.HEADER}{'='*70}")
    print(f"  KAPSAMLI DOMAIN ANALİZİ BAŞLIYOR: {domain}")
    print(f"{'='*70}{Colors.RESET}\n")
    
    results = {
        'domain': domain,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'scans': {}
    }
    
    # 1. WHOIS
    print(f"\n{Colors.MENU}[1/9] WHOIS Analizi{Colors.RESET}")
    results['scans']['whois'] = whois_lookup(domain)
    
    # 2. DNS
    print(f"\n{Colors.MENU}[2/9] DNS Analizi{Colors.RESET}")
    results['scans']['dns'] = dns_enumeration(domain)
    
    # 3. SSL/TLS
    print(f"\n{Colors.MENU}[3/9] SSL/TLS Analizi{Colors.RESET}")
    results['scans']['ssl'] = ssl_certificate_info(domain)
    
    # 4. HTTP/HTTPS
    url = f"https://{domain}"
    print(f"\n{Colors.MENU}[4/9] HTTP Güvenlik Başlıkları{Colors.RESET}")
    results['scans']['security_headers'] = http_security_headers(url)
    
    # 5. Web Teknolojileri
    print(f"\n{Colors.MENU}[5/9] Web Teknoloji Tespiti{Colors.RESET}")
    results['scans']['technologies'] = web_technology_detection(url)
    
    # 6. Subdomain Keşfi
    print(f"\n{Colors.MENU}[6/9] Subdomain Keşfi{Colors.RESET}")
    results['scans']['subdomains'] = subdomain_enumeration(domain)
    
    # 7. Reverse IP
    print(f"\n{Colors.MENU}[7/9] Reverse IP Lookup{Colors.RESET}")
    results['scans']['reverse_ip'] = reverse_ip_lookup(domain)
    
    # 8. Wayback Machine
    print(f"\n{Colors.MENU}[8/9] Wayback Machine Kontrolü{Colors.RESET}")
    results['scans']['wayback'] = wayback_machine_check(domain)
    
    # 9. Özet
    print(f"\n{Colors.MENU}[9/9] Özet Rapor Oluşturuluyor{Colors.RESET}")
    print(f"\n{Colors.HEADER}{'='*70}")
    print(f"  ANALİZ TAMAMLANDI!")
    print(f"{'='*70}{Colors.RESET}\n")
    
    return results

def domain_search_menu():
    """Domain araştırma menüsü"""
    while True:
        clear_screen()
        print_header()
        
        menu = f"""{Colors.MENU}
╔═══════════════════════════════════════════════════════════════╗
║                  DOMAIN ARAŞTIRMA MENÜSÜ                     ║
╚═══════════════════════════════════════════════════════════════╝

  {Colors.INPUT}[1]{Colors.RESET}  📋 WHOIS Sorgusu
  {Colors.INPUT}[2]{Colors.RESET}  🌐 DNS Kayıtları
  {Colors.INPUT}[3]{Colors.RESET}  🔒 SSL/TLS Sertifika Analizi
  {Colors.INPUT}[4]{Colors.RESET}  🛡️  HTTP Güvenlik Başlıkları
  {Colors.INPUT}[5]{Colors.RESET}  💻 Web Teknoloji Tespiti
  {Colors.INPUT}[6]{Colors.RESET}  🔍 Subdomain Keşfi
  {Colors.INPUT}[7]{Colors.RESET}  🔄 Reverse IP Lookup
  {Colors.INPUT}[8]{Colors.RESET}  📅 Wayback Machine Arşivi
  {Colors.INPUT}[9]{Colors.RESET}  🎯 KAPSAMLI TAM ANALİZ
  {Colors.INPUT}[0]{Colors.RESET}  🔙 Ana Menüye Dön

{Colors.INPUT}Seçiminiz: {Colors.RESET}"""
        
        print(menu, end='')
        choice = input().strip()
        
        if choice == '0':
            break
        elif choice == '1':
            domain = input(f"\n{Colors.INPUT}Domain adı: {Colors.RESET}").strip()
            if domain:
                result = whois_lookup(domain)
                if result:
                    save_result(f"whois_{domain}", result)
        elif choice == '2':
            domain = input(f"\n{Colors.INPUT}Domain adı: {Colors.RESET}").strip()
            if domain:
                result = dns_enumeration(domain)
                if result:
                    save_result(f"dns_{domain}", result)
        elif choice == '3':
            domain = input(f"\n{Colors.INPUT}Domain adı: {Colors.RESET}").strip()
            if domain:
                result = ssl_certificate_info(domain)
                if result:
                    save_result(f"ssl_{domain}", result)
        elif choice == '4':
            domain = input(f"\n{Colors.INPUT}Domain adı: {Colors.RESET}").strip()
            if domain:
                url = f"https://{domain}"
                result = http_security_headers(url)
                if result:
                    save_result(f"security_{domain}", result)
        elif choice == '5':
            domain = input(f"\n{Colors.INPUT}Domain adı: {Colors.RESET}").strip()
            if domain:
                url = f"https://{domain}"
                result = web_technology_detection(url)
                if result:
                    save_result(f"tech_{domain}", result)
        elif choice == '6':
            domain = input(f"\n{Colors.INPUT}Domain adı: {Colors.RESET}").strip()
            if domain:
                result = subdomain_enumeration(domain)
                if result:
                    save_result(f"subdomains_{domain}", result)
        elif choice == '7':
            domain = input(f"\n{Colors.INPUT}Domain adı: {Colors.RESET}").strip()
            if domain:
                result = reverse_ip_lookup(domain)
                if result:
                    save_result(f"reverseip_{domain}", result)
        elif choice == '8':
            domain = input(f"\n{Colors.INPUT}Domain adı: {Colors.RESET}").strip()
            if domain:
                result = wayback_machine_check(domain)
                if result:
                    save_result(f"wayback_{domain}", result)
        elif choice == '9':
            domain = input(f"\n{Colors.INPUT}Domain adı: {Colors.RESET}").strip()
            if domain:
                result = comprehensive_domain_scan(domain)
                if result:
                    filepath = save_result(f"comprehensive_{domain}", result)
                    print(f"\n{Colors.SUCCESS}[+] Kapsamlı analiz tamamlandı!{Colors.RESET}")
        else:
            print(f"{Colors.ERROR}[-] Geçersiz seçim!{Colors.RESET}")
        
        input(f"\n{Colors.INPUT}Devam etmek için Enter'a basın...{Colors.RESET}")

def main():
    try:
        domain_search_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}[!] İşlem iptal edildi{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.ERROR}[-] Beklenmeyen hata: {e}{Colors.RESET}")

if __name__ == "__main__":
    main()
