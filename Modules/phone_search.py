#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HIG-Osint Phone Search Module
Telefon numarası araştırması ve lokasyon tespiti
"""

import os
import sys
from pathlib import Path
from colorama import Fore, Style
from datetime import datetime

try:
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone
except ImportError:
    print("[!] phonenumbers modülü bulunamadı. Yükleniyor...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "phonenumbers", "--break-system-packages"])
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone

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
║           📱 TELEFON NUMARASI ARAŞTIRMA MODÜLÜ 📱           ║
╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(header)

def analyze_phone(phone_number):
    """Telefon numarasını analiz et"""
    print(f"\n{Colors.INFO}[*] Telefon numarası analiz ediliyor...{Colors.RESET}\n")
    
    results = {
        'number': phone_number,
        'valid': False,
        'country': None,
        'location': None,
        'carrier': None,
        'timezone': None,
        'number_type': None,
        'international_format': None,
        'national_format': None,
        'country_code': None
    }
    
    try:
        # Numarayı parse et
        parsed_number = phonenumbers.parse(phone_number, None)
        
        # Geçerlilik kontrolü
        results['valid'] = phonenumbers.is_valid_number(parsed_number)
        
        if not results['valid']:
            print(f"{Colors.ERROR}✗ Geçersiz telefon numarası{Colors.RESET}")
            return results
        
        print(f"{Colors.SUCCESS}✓ Telefon numarası geçerli{Colors.RESET}\n")
        
        # Ülke bilgisi
        results['country'] = geocoder.description_for_number(parsed_number, "tr")
        results['country_code'] = f"+{parsed_number.country_code}"
        print(f"{Colors.INFO}Ülke          : {results['country']} ({results['country_code']}){Colors.RESET}")
        
        # Bölge/Lokasyon
        results['location'] = geocoder.description_for_number(parsed_number, "tr")
        print(f"{Colors.INFO}Lokasyon      : {results['location']}{Colors.RESET}")
        
        # Operatör bilgisi
        results['carrier'] = carrier.name_for_number(parsed_number, "tr")
        if results['carrier']:
            print(f"{Colors.INFO}Operatör      : {results['carrier']}{Colors.RESET}")
        
        # Zaman dilimi
        timezones = timezone.time_zones_for_number(parsed_number)
        if timezones:
            results['timezone'] = list(timezones)
            print(f"{Colors.INFO}Zaman Dilimi  : {', '.join(results['timezone'])}{Colors.RESET}")
        
        # Numara türü
        number_type = phonenumbers.number_type(parsed_number)
        type_names = {
            0: "Sabit Hat",
            1: "Mobil",
            2: "Sabit Hat veya Mobil",
            3: "Ücretsiz",
            4: "Ücretli",
            5: "Paylaşımlı Maliyet",
            6: "VoIP",
            7: "Kişisel Numara",
            8: "Çağrı Merkezi",
            9: "UAN",
            10: "Bilinmeyen"
        }
        results['number_type'] = type_names.get(number_type, "Bilinmeyen")
        print(f"{Colors.INFO}Numara Türü   : {results['number_type']}{Colors.RESET}")
        
        # Formatlar
        results['international_format'] = phonenumbers.format_number(
            parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )
        results['national_format'] = phonenumbers.format_number(
            parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL
        )
        
        print(f"{Colors.INFO}Uluslararası  : {results['international_format']}{Colors.RESET}")
        print(f"{Colors.INFO}Ulusal Format : {results['national_format']}{Colors.RESET}")
        
        # Olası e164 format
        e164_format = phonenumbers.format_number(
            parsed_number, phonenumbers.PhoneNumberFormat.E164
        )
        print(f"{Colors.INFO}E164 Format   : {e164_format}{Colors.RESET}")
        
    except phonenumbers.phonenumberutil.NumberParseException as e:
        print(f"{Colors.ERROR}[!] Numara parse edilemedi: {e}{Colors.RESET}")
        results['valid'] = False
    except Exception as e:
        print(f"{Colors.ERROR}[!] Beklenmeyen hata: {e}{Colors.RESET}")
        results['valid'] = False
    
    return results

def search_phone_online(phone_number):
    """Telefon numarasını online araştır"""
    print(f"\n{Colors.INFO}[*] Online araştırma linkleri:{Colors.RESET}\n")
    
    clean_number = phone_number.replace('+', '').replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
    
    search_links = {
        "Google": f"https://www.google.com/search?q={phone_number}",
        "TrueCaller": f"https://www.truecaller.com/search/tr/{clean_number}",
        "GetContact": f"https://www.getcontact.com/tr/search?number={phone_number}",
        "NumLookup": f"https://www.numlookup.com/?phone={clean_number}",
        "Sync.ME": f"https://sync.me/search/?phone={clean_number}",
        "411": f"https://www.411.com/phone/{clean_number}",
        "WhitePages": f"https://www.whitepages.com/phone/{clean_number}",
    }
    
    for site, url in search_links.items():
        print(f"{Colors.SUCCESS}→ {site:15} : {url}{Colors.RESET}")
    
    return search_links

def save_report(results, search_links):
    """Raporu kaydet"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = BASE_DIR / 'reports' / 'phone_search'
    report_dir.mkdir(parents=True, exist_ok=True)
    
    phone_safe = results['number'].replace('+', '').replace(' ', '_')
    report_file = report_dir / f"{phone_safe}_{timestamp}.txt"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("╔═══════════════════════════════════════════════════════════════╗\n")
        f.write("║            HIG-OSINT TELEFON NUMARASI RAPORU                 ║\n")
        f.write("╚═══════════════════════════════════════════════════════════════╝\n\n")
        f.write(f"Telefon Numarası: {results['number']}\n")
        f.write(f"Tarih: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n")
        f.write("="*65 + "\n\n")
        
        f.write("ANALİZ SONUÇLARI:\n")
        f.write(f"Geçerli          : {'✓ Evet' if results['valid'] else '✗ Hayır'}\n")
        
        if results['valid']:
            f.write(f"Ülke             : {results['country']} ({results['country_code']})\n")
            f.write(f"Lokasyon         : {results['location']}\n")
            if results['carrier']:
                f.write(f"Operatör         : {results['carrier']}\n")
            f.write(f"Numara Türü      : {results['number_type']}\n")
            if results['timezone']:
                f.write(f"Zaman Dilimi     : {', '.join(results['timezone'])}\n")
            f.write(f"Uluslararası     : {results['international_format']}\n")
            f.write(f"Ulusal Format    : {results['national_format']}\n")
        
        f.write("\n" + "-"*65 + "\n\n")
        f.write("ONLINE ARAŞTIRMA LİNKLERİ:\n")
        for site, url in search_links.items():
            f.write(f"  → {site:15} : {url}\n")
        
        f.write(f"\nRapor Dosyası: {report_file}\n")
    
    return report_file

