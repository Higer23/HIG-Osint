#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Port Scanner Module - Port Tarama Modülü
"""

import os
import sys
import socket
import json
from datetime import datetime
from pathlib import Path
from colorama import Fore, Style
import threading
from queue import Queue

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

# Yaygın portlar ve servisleri
COMMON_PORTS = {
    20: 'FTP Data',
    21: 'FTP Control',
    22: 'SSH',
    23: 'Telnet',
    25: 'SMTP',
    53: 'DNS',
    80: 'HTTP',
    110: 'POP3',
    111: 'RPC',
    135: 'MSRPC',
    139: 'NetBIOS',
    143: 'IMAP',
    443: 'HTTPS',
    445: 'SMB',
    465: 'SMTPS',
    587: 'SMTP Submission',
    993: 'IMAPS',
    995: 'POP3S',
    1433: 'MS SQL Server',
    1521: 'Oracle DB',
    3306: 'MySQL',
    3389: 'RDP',
    5432: 'PostgreSQL',
    5900: 'VNC',
    6379: 'Redis',
    8080: 'HTTP Proxy',
    8443: 'HTTPS Alt',
    9090: 'Web Admin',
    27017: 'MongoDB'
}

def clear_screen():
    """Ekranı temizle"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Modül başlığını göster"""
    header = f"""{Colors.HEADER}
╔═══════════════════════════════════════════════════════════════════╗
║                     PORT TARAMA MODÜLÜ                           ║
║                     Port Scanner Module                          ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(header)

def save_result(filename, data):
    """Sonuçları kaydet"""
    try:
        reports_dir = Path('reports')
        reports_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = reports_dir / f"port_scan_{filename}_{timestamp}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"{Colors.SUCCESS}[+] Sonuçlar kaydedildi: {filepath}{Colors.RESET}")
        return True
    except Exception as e:
        print(f"{Colors.ERROR}[-] Kayıt hatası: {e}{Colors.RESET}")
        return False

def scan_port(target, port, timeout=1):
    """Tek bir portu tara"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))
        sock.close()
        
        if result == 0:
            return True
        return False
    except socket.gaierror:
        return False
    except socket.error:
        return False

def get_service_name(port):
    """Port numarasından servis adını al"""
    return COMMON_PORTS.get(port, 'Unknown')

def scan_worker(target, port_queue, open_ports, timeout):
    """Thread worker fonksiyonu"""
    while not port_queue.empty():
        port = port_queue.get()
        
        if scan_port(target, port, timeout):
            service = get_service_name(port)
            open_ports.append({
                'port': port,
                'service': service,
                'state': 'open'
            })
            print(f"{Colors.SUCCESS}[+] Port {port} açık - {service}{Colors.RESET}")
        
        port_queue.task_done()

