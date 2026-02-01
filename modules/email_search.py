#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Email Search Module - Kapsamlı E-posta Araştırma ve Doğrulama Modülü
E-posta OSINT, veri ihlali kontrolü, spam veritabanı, format doğrulama
"""

import os
import sys
import json
import re
import socket
import dns.resolver
import requests
import hashlib
from datetime import datetime
from pathlib import Path
from colorama import Fore, Style
import smtplib
from email.mime.text import MIMEText
import threading
from queue import Queue
import time

try:
    import phonenumbers
except ImportError:
    print("[!] phonenumbers modülü yükleniyor...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "phonenumbers", "--break-system-packages"])
    import phonenumbers

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
║                   E-POSTA ARAŞTIRMA MODÜLÜ                       ║
║          Advanced Email Research & Validation Module             ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(header)

def save_result(filename, data):
    try:
        reports_dir = Path('reports')
        reports_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = reports_dir / f"email_{filename}_{timestamp}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"{Colors.SUCCESS}[+] Sonuçlar kaydedildi: {filepath}{Colors.RESET}")
        return filepath
    except Exception as e:
        print(f"{Colors.ERROR}[-] Kayıt hatası: {e}{Colors.RESET}")
        return None

def validate_email_format(email):
    """E-posta format doğrulaması (RFC 5322)"""
    print(f"\n{Colors.INFO}[*] E-posta formatı kontrol ediliyor: {email}{Colors.RESET}")
    
    # RFC 5322 regex pattern
    pattern = r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
    
    is_valid = bool(re.match(pattern, email))
    
    result = {
        'email': email,
        'format_valid': is_valid,
        'local_part': email.split('@')[0] if '@' in email else None,
        'domain': email.split('@')[1] if '@' in email else None,
        'checks': {
            'has_at_symbol': '@' in email,
            'single_at_symbol': email.count('@') == 1,
            'not_empty_local': len(email.split('@')[0]) > 0 if '@' in email else False,
            'not_empty_domain': len(email.split('@')[1]) > 0 if '@' in email and len(email.split('@')) > 1 else False,
            'valid_characters': bool(re.match(pattern, email)),
            'no_spaces': ' ' not in email,
            'has_domain_extension': '.' in email.split('@')[1] if '@' in email and len(email.split('@')) > 1 else False
        }
    }
    
    if is_valid:
        print(f"{Colors.SUCCESS}[+] Format geçerli ✓{Colors.RESET}")
    else:
        print(f"{Colors.ERROR}[-] Format geçersiz ✗{Colors.RESET}")
        print(f"{Colors.WARNING}[!] Başarısız kontroller:{Colors.RESET}")
        for check, status in result['checks'].items():
            if not status:
                print(f"    • {check}")
    
    return result

def check_mx_records(domain):
    """MX kayıtlarını kontrol et"""
    print(f"\n{Colors.INFO}[*] MX kayıtları kontrol ediliyor: {domain}{Colors.RESET}")
    
    try:
        mx_records = []
        answers = dns.resolver.resolve(domain, 'MX')
        
        for rdata in answers:
            mx_records.append({
                'priority': rdata.preference,
                'exchange': str(rdata.exchange),
                'host': str(rdata.exchange).rstrip('.')
            })
        
        mx_records.sort(key=lambda x: x['priority'])
        
        print(f"{Colors.SUCCESS}[+] {len(mx_records)} MX kaydı bulundu:{Colors.RESET}")
        for mx in mx_records:
            print(f"    Priority {mx['priority']}: {mx['exchange']}")
        
        return {
            'has_mx': True,
            'mx_records': mx_records,
            'primary_mx': mx_records[0] if mx_records else None
        }
        
    except dns.resolver.NoAnswer:
        print(f"{Colors.WARNING}[!] MX kaydı bulunamadı{Colors.RESET}")
        return {'has_mx': False, 'mx_records': [], 'primary_mx': None}
    except dns.resolver.NXDOMAIN:
        print(f"{Colors.ERROR}[-] Domain mevcut değil{Colors.RESET}")
        return {'has_mx': False, 'mx_records': [], 'error': 'Domain not found'}
    except Exception as e:
        print(f"{Colors.ERROR}[-] MX kontrol hatası: {e}{Colors.RESET}")
        return {'has_mx': False, 'error': str(e)}

def smtp_verification(email):
    """SMTP seviyesinde e-posta doğrulama"""
    print(f"\n{Colors.INFO}[*] SMTP doğrulaması yapılıyor: {email}{Colors.RESET}")
    
    if '@' not in email:
        return {'valid': False, 'error': 'Invalid email format'}
    
    local, domain = email.split('@')
    
    # MX kayıtlarını al
    mx_check = check_mx_records(domain)
    if not mx_check['has_mx']:
        return {'valid': False, 'error': 'No MX records', 'mx_check': mx_check}
    
    mx_host = mx_check['primary_mx']['host']
    
    try:
        # SMTP sunucusuna bağlan
        server = smtplib.SMTP(timeout=10)
        server.set_debuglevel(0)
        server.connect(mx_host)
        server.helo('verify.example.com')
        server.mail('verify@example.com')
        code, message = server.rcpt(email)
        server.quit()
        
        # 250 = başarılı, 550 = mailbox bulunamadı
        if code == 250:
            print(f"{Colors.SUCCESS}[+] E-posta adresi doğrulandı ✓{Colors.RESET}")
            return {
                'valid': True,
                'smtp_code': code,
                'smtp_message': message.decode() if isinstance(message, bytes) else str(message),
                'mx_host': mx_host
            }
        else:
            print(f"{Colors.WARNING}[!] E-posta adresi doğrulanamadı (Code: {code}){Colors.RESET}")
            return {
                'valid': False,
                'smtp_code': code,
                'smtp_message': message.decode() if isinstance(message, bytes) else str(message),
                'mx_host': mx_host
            }
            
    except smtplib.SMTPServerDisconnected:
        print(f"{Colors.WARNING}[!] SMTP sunucusu bağlantıyı kesti{Colors.RESET}")
        return {'valid': None, 'error': 'SMTP disconnected', 'mx_host': mx_host}
    except smtplib.SMTPConnectError as e:
        print(f"{Colors.ERROR}[-] SMTP bağlantı hatası: {e}{Colors.RESET}")
        return {'valid': None, 'error': str(e)}
    except Exception as e:
        print(f"{Colors.ERROR}[-] SMTP doğrulama hatası: {e}{Colors.RESET}")
        return {'valid': None, 'error': str(e)}

def check_disposable_email(domain):
    """Geçici/çöp e-posta kontrolü"""
    print(f"\n{Colors.INFO}[*] Geçici e-posta kontrolü: {domain}{Colors.RESET}")
    
    # Bilinen disposable email servisleri
    disposable_domains = [
        '10minutemail.com', 'guerrillamail.com', 'mailinator.com', 'temp-mail.org',
        'throwaway.email', 'yopmail.com', 'tempmail.com', 'fakeinbox.com',
        'maildrop.cc', 'getnada.com', 'trashmail.com', 'mintemail.com',
        'tempr.email', 'mohmal.com', 'sharklasers.com', 'guerrillamail.de'
    ]
    
    is_disposable = domain.lower() in disposable_domains
    
    # DisposableEmailChecker API
    try:
        url = f"https://open.kickbox.com/v1/disposable/{domain}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            is_disposable = data.get('disposable', is_disposable)
    except:
        pass
    
    if is_disposable:
        print(f"{Colors.WARNING}[!] Geçici/çöp e-posta servisi tespit edildi{Colors.RESET}")
    else:
        print(f"{Colors.SUCCESS}[+] Geçici e-posta değil{Colors.RESET}")
    
    return {'is_disposable': is_disposable, 'domain': domain}

def haveibeenpwned_check(email):
    """Have I Been Pwned veri ihlali kontrolü"""
    print(f"\n{Colors.INFO}[*] Have I Been Pwned kontrolü yapılıyor: {email}{Colors.RESET}")
    print(f"{Colors.WARNING}[!] Bu işlem API anahtarı gerektirir{Colors.RESET}")
    
    # SHA-1 hash (HIBP k-anonymity için)
    sha1_hash = hashlib.sha1(email.encode()).hexdigest().upper()
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]
    
    try:
        # Önce breach'leri kontrol et (email direkt)
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
        headers = {
            'User-Agent': 'HIG-OSINT-Tool',
            'hibp-api-key': ''  # API key gerekli
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            breaches = response.json()
            print(f"{Colors.ERROR}[!] VERİ İHLALİ TESPİT EDİLDİ!{Colors.RESET}")
            print(f"{Colors.ERROR}[!] Bu e-posta {len(breaches)} veri ihlalinde bulundu:{Colors.RESET}")
            
            breach_info = []
            for breach in breaches[:10]:
                info = {
                    'name': breach.get('Name'),
                    'domain': breach.get('Domain'),
                    'breach_date': breach.get('BreachDate'),
                    'added_date': breach.get('AddedDate'),
                    'pwn_count': breach.get('PwnCount'),
                    'data_classes': breach.get('DataClasses', [])
                }
                breach_info.append(info)
                print(f"\n  • {info['name']} ({info['domain']})")
                print(f"    İhlal Tarihi: {info['breach_date']}")
                print(f"    Etkilenen: {info['pwn_count']:,} hesap")
                print(f"    Sızan Veriler: {', '.join(info['data_classes'][:5])}")
            
            return {
                'pwned': True,
                'breach_count': len(breaches),
                'breaches': breach_info
            }
        elif response.status_code == 404:
            print(f"{Colors.SUCCESS}[+] Veri ihlali tespit edilmedi ✓{Colors.RESET}")
            return {'pwned': False, 'breach_count': 0}
        elif response.status_code == 401:
            print(f"{Colors.WARNING}[!] API anahtarı gerekli veya geçersiz{Colors.RESET}")
            return {'error': 'API key required'}
        else:
            print(f"{Colors.WARNING}[!] API hatası: {response.status_code}{Colors.RESET}")
            return {'error': f'API error: {response.status_code}'}
            
    except Exception as e:
        print(f"{Colors.ERROR}[-] HIBP kontrol hatası: {e}{Colors.RESET}")
        return {'error': str(e)}

def dehashed_lookup(email):
    """DeHashed veri ihlali arama"""
    print(f"\n{Colors.INFO}[*] DeHashed veritabanı sorgulanıyor: {email}{Colors.RESET}")
    print(f"{Colors.WARNING}[!] Bu işlem DeHashed API anahtarı gerektirir{Colors.RESET}")
    
    # DeHashed API (ücretli servis)
    api_url = "https://api.dehashed.com/search"
    headers = {
        'Accept': 'application/json'
    }
    params = {
        'query': f'email:{email}',
        'size': 10000
    }
    
    # Not: Gerçek kullanım için API key ve auth gerekli
    print(f"{Colors.INFO}[*] DeHashed URL: {api_url}?query=email:{email}{Colors.RESET}")
    print(f"{Colors.WARNING}[!] Tam sonuçlar için DeHashed hesabı gereklidir{Colors.RESET}")
    
    return {
        'service': 'DeHashed',
        'search_url': f"{api_url}?query=email:{email}",
        'note': 'API key required for actual search'
    }

def email_reputation_check(email):
    """E-posta itibar kontrolü"""
    print(f"\n{Colors.INFO}[*] E-posta itibarı kontrol ediliyor: {email}{Colors.RESET}")
    
    domain = email.split('@')[1] if '@' in email else None
    if not domain:
        return {'error': 'Invalid email'}
    
    reputation = {
        'email': email,
        'domain': domain,
        'checks': {}
    }
    
    # Spam veritabanı kontrolü
    spam_databases = [
        f"https://www.stopforumspam.com/api?email={email}",
        f"https://check.spamhaus.org/query/email/{email}"
    ]
    
    try:
        # StopForumSpam API
        response = requests.get(spam_databases[0], timeout=5)
        if response.status_code == 200:
            data = response.json()
            if 'email' in data and 'appears' in data['email']:
                appears = data['email']['appears']
                reputation['checks']['stopforumspam'] = {
                    'listed': appears > 0,
                    'frequency': appears
                }
                if appears > 0:
                    print(f"{Colors.WARNING}[!] StopForumSpam'de {appears} kez listelendi{Colors.RESET}")
                else:
                    print(f"{Colors.SUCCESS}[+] StopForumSpam'de temiz{Colors.RESET}")
    except:
        reputation['checks']['stopforumspam'] = {'error': 'Could not check'}
    
    # Domain blacklist kontrolü
    blacklist_check = check_domain_blacklist(domain)
    reputation['checks']['blacklist'] = blacklist_check
    
    return reputation

def check_domain_blacklist(domain):
    """Domain blacklist kontrolü"""
    print(f"\n{Colors.INFO}[*] Domain blacklist kontrolü: {domain}{Colors.RESET}")
    
    blacklists = [
        'zen.spamhaus.org',
        'bl.spamcop.net',
        'dnsbl.sorbs.net',
        'cbl.abuseat.org'
    ]
    
    listed_on = []
    
    try:
        # Domain'in IP'sini al
        ip = socket.gethostbyname(domain)
        reversed_ip = '.'.join(reversed(ip.split('.')))
        
        for bl in blacklists:
            try:
                query = f"{reversed_ip}.{bl}"
                socket.gethostbyname(query)
                listed_on.append(bl)
                print(f"{Colors.WARNING}[!] {bl}'de listelendi{Colors.RESET}")
            except socket.gaierror:
                # Listede değil
                pass
        
        if not listed_on:
            print(f"{Colors.SUCCESS}[+] Hiçbir blacklist'te listelenmemiş{Colors.RESET}")
        
        return {
            'domain': domain,
            'ip': ip,
            'listed': len(listed_on) > 0,
            'blacklists': listed_on
        }
        
    except Exception as e:
        print(f"{Colors.ERROR}[-] Blacklist kontrol hatası: {e}{Colors.RESET}")
        return {'error': str(e)}

def social_media_search(email):
    """Sosyal medya hesapları arama"""
    print(f"\n{Colors.INFO}[*] Sosyal medya hesapları aranıyor: {email}{Colors.RESET}")
    
    platforms = {
        'Gravatar': f"https://gravatar.com/{hashlib.md5(email.lower().encode()).hexdigest()}",
        'GitHub': f"https://api.github.com/search/users?q={email}",
        'About.me': f"https://about.me/{email.split('@')[0]}",
        'Skype': f"https://www.skype.com/search/profile?q={email}",
    }
    
    print(f"\n{Colors.SUCCESS}[+] Kontrol Edilecek Platformlar:{Colors.RESET}")
    for platform, url in platforms.items():
        print(f"  • {platform}: {url}")
    
    # Gravatar kontrolü
    try:
        gravatar_url = platforms['Gravatar']
        response = requests.get(gravatar_url, timeout=5)
        if response.status_code == 200:
            print(f"\n{Colors.SUCCESS}[+] Gravatar profili bulundu!{Colors.RESET}")
    except:
        pass
    
    return {
        'email': email,
        'platforms': platforms,
        'note': 'Manual verification required for most platforms'
    }

def email_intelligence_gathering(email):
    """E-posta istihbarat toplama"""
    print(f"\n{Colors.INFO}[*] E-posta istihbaratı toplanıyor: {email}{Colors.RESET}")
    
    intelligence = {
        'email': email,
        'timestamp': datetime.now().isoformat(),
        'data': {}
    }
    
    # Email pattern analizi
    local, domain = email.split('@') if '@' in email else (None, None)
    if local and domain:
        intelligence['data']['patterns'] = {
            'local_length': len(local),
            'has_numbers': bool(re.search(r'\d', local)),
            'has_dots': '.' in local,
            'has_underscore': '_' in local,
            'has_hyphen': '-' in local,
            'pattern_type': 'firstname.lastname' if '.' in local else 
                          'firstnamelastname' if len(local) > 10 else
                          'username'
        }
    
    # Domain analizi
    intelligence['data']['domain_info'] = {
        'domain': domain,
        'tld': domain.split('.')[-1] if domain and '.' in domain else None,
        'is_common_provider': domain in [
            'gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com',
            'icloud.com', 'protonmail.com', 'aol.com'
        ] if domain else False
    }
    
    print(f"\n{Colors.SUCCESS}[+] İstihbarat Özeti:{Colors.RESET}")
    print(f"  • E-posta: {email}")
    print(f"  • Local Part: {local}")
    print(f"  • Domain: {domain}")
    if intelligence['data'].get('patterns'):
        print(f"  • Pattern Tipi: {intelligence['data']['patterns']['pattern_type']}")
    
    return intelligence

def comprehensive_email_analysis(email):
    """Kapsamlı e-posta analizi - tüm kontroller"""
    print(f"\n{Colors.HEADER}{'='*70}")
    print(f"  KAPSAMLI E-POSTA ANALİZİ BAŞLIYOR: {email}")
    print(f"{'='*70}{Colors.RESET}\n")
    
    results = {
        'email': email,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'analyses': {}
    }
    
    # 1. Format Doğrulama
    print(f"\n{Colors.MENU}[1/10] Format Doğrulama{Colors.RESET}")
    results['analyses']['format'] = validate_email_format(email)
    
    if not results['analyses']['format']['format_valid']:
        print(f"\n{Colors.ERROR}[!] Geçersiz e-posta formatı. Analiz sonlandırılıyor.{Colors.RESET}")
        return results
    
    domain = email.split('@')[1]
    
    # 2. MX Kayıtları
    print(f"\n{Colors.MENU}[2/10] MX Kayıt Kontrolü{Colors.RESET}")
    results['analyses']['mx_records'] = check_mx_records(domain)
    
    # 3. SMTP Doğrulama
    print(f"\n{Colors.MENU}[3/10] SMTP Doğrulama{Colors.RESET}")
    results['analyses']['smtp'] = smtp_verification(email)
    
    # 4. Geçici E-posta Kontrolü
    print(f"\n{Colors.MENU}[4/10] Geçici E-posta Kontrolü{Colors.RESET}")
    results['analyses']['disposable'] = check_disposable_email(domain)
    
    # 5. Veri İhlali Kontrolü
    print(f"\n{Colors.MENU}[5/10] Veri İhlali Kontrolü (HIBP){Colors.RESET}")
    results['analyses']['hibp'] = haveibeenpwned_check(email)
    
    # 6. DeHashed Lookup
    print(f"\n{Colors.MENU}[6/10] DeHashed Arama{Colors.RESET}")
    results['analyses']['dehashed'] = dehashed_lookup(email)
    
    # 7. İtibar Kontrolü
    print(f"\n{Colors.MENU}[7/10] E-posta İtibar Kontrolü{Colors.RESET}")
    results['analyses']['reputation'] = email_reputation_check(email)
    
    # 8. Blacklist Kontrolü
    print(f"\n{Colors.MENU}[8/10] Domain Blacklist Kontrolü{Colors.RESET}")
    results['analyses']['blacklist'] = check_domain_blacklist(domain)
    
    # 9. Sosyal Medya Arama
    print(f"\n{Colors.MENU}[9/10] Sosyal Medya Arama{Colors.RESET}")
    results['analyses']['social_media'] = social_media_search(email)
    
    # 10. İstihbarat Toplama
    print(f"\n{Colors.MENU}[10/10] İstihbarat Toplama{Colors.RESET}")
    results['analyses']['intelligence'] = email_intelligence_gathering(email)
    
    # Özet
    print(f"\n{Colors.HEADER}{'='*70}")
    print(f"  ANALİZ TAMAMLANDI!")
    print(f"{'='*70}{Colors.RESET}\n")
    
    print(f"{Colors.SUCCESS}[+] Özet:{Colors.RESET}")
    print(f"  • Format: {'✓ Geçerli' if results['analyses']['format']['format_valid'] else '✗ Geçersiz'}")
    print(f"  • MX Kayıtları: {'✓ Var' if results['analyses']['mx_records']['has_mx'] else '✗ Yok'}")
    print(f"  • Geçici E-posta: {'✗ Evet' if results['analyses']['disposable']['is_disposable'] else '✓ Hayır'}")
    
    if results['analyses']['hibp'].get('pwned'):
        print(f"  • Veri İhlali: {Colors.ERROR}✗ {results['analyses']['hibp']['breach_count']} ihlalde bulundu{Colors.RESET}")
    elif results['analyses']['hibp'].get('error'):
        print(f"  • Veri İhlali: ? Kontrol edilemedi")
    else:
        print(f"  • Veri İhlali: ✓ Bulunamadı")
    
    return results

def email_search_menu():
    """E-posta araştırma menüsü"""
    while True:
        clear_screen()
        print_header()
        
        menu = f"""{Colors.MENU}