def main():
    """Ana fonksiyon"""
    os.system('clear' if os.name != 'nt' else 'cls')
    print_header()
    
    print(f"{Colors.INFO}Telefon numarasını uluslararası formatta girin (+90XXXXXXXXXX){Colors.RESET}\n")
    
    phone_number = input(f"{Colors.INPUT}Telefon Numarası: {Colors.RESET}").strip()
    
    if not phone_number:
        print(f"{Colors.ERROR}[!] Telefon numarası boş olamaz!{Colors.RESET}")
        return
    
    # Analiz
    results = analyze_phone(phone_number)
    
    # Online araştırma
    search_links = search_phone_online(phone_number)
    
    # Özet
    print(f"\n{Colors.HEADER}╔════════════════════ SONUÇ ÖZETİ ══════════════════════╗{Colors.RESET}")
    print(f"{Colors.SUCCESS}Geçerli          : {'✓ Evet' if results['valid'] else '✗ Hayır'}{Colors.RESET}")
    if results['valid']:
        print(f"{Colors.SUCCESS}Ülke             : {results['country']}{Colors.RESET}")
        print(f"{Colors.SUCCESS}Lokasyon         : {results['location']}{Colors.RESET}")
        if results['carrier']:
            print(f"{Colors.SUCCESS}Operatör         : {results['carrier']}{Colors.RESET}")
        print(f"{Colors.SUCCESS}Numara Türü      : {results['number_type']}{Colors.RESET}")
    print(f"{Colors.HEADER}╚════════════════════════════════════════════════════════╝{Colors.RESET}\n")
    
    save = input(f"{Colors.INPUT}Raporu kaydetmek ister misiniz? (E/H): {Colors.RESET}").strip().upper()
    if save in ['E', 'Y', 'EVET', 'YES']:
        report_file = save_report(results, search_links)
        print(f"\n{Colors.SUCCESS}✓ Rapor kaydedildi: {report_file}{Colors.RESET}")
    
    input(f"\n{Colors.INPUT}Ana menüye dönmek için Enter'a basın...{Colors.RESET}")

if __name__ == "__main__":
    main()