def quick_scan(target):
    """Hızlı tarama - Yaygın portlar"""
    print(f"\n{Colors.INFO}[*] Hızlı tarama başlatılıyor: {target}{Colors.RESET}")
    print(f"{Colors.INFO}[*] Yaygın {len(COMMON_PORTS)} port taranıyor...{Colors.RESET}\n")
    
    open_ports = []
    
    for port in COMMON_PORTS.keys():
        if scan_port(target, port, timeout=1):
            service = COMMON_PORTS[port]
            open_ports.append({
                'port': port,
                'service': service,
                'state': 'open'
            })
            print(f"{Colors.SUCCESS}[+] Port {port} açık - {service}{Colors.RESET}")
    
    result = {
        'target': target,
        'scan_type': 'quick',
        'total_ports_scanned': len(COMMON_PORTS),
        'open_ports': open_ports,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    print(f"\n{Colors.SUCCESS}[+] Tarama tamamlandı!{Colors.RESET}")
    print(f"{Colors.INFO}[*] Açık port sayısı: {len(open_ports)}{Colors.RESET}")
    
    return result

def range_scan(target, start_port, end_port, threads=50):
    """Port aralığı tarama"""
    print(f"\n{Colors.INFO}[*] Aralık taraması başlatılıyor: {target}{Colors.RESET}")
    print(f"{Colors.INFO}[*] Port aralığı: {start_port}-{end_port}{Colors.RESET}")
    print(f"{Colors.INFO}[*] Thread sayısı: {threads}{Colors.RESET}\n")
    
    port_queue = Queue()
    open_ports = []
    
    # Port kuyruğunu doldur
    for port in range(start_port, end_port + 1):
        port_queue.put(port)
    
    # Thread'leri başlat
    thread_list = []
    for _ in range(threads):
        thread = threading.Thread(target=scan_worker, args=(target, port_queue, open_ports, 1))
        thread.daemon = True
        thread.start()
        thread_list.append(thread)
    
    # Tüm thread'lerin bitmesini bekle
    port_queue.join()
    
    result = {
        'target': target,
        'scan_type': 'range',
        'port_range': f"{start_port}-{end_port}",
        'total_ports_scanned': end_port - start_port + 1,
        'open_ports': sorted(open_ports, key=lambda x: x['port']),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    print(f"\n{Colors.SUCCESS}[+] Tarama tamamlandı!{Colors.RESET}")
    print(f"{Colors.INFO}[*] Açık port sayısı: {len(open_ports)}{Colors.RESET}")
    
    return result

def full_scan(target, threads=100):
    """Tam tarama - Tüm portlar (1-65535)"""
    print(f"\n{Colors.WARNING}[!] UYARI: Tam port taraması uzun sürebilir!{Colors.RESET}")
    confirm = input(f"{Colors.INPUT}Devam etmek istiyor musunuz? (E/H): {Colors.RESET}").strip().upper()
    
    if confirm not in ['E', 'Y', 'EVET', 'YES']:
        print(f"{Colors.WARNING}[!] Tarama iptal edildi{Colors.RESET}")
        return None
    
    print(f"\n{Colors.INFO}[*] Tam tarama başlatılıyor: {target}{Colors.RESET}")
    print(f"{Colors.INFO}[*] Port aralığı: 1-65535{Colors.RESET}")
    print(f"{Colors.INFO}[*] Thread sayısı: {threads}{Colors.RESET}\n")
    
    port_queue = Queue()
    open_ports = []
    
    # Port kuyruğunu doldur
    for port in range(1, 65536):
        port_queue.put(port)
    
    # Thread'leri başlat
    thread_list = []
    for _ in range(threads):
        thread = threading.Thread(target=scan_worker, args=(target, port_queue, open_ports, 0.5))
        thread.daemon = True
        thread.start()
        thread_list.append(thread)
    
    # Tüm thread'lerin bitmesini bekle
    port_queue.join()
    
    result = {
        'target': target,
        'scan_type': 'full',
        'port_range': '1-65535',
        'total_ports_scanned': 65535,
        'open_ports': sorted(open_ports, key=lambda x: x['port']),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    print(f"\n{Colors.SUCCESS}[+] Tarama tamamlandı!{Colors.RESET}")
    print(f"{Colors.INFO}[*] Açık port sayısı: {len(open_ports)}{Colors.RESET}")
    
    return result

def custom_ports_scan(target, ports):
    """Özel port listesi tarama"""
    print(f"\n{Colors.INFO}[*] Özel port taraması başlatılıyor: {target}{Colors.RESET}")
    print(f"{Colors.INFO}[*] {len(ports)} port taranacak...{Colors.RESET}\n")
    
    open_ports = []
    
    for port in ports:
        if scan_port(target, port, timeout=1):
            service = get_service_name(port)
            open_ports.append({
                'port': port,
                'service': service,
                'state': 'open'
            })
            print(f"{Colors.SUCCESS}[+] Port {port} açık - {service}{Colors.RESET}")
    
    result = {
        'target': target,
        'scan_type': 'custom',
        'total_ports_scanned': len(ports),
        'open_ports': open_ports,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    print(f"\n{Colors.SUCCESS}[+] Tarama tamamlandı!{Colors.RESET}")
    print(f"{Colors.INFO}[*] Açık port sayısı: {len(open_ports)}{Colors.RESET}")
    
    return result

def service_detection(target, port):
    """Servis versiyonu tespiti (banner grabbing)"""
    print(f"\n{Colors.INFO}[*] Servis tespiti yapılıyor: {target}:{port}{Colors.RESET}")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((target, port))
        
        # Banner al
        try:
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            if banner:
                print(f"{Colors.SUCCESS}[+] Banner: {banner}{Colors.RESET}")
                return {'port': port, 'banner': banner}
        except:
            pass
        
        # HTTP request dene
        if port in [80, 443, 8080, 8443]:
            sock.send(b"GET / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n")
            response = sock.recv(1024).decode('utf-8', errors='ignore')
            print(f"{Colors.SUCCESS}[+] HTTP Response: {response[:200]}...{Colors.RESET}")
            return {'port': port, 'response': response[:500]}
        
        sock.close()
        return None
        
    except Exception as e:
        print(f"{Colors.ERROR}[-] Servis tespit hatası: {e}{Colors.RESET}")
        return None

def vulnerability_check(open_ports):
    """Temel güvenlik açığı kontrolü"""
    print(f"\n{Colors.INFO}[*] Güvenlik açığı kontrolü yapılıyor...{Colors.RESET}")
    
    vulnerabilities = []
    
    for port_info in open_ports:
        port = port_info['port']
        
        # Tehlikeli portlar
        if port == 23:  # Telnet
            vulnerabilities.append({
                'port': port,
                'severity': 'HIGH',
                'issue': 'Telnet servisi aktif - Şifrelenmemiş bağlantı'
            })
        elif port == 21:  # FTP
            vulnerabilities.append({
                'port': port,
                'severity': 'MEDIUM',
                'issue': 'FTP servisi aktif - Şifrelenmemiş veri transferi'
            })
        elif port == 445:  # SMB
            vulnerabilities.append({
                'port': port,
                'severity': 'MEDIUM',
                'issue': 'SMB servisi açık - EternalBlue ve benzeri saldırılara açık olabilir'
            })
        elif port == 3389:  # RDP
            vulnerabilities.append({
                'port': port,
                'severity': 'MEDIUM',
                'issue': 'RDP servisi açık - Brute force saldırılarına karşı savunmasız olabilir'
            })
    
    if vulnerabilities:
        print(f"\n{Colors.WARNING}[!] Tespit Edilen Potansiyel Güvenlik Sorunları:{Colors.RESET}")
        for vuln in vulnerabilities:
            severity_color = Colors.ERROR if vuln['severity'] == 'HIGH' else Colors.WARNING
            print(f"  {severity_color}[{vuln['severity']}] Port {vuln['port']}: {vuln['issue']}{Colors.RESET}")
    else:
        print(f"{Colors.SUCCESS}[+] Bilinen kritik güvenlik sorunu tespit edilmedi{Colors.RESET}")
    
    return vulnerabilities

def port_scanner_menu():
    """Port tarayıcı menüsü"""
    while True:
        clear_screen()
        print_header()
        
        menu = f"""{Colors.MENU}
╔═══════════════════════════════════════════════════════════════╗
║                   PORT TARAMA MENÜSÜ                         ║
╚═══════════════════════════════════════════════════════════════╝

  {Colors.INPUT}[1]{Colors.RESET} ⚡ Hızlı Tarama (Yaygın Portlar)
  {Colors.INPUT}[2]{Colors.RESET} 📊 Aralık Taraması
  {Colors.INPUT}[3]{Colors.RESET} 🔍 Tam Tarama (1-65535)
  {Colors.INPUT}[4]{Colors.RESET} 🎯 Özel Port Listesi
  {Colors.INPUT}[5]{Colors.RESET} 🔎 Servis Tespiti (Banner)
  {Colors.INPUT}[6]{Colors.RESET} 🛡️  Güvenlik Kontrolü
  {Colors.INPUT}[0]{Colors.RESET} 🔙 Ana Menüye Dön

{Colors.WARNING}[!] UYARI: Port tarama sadece kendi sistemlerinizde veya izniniz 
    olan sistemlerde yapılmalıdır. İzinsiz tarama yasadışıdır!{Colors.RESET}

{Colors.INPUT}Seçiminiz: {Colors.RESET}"""
        
        print(menu, end='')
        choice = input().strip()
        
        if choice == '0':
            break
        elif choice == '1':
            target = input(f"\n{Colors.INPUT}Hedef IP/Domain: {Colors.RESET}").strip()
            if target:
                result = quick_scan(target)
                if result:
                    save_result(f"quick_{target}", result)
        elif choice == '2':
            target = input(f"\n{Colors.INPUT}Hedef IP/Domain: {Colors.RESET}").strip()
            start_port = input(f"{Colors.INPUT}Başlangıç portu (örn: 1): {Colors.RESET}").strip()
            end_port = input(f"{Colors.INPUT}Bitiş portu (örn: 1000): {Colors.RESET}").strip()
            
            if target and start_port.isdigit() and end_port.isdigit():
                result = range_scan(target, int(start_port), int(end_port))
                if result:
                    save_result(f"range_{target}_{start_port}-{end_port}", result)
        elif choice == '3':
            target = input(f"\n{Colors.INPUT}Hedef IP/Domain: {Colors.RESET}").strip()
            if target:
                result = full_scan(target)
                if result:
                    save_result(f"full_{target}", result)
        elif choice == '4':
            target = input(f"\n{Colors.INPUT}Hedef IP/Domain: {Colors.RESET}").strip()
            ports_str = input(f"{Colors.INPUT}Port listesi (virgülle ayırın, örn: 80,443,8080): {Colors.RESET}").strip()
            
            if target and ports_str:
                try:
                    ports = [int(p.strip()) for p in ports_str.split(',')]
                    result = custom_ports_scan(target, ports)
                    if result:
                        save_result(f"custom_{target}", result)
                except ValueError:
                    print(f"{Colors.ERROR}[-] Geçersiz port listesi!{Colors.RESET}")
        elif choice == '5':
            target = input(f"\n{Colors.INPUT}Hedef IP/Domain: {Colors.RESET}").strip()
            port = input(f"{Colors.INPUT}Port numarası: {Colors.RESET}").strip()
            
            if target and port.isdigit():
                service_detection(target, int(port))
        elif choice == '6':
            target = input(f"\n{Colors.INPUT}Hedef IP/Domain: {Colors.RESET}").strip()
            if target:
                result = quick_scan(target)
                if result and result['open_ports']:
                    vulnerabilities = vulnerability_check(result['open_ports'])
                    result['vulnerabilities'] = vulnerabilities
                    save_result(f"security_{target}", result)
        else:
            print(f"{Colors.ERROR}[-] Geçersiz seçim!{Colors.RESET}")
        
        input(f"\n{Colors.INPUT}Devam etmek için Enter'a basın...{Colors.RESET}")

def main():
    """Ana fonksiyon"""
    try:
        port_scanner_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}[!] İşlem iptal edildi{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.ERROR}[-] Beklenmeyen hata: {e}{Colors.RESET}")

if __name__ == "__main__":
    main()
