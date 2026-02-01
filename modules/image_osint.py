#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Image OSINT Module - Görsel OSINT ve EXIF Analiz Modülü
"""

import os
import sys
import json
import webbrowser
from datetime import datetime
from pathlib import Path
from colorama import Fore, Style

try:
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
except ImportError:
    print("[!] Pillow modülü bulunamadı. Yükleniyor...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "--break-system-packages"])
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS

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
║                     GÖRSEL OSINT MODÜLÜ                          ║
║                Image OSINT & EXIF Analysis Module                ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(header)

def save_result(filename, data):
    """Sonuçları kaydet"""
    try:
        reports_dir = Path('reports')
        reports_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = reports_dir / f"image_osint_{filename}_{timestamp}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"{Colors.SUCCESS}[+] Sonuçlar kaydedildi: {filepath}{Colors.RESET}")
        return True
    except Exception as e:
        print(f"{Colors.ERROR}[-] Kayıt hatası: {e}{Colors.RESET}")
        return False

def get_decimal_from_dms(dms, ref):
    """DMS (Degrees, Minutes, Seconds) formatını decimal'e çevir"""
    try:
        degrees = float(dms[0])
        minutes = float(dms[1]) / 60.0
        seconds = float(dms[2]) / 3600.0
        
        decimal = degrees + minutes + seconds
        
        if ref in ['S', 'W']:
            decimal = -decimal
        
        return decimal
    except:
        return None

def extract_gps_info(gps_data):
    """GPS bilgilerini çıkart"""
    if not gps_data:
        return None
    
    gps_info = {}
    
    for tag, value in gps_data.items():
        decoded = GPSTAGS.get(tag, tag)
        gps_info[decoded] = value
    
    # Koordinatları al
    lat = None
    lon = None
    
    if 'GPSLatitude' in gps_info and 'GPSLatitudeRef' in gps_info:
        lat = get_decimal_from_dms(gps_info['GPSLatitude'], gps_info['GPSLatitudeRef'])
    
    if 'GPSLongitude' in gps_info and 'GPSLongitudeRef' in gps_info:
        lon = get_decimal_from_dms(gps_info['GPSLongitude'], gps_info['GPSLongitudeRef'])
    
    result = {
        'latitude': lat,
        'longitude': lon,
        'altitude': gps_info.get('GPSAltitude'),
        'timestamp': gps_info.get('GPSTimeStamp'),
        'datestamp': gps_info.get('GPSDateStamp'),
        'raw_data': {k: str(v) for k, v in gps_info.items()}
    }
    
    return result

def extract_exif_data(image_path):
    """EXIF verilerini çıkart"""
    print(f"\n{Colors.INFO}[*] EXIF verileri çıkartılıyor: {image_path}{Colors.RESET}")
    
    try:
        image = Image.open(image_path)
        exif_data = image.getexif()
        
        if not exif_data:
            print(f"{Colors.WARNING}[!] EXIF verisi bulunamadı{Colors.RESET}")
            return None
        
        # Temel bilgiler
        result = {
            'filename': os.path.basename(image_path),
            'format': image.format,
            'size': f"{image.width}x{image.height}",
            'mode': image.mode,
            'exif_data': {},
            'gps_data': None
        }
        
        print(f"\n{Colors.SUCCESS}[+] Temel Bilgiler:{Colors.RESET}")
        print(f"  - Dosya: {result['filename']}")
        print(f"  - Format: {result['format']}")
        print(f"  - Boyut: {result['size']}")
        print(f"  - Mod: {result['mode']}")
        
        # EXIF etiketlerini çöz
        print(f"\n{Colors.SUCCESS}[+] EXIF Verileri:{Colors.RESET}")
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            
            # GPS verisi varsa ayrıca işle
            if tag == 'GPSInfo':
                gps_data = {}
                for gps_tag_id, gps_value in value.items():
                    gps_tag = GPSTAGS.get(gps_tag_id, gps_tag_id)
                    gps_data[gps_tag] = gps_value
                
                result['gps_data'] = extract_gps_info(gps_data)
            else:
                # Değeri string'e çevir
                try:
                    if isinstance(value, bytes):
                        value = value.decode('utf-8', errors='ignore')
                    result['exif_data'][tag] = str(value)
                except:
                    result['exif_data'][tag] = repr(value)
        
        # Önemli EXIF bilgilerini göster
        important_tags = [
            'Make', 'Model', 'Software', 'DateTime', 
            'DateTimeOriginal', 'Artist', 'Copyright'
        ]
        
        for tag in important_tags:
            if tag in result['exif_data']:
                print(f"  - {tag}: {result['exif_data'][tag]}")
        
        # GPS bilgilerini göster
        if result['gps_data']:
            print(f"\n{Colors.SUCCESS}[+] GPS Bilgileri:{Colors.RESET}")
            gps = result['gps_data']
            
            if gps['latitude'] and gps['longitude']:
                print(f"  - Koordinatlar: {gps['latitude']}, {gps['longitude']}")
                print(f"  - Google Maps: https://www.google.com/maps?q={gps['latitude']},{gps['longitude']}")
                
                if gps['altitude']:
                    print(f"  - Yükseklik: {gps['altitude']}")
                
                if gps['timestamp']:
                    print(f"  - Zaman: {gps['timestamp']}")
                
                if gps['datestamp']:
                    print(f"  - Tarih: {gps['datestamp']}")
        else:
            print(f"\n{Colors.WARNING}[!] GPS verisi bulunamadı{Colors.RESET}")
        
        return result
        
    except FileNotFoundError:
        print(f"{Colors.ERROR}[-] Dosya bulunamadı: {image_path}{Colors.RESET}")
        return None
    except Exception as e:
        print(f"{Colors.ERROR}[-] EXIF çıkarma hatası: {e}{Colors.RESET}")
        return None