╔═══════════════════════════════════════════════════════════════╗
║                 E-POSTA ARAŞTIRMA MENÜSÜ                     ║
╚═══════════════════════════════════════════════════════════════╝

  {Colors.INPUT}[1]{Colors.RESET}  ✓  Format Doğrulama
  {Colors.INPUT}[2]{Colors.RESET}  📧 MX Kayıt Kontrolü
  {Colors.INPUT}[3]{Colors.RESET}  🔍 SMTP Doğrulama
  {Colors.INPUT}[4]{Colors.RESET}  🗑️  Geçici E-posta Kontrolü
  {Colors.INPUT}[5]{Colors.RESET}  🔓 Have I Been Pwned
  {Colors.INPUT}[6]{Colors.RESET}  💀 DeHashed Arama
  {Colors.INPUT}[7]{Colors.RESET}  ⭐ İtibar Kontrolü
  {Colors.INPUT}[8]{Colors.RESET}  🚫 Blacklist Kontrolü
  {Colors.INPUT}[9]{Colors.RESET}  📱 Sosyal Medya Arama
  {Colors.INPUT}[10]{Colors.RESET} 🎯 KAPSAMLI TAM ANALİZ
  {Colors.INPUT}[0]{Colors.RESET}  🔙 Ana Menüye Dön

