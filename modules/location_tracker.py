cat > /home/claude/hig_modules/location_tracker.py << 'EOFLOC'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
from pathlib import Path
from colorama import Fore, Style
from datetime import datetime

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
║            🗺️  KONUM TAKİBİ MODÜLÜ 🗺️                       ║
╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}""")

def track_coordinates(lat, lon):
    print(f"\n{Colors.INFO}[*] Konum bilgisi alınıyor...{Colors.RESET}\n")
    
    try:
        response = requests.get(f'https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json', timeout=10)
        if response.status_code == 200:
            data = response.json()
            address = data.get('address', {})
            print(f"{Colors.SUCCESS}✓ Konum Bilgisi:{Colors.RESET}")
            print(f"  Koordinat   : {lat}, {lon}")
            print(f"  Adres       : {data.get('display_name')}")
            print(f"  Ülke        : {address.get('country')}")
            print(f"  Şehir       : {address.get('city') or address.get('town') or address.get('village')}")
            
            maps = {
                "Google Maps": f"https://www.google.com/maps?q={lat},{lon}",
                "OpenStreetMap": f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}&zoom=15",
                "Bing Maps": f"https://www.bing.com/maps?cp={lat}~{lon}&lvl=15",
                "Yandex Maps": f"https://yandex.com/maps/?ll={lon},{lat}&z=15",
            }
            
            print(f"\n{Colors.INFO}[*] Harita Linkleri:{Colors.RESET}")
            for name, url in maps.items():
                print(f"{Colors.SUCCESS}→ {name:15} : {url}{Colors.RESET}")
            
            return data, maps
    except Exception as e:
        print(f"{Colors.ERROR}✗ Hata: {e}{Colors.RESET}")
    return None, None

def main():
    os.system('clear' if os.name != 'nt' else 'cls')
    print_header()
    
    print(f"{Colors.INFO}Enlem (latitude) ve boylam (longitude) koordinatlarını girin.{Colors.RESET}\n")
    
    lat = input(f"{Colors.INPUT}Enlem (örn: 41.0082): {Colors.RESET}").strip()
    lon = input(f"{Colors.INPUT}Boylam (örn: 28.9784): {Colors.RESET}").strip()
    
    if not lat or not lon:
        print(f"{Colors.ERROR}[!] Koordinatlar boş olamaz!{Colors.RESET}")
        return
    
    try:
        lat = float(lat)
        lon = float(lon)
    except:
        print(f"{Colors.ERROR}[!] Geçersiz koordinat formatı!{Colors.RESET}")
        return
    
    data, maps = track_coordinates(lat, lon)
    
    if data:
        if input(f"\n{Colors.INPUT}Kaydet? (E/H): {Colors.RESET}").strip().upper() in ['E', 'Y', 'EVET', 'YES']:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_dir = BASE_DIR / 'reports' / 'location_tracker'
            report_dir.mkdir(parents=True, exist_ok=True)
            report_file = report_dir / f"location_{timestamp}.txt"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(f"Konum Takibi Raporu\n" + "="*65 + "\n")
                f.write(f"Koordinat: {lat}, {lon}\n")
                f.write(f"Adres: {data.get('display_name')}\n\n")
                f.write("Harita Linkleri:\n")
                for name, url in maps.items():
                    f.write(f"{name}: {url}\n")
            print(f"{Colors.SUCCESS}✓ {report_file}{Colors.RESET}")
    
    input(f"\n{Colors.INPUT}Enter...{Colors.RESET}")

if __name__ == "__main__":
    main()
EOFLOC

cat > /home/claude/hig_modules/image_osint.py << 'EOFIMAGE'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path
from colorama import Fore, Style

try:
    from PIL import Image
    from PIL.ExifTags import TAGS
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "--break-system-packages"])
    from PIL import Image
    from PIL.ExifTags import TAGS

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
║            📸 GÖRSEL OSINT (EXIF) MODÜLÜ 📸                 ║
╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}""")

def extract_exif(image_path):
    print(f"\n{Colors.INFO}[*] EXIF verileri çıkarılıyor...{Colors.RESET}\n")
    
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        
        if not exif_data:
            print(f"{Colors.ERROR}✗ EXIF verisi bulunamadı!{Colors.RESET}")
            return None
        
        exif_info = {}
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            exif_info[tag] = value
        
        print(f"{Colors.SUCCESS}✓ EXIF Bilgileri:{Colors.RESET}\n")
        
        important_tags = ['Make', 'Model', 'DateTime', 'GPSInfo', 'Software', 'Artist', 'Copyright']
        
        for tag in important_tags:
            if tag in exif_info:
                print(f"{Colors.INFO}  {tag:15} : {exif_info[tag]}{Colors.RESET}")
        
        if 'GPSInfo' in exif_info:
            print(f"\n{Colors.WARNING}⚠ GPS bilgisi bulundu! Konum verisi mevcut.{Colors.RESET}")
        
        return exif_info
        
    except Exception as e:
        print(f"{Colors.ERROR}✗ Hata: {e}{Colors.RESET}")
        return None

def main():
    os.system('clear' if os.name != 'nt' else 'cls')
    print_header()
    
    image_path = input(f"{Colors.INPUT}Görsel dosya yolu: {Colors.RESET}").strip()
    
    if not os.path.exists(image_path):
        print(f"{Colors.ERROR}[!] Dosya bulunamadı!{Colors.RESET}")
        return
    
    exif_info = extract_exif(image_path)
    
    if exif_info:
        print(f"\n{Colors.SUCCESS}✓ Toplam {len(exif_info)} EXIF etiketi bulundu.{Colors.RESET}")
        
        print(f"\n{Colors.INFO}Reverse Image Search Linkleri:{Colors.RESET}")
        filename = os.path.basename(image_path)
        print(f"{Colors.SUCCESS}→ Google Images: https://images.google.com/{Colors.RESET}")
        print(f"{Colors.SUCCESS}→ TinEye: https://tineye.com/{Colors.RESET}")
        print(f"{Colors.SUCCESS}→ Yandex: https://yandex.com/images/{Colors.RESET}")
    
    input(f"\n{Colors.INPUT}Enter...{Colors.RESET}")

if __name__ == "__main__":
    main()
EOFIMAGE

echo "Location Tracker ve Image OSINT modülleri oluşturuldu"