def reverse_image_search(image_path):
    """Ters görsel arama"""
    print(f"\n{Colors.INFO}[*] Ters görsel arama araçları{Colors.RESET}")
    
    # Görsel arama servisleri
    services = {
        'Google Images': 'https://images.google.com/',
        'Yandex Images': 'https://yandex.com/images/',
        'TinEye': 'https://tineye.com/',
        'Bing Visual Search': 'https://www.bing.com/visualsearch',
        'Baidu Images': 'https://image.baidu.com/'
    }
    
    print(f"\n{Colors.SUCCESS}[+] Ters Görsel Arama Servisleri:{Colors.RESET}")
    for i, (service, url) in enumerate(services.items(), 1):
        print(f"  [{i}] {service}: {url}")
    
    print(f"\n{Colors.WARNING}[!] Not: Görseli manuel olarak yüklemeniz gerekecek{Colors.RESET}")
    print(f"{Colors.INFO}[*] Görsel yolu: {os.path.abspath(image_path)}{Colors.RESET}")
    
    choice = input(f"\n{Colors.INPUT}Servisleri tarayıcıda açmak ister misiniz? (E/H): {Colors.RESET}").strip().upper()
    if choice in ['E', 'Y', 'EVET', 'YES']:
        for service, url in services.items():
            print(f"{Colors.INFO}[*] Açılıyor: {service}{Colors.RESET}")
            webbrowser.open(url)
    
    return services

def analyze_image_metadata(image_path):
    """Görsel metadata analizini yap"""
    print(f"\n{Colors.INFO}[*] Detaylı metadata analizi yapılıyor...{Colors.RESET}")
    
    try:
        stat = os.stat(image_path)
        
        metadata = {
            'file_size': f"{stat.st_size / 1024:.2f} KB",
            'created': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
            'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            'accessed': datetime.fromtimestamp(stat.st_atime).strftime('%Y-%m-%d %H:%M:%S'),
        }
        
        print(f"\n{Colors.SUCCESS}[+] Dosya Metadata:{Colors.RESET}")
        print(f"  - Dosya Boyutu: {metadata['file_size']}")
        print(f"  - Oluşturulma: {metadata['created']}")
        print(f"  - Değiştirilme: {metadata['modified']}")
        print(f"  - Erişim: {metadata['accessed']}")
        
        return metadata
        
    except Exception as e:
        print(f"{Colors.ERROR}[-] Metadata hatası: {e}{Colors.RESET}")
        return None

def remove_exif_data(image_path, output_path=None):
    """EXIF verilerini temizle"""
    print(f"\n{Colors.INFO}[*] EXIF verileri temizleniyor...{Colors.RESET}")
    
    try:
        if output_path is None:
            name, ext = os.path.splitext(image_path)
            output_path = f"{name}_no_exif{ext}"
        
        image = Image.open(image_path)
        
        # EXIF verisiz kaydet
        data = list(image.getdata())
        image_without_exif = Image.new(image.mode, image.size)
        image_without_exif.putdata(data)
        image_without_exif.save(output_path)
        
        print(f"{Colors.SUCCESS}[+] EXIF verileri temizlendi{Colors.RESET}")
        print(f"{Colors.SUCCESS}[+] Kaydedildi: {output_path}{Colors.RESET}")
        
        return output_path
        
    except Exception as e:
        print(f"{Colors.ERROR}[-] EXIF temizleme hatası: {e}{Colors.RESET}")
        return None