{Colors.INPUT}Seçiminiz: {Colors.RESET}"""
        
        print(menu, end='')
        choice = input().strip()
        
        if choice == '0':
            break
        elif choice == '1':
            email = input(f"\n{Colors.INPUT}E-posta adresi: {Colors.RESET}").strip()
            if email:
                result = validate_email_format(email)
                save_result(f"format_{email.replace('@', '_')}", result)
        elif choice == '2':
            email = input(f"\n{Colors.INPUT}E-posta adresi: {Colors.RESET}").strip()
            if email and '@' in email:
                domain = email.split('@')[1]
                result = check_mx_records(domain)
                save_result(f"mx_{domain}", result)
        elif choice == '3':
            email = input(f"\n{Colors.INPUT}E-posta adresi: {Colors.RESET}").strip()
            if email:
                result = smtp_verification(email)
                save_result(f"smtp_{email.replace('@', '_')}", result)
        elif choice == '4':
            email = input(f"\n{Colors.INPUT}E-posta adresi: {Colors.RESET}").strip()
            if email and '@' in email:
                domain = email.split('@')[1]
                result = check_disposable_email(domain)
                save_result(f"disposable_{domain}", result)
        elif choice == '5':
            email = input(f"\n{Colors.INPUT}E-posta adresi: {Colors.RESET}").strip()
            if email:
                result = haveibeenpwned_check(email)
                save_result(f"hibp_{email.replace('@', '_')}", result)
        elif choice == '6':
            email = input(f"\n{Colors.INPUT}E-posta adresi: {Colors.RESET}").strip()
            if email:
                result = dehashed_lookup(email)
                save_result(f"dehashed_{email.replace('@', '_')}", result)
        elif choice == '7':
            email = input(f"\n{Colors.INPUT}E-posta adresi: {Colors.RESET}").strip()
            if email:
                result = email_reputation_check(email)
                save_result(f"reputation_{email.replace('@', '_')}", result)
        elif choice == '8':
            email = input(f"\n{Colors.INPUT}E-posta adresi: {Colors.RESET}").strip()
            if email and '@' in email:
                domain = email.split('@')[1]
                result = check_domain_blacklist(domain)
                save_result(f"blacklist_{domain}", result)
        elif choice == '9':
            email = input(f"\n{Colors.INPUT}E-posta adresi: {Colors.RESET}").strip()
            if email:
                result = social_media_search(email)
                save_result(f"social_{email.replace('@', '_')}", result)
        elif choice == '10':
            email = input(f"\n{Colors.INPUT}E-posta adresi: {Colors.RESET}").strip()
            if email:
                result = comprehensive_email_analysis(email)
                save_result(f"comprehensive_{email.replace('@', '_')}", result)
                print(f"\n{Colors.SUCCESS}[+] Kapsamlı analiz tamamlandı!{Colors.RESET}")
        else:
            print(f"{Colors.ERROR}[-] Geçersiz seçim!{Colors.RESET}")
        
        input(f"\n{Colors.INPUT}Devam etmek için Enter'a basın...{Colors.RESET}")

def main():
    try:
        email_search_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}[!] İşlem iptal edildi{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.ERROR}[-] Beklenmeyen hata: {e}{Colors.RESET}")

if __name__ == "__main__":
    main()
