cat > /home/claude/hig_modules/hash_decoder.py << 'EOFHASH'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import hashlib
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
║            🔐 HASH ÇÖZÜMLEME MODÜLÜ 🔐                      ║
╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}""")

def identify_hash(hash_string):
    length = len(hash_string)
    hash_types = {
        32: ["MD5", "NTLM"],
        40: ["SHA-1"],
        56: ["SHA-224"],
        64: ["SHA-256"],
        96: ["SHA-384"],
        128: ["SHA-512"],
    }
    
    print(f"\n{Colors.INFO}[*] Hash türü tahmin ediliyor...{Colors.RESET}\n")
    print(f"{Colors.SUCCESS}Hash Uzunluğu: {length} karakter{Colors.RESET}")
    
    if length in hash_types:
        print(f"{Colors.SUCCESS}Olası Hash Türleri: {', '.join(hash_types[length])}{Colors.RESET}")
        return hash_types[length]
    else:
        print(f"{Colors.ERROR}Bilinmeyen hash türü!{Colors.RESET}")
        return None

def generate_hash(text):
    print(f"\n{Colors.INFO}[*] Hash değerleri oluşturuluyor...{Colors.RESET}\n")
    
    algorithms = {
        'MD5': hashlib.md5(text.encode()).hexdigest(),
        'SHA-1': hashlib.sha1(text.encode()).hexdigest(),
        'SHA-256': hashlib.sha256(text.encode()).hexdigest(),
        'SHA-512': hashlib.sha512(text.encode()).hexdigest(),
    }
    
    for algo, hash_val in algorithms.items():
        print(f"{Colors.SUCCESS}{algo:10} : {hash_val}{Colors.RESET}")
    
    return algorithms

def main():
    os.system('clear' if os.name != 'nt' else 'cls')
    print_header()
    
    print(f"{Colors.INFO}Modlar:{Colors.RESET}")
    print(f"{Colors.INPUT}[1]{Colors.INFO} Hash Türü Tanımlama")
    print(f"{Colors.INPUT}[2]{Colors.INFO} Metin'den Hash Oluşturma{Colors.RESET}\n")
    
    choice = input(f"{Colors.INPUT}Seçim (1/2): {Colors.RESET}").strip()
    
    if choice == '1':
        hash_str = input(f"{Colors.INPUT}Hash değeri: {Colors.RESET}").strip()
        if hash_str:
            hash_types = identify_hash(hash_str)
            if hash_types:
                print(f"\n{Colors.INFO}Online Hash Cracking Linkleri:{Colors.RESET}")
                print(f"{Colors.SUCCESS}→ CrackStation: https://crackstation.net/{Colors.RESET}")
                print(f"{Colors.SUCCESS}→ MD5Decrypt: https://md5decrypt.net/{Colors.RESET}")
                print(f"{Colors.SUCCESS}→ HashKiller: https://hashkiller.io/{Colors.RESET}")
    
    elif choice == '2':
        text = input(f"{Colors.INPUT}Metin: {Colors.RESET}").strip()
        if text:
            generate_hash(text)
    
    else:
        print(f"{Colors.ERROR}[!] Geçersiz seçim!{Colors.RESET}")
    
    input(f"\n{Colors.INPUT}Enter...{Colors.RESET}")

if __name__ == "__main__":
    main()
EOFHASH

cat > /home/claude/hig_modules/port_scanner.py << 'EOFPORT'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import socket
from pathlib import Path
from colorama import Fore, Style

BASE_DIR = Path(__file__).resolve().parent.parent

class Colors:
    HEADER = Fore.CYAN + Style.BRIGHT
    SUCCESS = Fore.GREEN + Style.BRIGHT
    ERROR = Fore.RED + Style.BRIGHT
    WARNING = Fore.YELLOW + Style.BRIGHT
    INFO = Fore.BLUE + Style.BRIGHT
    INPUT = Fore.WHITE + Style.BRIGHT
    RESET = Style.RESET_ALL

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB",
    3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 5900: "VNC",
    8080: "HTTP-Alt", 8443: "HTTPS-Alt", 27017: "MongoDB"
}

def print_header():
    print(f"""{Colors.HEADER}
╔══════════════════════════════════════════════════════════════╗
║            📡 PORT TARAMA MODÜLÜ 📡                          ║
╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}""")

def scan_port(host, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def main():
    os.system('clear' if os.name != 'nt' else 'cls')
    print_header()
    
    host = input(f"{Colors.INPUT}Hedef IP veya domain: {Colors.RESET}").strip()
    if not host:
        print(f"{Colors.ERROR}[!] Hedef boş olamaz!{Colors.RESET}")
        return
    
    print(f"\n{Colors.INFO}[*] Yaygın portlar taranıyor...{Colors.RESET}\n")
    
    open_ports = []
    
    for port, service in COMMON_PORTS.items():
        if scan_port(host, port):
            open_ports.append((port, service))
            print(f"{Colors.SUCCESS}✓ Port {port:5} ({service:15}) - AÇIK{Colors.RESET}")
        else:
            print(f"{Colors.WARNING}  Port {port:5} ({service:15}) - Kapalı{Colors.RESET}", end='\r')
    
    print(f"\n\n{Colors.HEADER}╔════════════════════ SONUÇ ══════════════════════╗{Colors.RESET}")
    print(f"{Colors.SUCCESS}Açık Port Sayısı: {len(open_ports)}{Colors.RESET}")
    print(f"{Colors.HEADER}╚═════════════════════════════════════════════════╝{Colors.RESET}\n")
    
    if open_ports:
        print(f"{Colors.INFO}Açık Portlar:{Colors.RESET}")
        for port, service in open_ports:
            print(f"{Colors.SUCCESS}  → {port} ({service}){Colors.RESET}")
    
    input(f"\n{Colors.INPUT}Enter...{Colors.RESET}")

if __name__ == "__main__":
    main()
EOFPORT

echo "Hash Decoder ve Port Scanner modülleri oluşturuldu"