def image_forensics_tools():
    """Görsel forensics araçları"""
    print(f"\n{Colors.MENU}=== Görsel Forensics Araçları ==={Colors.RESET}")
    
    tools = {
        'FotoForensics': {
            'url': 'https://fotoforensics.com/',
            'description': 'ELA (Error Level Analysis) ve diğer forensics analizleri'
        },
        'Forensically': {
            'url': 'https://29a.ch/photo-forensics/',
            'description': 'Çoklu forensics analiz araçları'
        },
        'Jeffrey\'s Image Metadata Viewer': {
            'url': 'http://exif.regex.info/exif.cgi',
            'description': 'Online EXIF viewer'
        },
        'InVID Verification': {
            'url': 'https://www.invid-project.eu/tools-and-services/invid-verification-plugin/',
            'description': 'Video ve görsel doğrulama aracı'
        },
        'Ghiro': {
            'url': 'https://www.getghiro.org/',
            'description': 'Otomatik görsel forensics aracı'
        }
    }
    
    print(f"\n{Colors.SUCCESS}[+] Önerilen Araçlar:{Colors.RESET}")
    for tool, info in tools.items():
        print(f"\n  - {tool}")
        print(f"    URL: {info['url']}")
        print(f"    Açıklama: {info['description']}")
    
    return tools

def image_osint_menu():
    """Görsel OSINT menüsü"""
    while True:
        clear_screen()
        print_header()
        
        menu = f"""{Colors.MENU}
╔═══════════════════════════════════════════════════════════════╗
║                   GÖRSEL OSINT MENÜSÜ                        ║
╚═══════════════════════════════════════════════════════════════╝

  {Colors.INPUT}[1]{Colors.RESET} 📸 EXIF Verisi Çıkart
  {Colors.INPUT}[2]{Colors.RESET} 🔍 Ters Görsel Arama
  {Colors.INPUT}[3]{Colors.RESET} 📊 Metadata Analizi
  {Colors.INPUT}[4]{Colors.RESET} 🧹 EXIF Verisi Temizle
  {Colors.INPUT}[5]{Colors.RESET} 🛠️  Forensics Araçları
  {Colors.INPUT}[0]{Colors.RESET} 🔙 Ana Menüye Dön

{Colors.INPUT}Seçiminiz: {Colors.RESET}"""
        
        print(menu, end='')
        choice = input().strip()
        
        if choice == '0':
            break
        elif choice == '1':
            image_path = input(f"\n{Colors.INPUT}Görsel dosya yolunu girin: {Colors.RESET}").strip()
            if image_path and os.path.exists(image_path):
                result = extract_exif_data(image_path)
                if result:
                    save_result(f"exif_{os.path.basename(image_path)}", result)
            else:
                print(f"{Colors.ERROR}[-] Dosya bulunamadı{Colors.RESET}")
        elif choice == '2':
            image_path = input(f"\n{Colors.INPUT}Görsel dosya yolunu girin: {Colors.RESET}").strip()
            if image_path and os.path.exists(image_path):
                reverse_image_search(image_path)
            else:
                print(f"{Colors.ERROR}[-] Dosya bulunamadı{Colors.RESET}")
        elif choice == '3':
            image_path = input(f"\n{Colors.INPUT}Görsel dosya yolunu girin: {Colors.RESET}").strip()
            if image_path and os.path.exists(image_path):
                result = analyze_image_metadata(image_path)
                if result:
                    save_result(f"metadata_{os.path.basename(image_path)}", result)
            else:
                print(f"{Colors.ERROR}[-] Dosya bulunamadı{Colors.RESET}")
        elif choice == '4':
            image_path = input(f"\n{Colors.INPUT}Görsel dosya yolunu girin: {Colors.RESET}").strip()
            if image_path and os.path.exists(image_path):
                output_path = input(f"{Colors.INPUT}Çıktı dosya yolu (boş bırakabilirsiniz): {Colors.RESET}").strip()
                remove_exif_data(image_path, output_path if output_path else None)
            else:
                print(f"{Colors.ERROR}[-] Dosya bulunamadı{Colors.RESET}")
        elif choice == '5':
            image_forensics_tools()
        else:
            print(f"{Colors.ERROR}[-] Geçersiz seçim!{Colors.RESET}")
        
        input(f"\n{Colors.INPUT}Devam etmek için Enter'a basın...{Colors.RESET}")

def main():
    """Ana fonksiyon"""
    try:
        image_osint_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}[!] İşlem iptal edildi{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.ERROR}[-] Beklenmeyen hata: {e}{Colors.RESET}")

if __name__ == "__main__":
    main()
