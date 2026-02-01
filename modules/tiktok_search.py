#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TikTok Search Module - TikTok OSINT Araştırma Modülü
"""

import os
import sys
import json
import webbrowser
from datetime import datetime
from pathlib import Path
from colorama import Fore, Style
from urllib.parse import quote

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
║                   TIKTOK ARAŞTIRMA MODÜLÜ                        ║
║                  TikTok Search OSINT Module                      ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(header)

def save_result(filename, data):
    """Sonuçları kaydet"""
    try:
        reports_dir = Path('reports')
        reports_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = reports_dir / f"tiktok_{filename}_{timestamp}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"{Colors.SUCCESS}[+] Sonuçlar kaydedildi: {filepath}{Colors.RESET}")
        return True
    except Exception as e:
        print(f"{Colors.ERROR}[-] Kayıt hatası: {e}{Colors.RESET}")
        return False

def search_tiktok_user(username):
    """TikTok kullanıcı ara"""
    print(f"\n{Colors.INFO}[*] TikTok kullanıcısı aranıyor: @{username}{Colors.RESET}")
    
    # TikTok profil URL'leri
    urls = {
        'Profil': f"https://www.tiktok.com/@{username}",
        'Web Profil': f"https://www.tiktok.com/@{username}",
        'Arama': f"https://www.tiktok.com/search/user?q={quote(username)}",
    }
    
    print(f"\n{Colors.SUCCESS}[+] TikTok Profil Linkleri:{Colors.RESET}")
    for link_type, url in urls.items():
        print(f"  - {link_type}: {url}")
    
    # Tarayıcıda aç
    choice = input(f"\n{Colors.INPUT}Profili tarayıcıda açmak ister misiniz? (E/H): {Colors.RESET}").strip().upper()
    if choice in ['E', 'Y', 'EVET', 'YES']:
        webbrowser.open(urls['Profil'])
    
    return urls

def search_tiktok_hashtag(hashtag):
    """TikTok hashtag ara"""
    print(f"\n{Colors.INFO}[*] TikTok hashtag aranıyor: #{hashtag}{Colors.RESET}")
    
    # Hashtag'ten # işaretini temizle
    hashtag = hashtag.lstrip('#')
    
    urls = {
        'Hashtag': f"https://www.tiktok.com/tag/{hashtag}",
        'Arama': f"https://www.tiktok.com/search?q=%23{quote(hashtag)}",
    }
    
    print(f"\n{Colors.SUCCESS}[+] TikTok Hashtag Linkleri:{Colors.RESET}")
    for link_type, url in urls.items():
        print(f"  - {link_type}: {url}")
    
    choice = input(f"\n{Colors.INPUT}Hashtag'i tarayıcıda açmak ister misiniz? (E/H): {Colors.RESET}").strip().upper()
    if choice in ['E', 'Y', 'EVET', 'YES']:
        webbrowser.open(urls['Hashtag'])
    
    return urls

def search_tiktok_sound(sound_name):
    """TikTok ses/müzik ara"""
    print(f"\n{Colors.INFO}[*] TikTok ses aranıyor: {sound_name}{Colors.RESET}")
    
    urls = {
        'Ses Arama': f"https://www.tiktok.com/search?q={quote(sound_name)}&t=sound",
        'Genel Arama': f"https://www.tiktok.com/search?q={quote(sound_name)}",
    }
    
    print(f"\n{Colors.SUCCESS}[+] TikTok Ses Arama Linkleri:{Colors.RESET}")
    for link_type, url in urls.items():
        print(f"  - {link_type}: {url}")
    
    return urls

def search_tiktok_video(video_id):
    """TikTok video ID ile ara"""
    print(f"\n{Colors.INFO}[*] TikTok video aranıyor: {video_id}{Colors.RESET}")
    
    # Video ID formatını kontrol et
    if not video_id.isdigit() or len(video_id) < 15:
        print(f"{Colors.WARNING}[!] Geçersiz video ID formatı. 19 haneli sayı olmalıdır.{Colors.RESET}")
        return None
    
    urls = {
        'Video': f"https://www.tiktok.com/@username/video/{video_id}",
        'Alternatif Link': f"https://vm.tiktok.com/{video_id}",
    }
    
    print(f"\n{Colors.SUCCESS}[+] TikTok Video Linkleri:{Colors.RESET}")
    for link_type, url in urls.items():
        print(f"  - {link_type}: {url}")
    
    print(f"\n{Colors.INFO}[*] Not: Video linkini tam olarak bilmiyorsanız,")
    print(f"    kullanıcı adını bilmeniz gerekebilir.{Colors.RESET}")
    
    return urls

def advanced_tiktok_search():
    """Gelişmiş TikTok arama"""
    print(f"\n{Colors.MENU}=== Gelişmiş TikTok Arama ==={Colors.RESET}")
    
    print(f"\n{Colors.INFO}[*] Arama Parametreleri:{Colors.RESET}")
    keyword = input(f"  Anahtar kelime: ").strip()
    
    if not keyword:
        print(f"{Colors.ERROR}[-] Anahtar kelime boş olamaz!{Colors.RESET}")
        return None
    
    # Arama tipleri
    search_types = {
        'Kullanıcı': f"https://www.tiktok.com/search/user?q={quote(keyword)}",
        'Video': f"https://www.tiktok.com/search/video?q={quote(keyword)}",
        'Hashtag': f"https://www.tiktok.com/search?q=%23{quote(keyword)}",
        'Ses': f"https://www.tiktok.com/search?q={quote(keyword)}&t=sound",
        'Canlı': f"https://www.tiktok.com/search?q={quote(keyword)}&t=live",
    }
    
    print(f"\n{Colors.SUCCESS}[+] Arama Linkleri:{Colors.RESET}")
    for search_type, url in search_types.items():
        print(f"  - {search_type}: {url}")
    
    choice = input(f"\n{Colors.INPUT}Aramaları tarayıcıda açmak ister misiniz? (E/H): {Colors.RESET}").strip().upper()
    if choice in ['E', 'Y', 'EVET', 'YES']:
        for search_type, url in search_types.items():
            print(f"{Colors.INFO}[*] Açılıyor: {search_type}{Colors.RESET}")
            webbrowser.open(url)
    
    return search_types

def tiktok_analytics_tools():
    """TikTok analiz araçları"""
    print(f"\n{Colors.MENU}=== TikTok Analiz Araçları ==={Colors.RESET}")
    
    tools = {
        'TikTok Analytics': {
            'url': 'https://www.tiktok.com/analytics/',
            'description': 'Resmi TikTok analitik aracı (hesap gerektirir)'
        },
        'TikBuddy': {
            'url': 'https://tikbuddy.com/',
            'description': 'TikTok profil ve video analizi'
        },
        'Pentos': {
            'url': 'https://app.pentos.io/',
            'description': 'TikTok analitik ve izleme platformu'
        },
        'Analisa.io': {
            'url': 'https://analisa.io/tiktok-analytics',
            'description': 'TikTok profil ve hashtag analizi'
        },
        'TikTokCounter': {
            'url': 'https://tiktokcounter.net/',
            'description': 'Gerçek zamanlı TikTok takipçi sayacı'
        },
        'Exolyt': {
            'url': 'https://exolyt.com/',
            'description': 'TikTok analitik ve izleme'
        }
    }
    
    print(f"\n{Colors.SUCCESS}[+] Önerilen Araçlar:{Colors.RESET}")
    for tool, info in tools.items():
        print(f"\n  - {tool}")
        print(f"    URL: {info['url']}")
        print(f"    Açıklama: {info['description']}")
    
    return tools

def tiktok_download_tools():
    """TikTok video indirme araçları"""
    print(f"\n{Colors.MENU}=== TikTok Video İndirme Araçları ==={Colors.RESET}")
    
    tools = {
        'SnapTik': 'https://snaptik.app/',
        'TikMate': 'https://tikmate.online/',
        'SaveTT': 'https://savett.cc/',
        'TikTok Downloader': 'https://tiktokdownloader.com/',
        'SSSTik': 'https://ssstik.io/',
        'TikDD': 'https://tikdd.cc/'
    }
    
    print(f"\n{Colors.SUCCESS}[+] Video İndirme Araçları:{Colors.RESET}")
    for tool, url in tools.items():
        print(f"  - {tool}: {url}")
    
    print(f"\n{Colors.WARNING}[!] Not: Bu araçları kullanırken telif haklarına dikkat edin!{Colors.RESET}")
    
    return tools

def tiktok_profile_info():
    """TikTok profil bilgileri toplama rehberi"""
    print(f"\n{Colors.MENU}=== TikTok Profil Bilgileri Toplama Rehberi ==={Colors.RESET}")
    
    info_points = [
        "Kullanıcı Adı (@username)",
        "Görünen İsim",
        "Bio/Açıklama",
        "Profil Fotoğrafı",
        "Takipçi Sayısı",
        "Takip Edilen Sayısı",
        "Beğeni Sayısı",
        "Video Sayısı",
        "Doğrulanmış Hesap mı?",
        "Bağlantılı Sosyal Medya Hesapları",
        "Paylaşılan Videolar",
        "En Popüler Videolar",
        "Kullanılan Hashtag'ler",
        "Kullanılan Müzikler/Sesler",
        "Videolarda Görünen Konum Bilgileri",
        "İşbirliği Yaptığı Hesaplar",
        "Düet ve Stitch Videoları"
    ]
    
    print(f"\n{Colors.SUCCESS}[+] Toplanabilecek Bilgiler:{Colors.RESET}")
    for i, info in enumerate(info_points, 1):
        print(f"  {i}. {info}")
    
    print(f"\n{Colors.INFO}[*] İpuçları:{Colors.RESET}")
    print(f"  - Video açıklamalarını ve hashtag'leri inceleyin")
    print(f"  - Profil linklerini kontrol edin (Instagram, YouTube vb.)")
    print(f"  - Video içeriklerinden konum ipuçları arayın")
    print(f"  - Yorum bölümlerini inceleyin")
    print(f"  - Düzenli olarak paylaşım yapılan saatleri not edin")

def tiktok_osint_resources():
    """TikTok OSINT kaynakları"""
    print(f"\n{Colors.MENU}=== TikTok OSINT Kaynakları ==={Colors.RESET}")
    
    resources = {
        'OSINT Framework - TikTok': 'https://osintframework.com/',
        'Bellingcat TikTok Guide': 'https://www.bellingcat.com/',
        'TikTok Transparency Center': 'https://www.tiktok.com/transparency/',
        'TikTok Community Guidelines': 'https://www.tiktok.com/community-guidelines',
        'TikTok Creator Portal': 'https://www.tiktok.com/creators/creator-portal/',
    }
    
    print(f"\n{Colors.SUCCESS}[+] Faydalı Kaynaklar:{Colors.RESET}")
    for resource, url in resources.items():
        print(f"  - {resource}: {url}")
    
    print(f"\n{Colors.INFO}[*] Ek İpuçları:{Colors.RESET}")
    print(f"  - TikTok API limitlerinin farkında olun")
    print(f"  - Gizlilik ayarlarını kontrol edin")
    print(f"  - Yasal sınırlamalara uyun")
    print(f"  - Doğrulama için çoklu kaynak kullanın")

def tiktok_search_menu():
    """TikTok arama menüsü"""
    while True:
        clear_screen()
        print_header()
        
        menu = f"""{Colors.MENU}
╔═══════════════════════════════════════════════════════════════╗
║                  TIKTOK ARAŞTIRMA MENÜSÜ                     ║
╚═══════════════════════════════════════════════════════════════╝

  {Colors.INPUT}[1]{Colors.RESET} 👤 Kullanıcı Ara
  {Colors.INPUT}[2]{Colors.RESET} #️⃣  Hashtag Ara
  {Colors.INPUT}[3]{Colors.RESET} 🎵 Ses/Müzik Ara
  {Colors.INPUT}[4]{Colors.RESET} 🎬 Video ID ile Ara
  {Colors.INPUT}[5]{Colors.RESET} 🔍 Gelişmiş Arama
  {Colors.INPUT}[6]{Colors.RESET} 📊 Analiz Araçları
  {Colors.INPUT}[7]{Colors.RESET} 📥 İndirme Araçları
  {Colors.INPUT}[8]{Colors.RESET} 📋 Profil Bilgileri Rehberi
  {Colors.INPUT}[9]{Colors.RESET} 🛠️  OSINT Kaynakları
  {Colors.INPUT}[0]{Colors.RESET} 🔙 Ana Menüye Dön

{Colors.INPUT}Seçiminiz: {Colors.RESET}"""
        
        print(menu, end='')
        choice = input().strip()
        
        if choice == '0':
            break
        elif choice == '1':
            username = input(f"\n{Colors.INPUT}TikTok kullanıcı adı girin (@ olmadan): {Colors.RESET}").strip()
            if username:
                username = username.lstrip('@')
                result = search_tiktok_user(username)
                save_result(f"user_{username}", result)
        elif choice == '2':
            hashtag = input(f"\n{Colors.INPUT}Hashtag girin (# ile veya olmadan): {Colors.RESET}").strip()
            if hashtag:
                result = search_tiktok_hashtag(hashtag)
                save_result(f"hashtag_{hashtag.lstrip('#')}", result)
        elif choice == '3':
            sound_name = input(f"\n{Colors.INPUT}Ses/müzik adı girin: {Colors.RESET}").strip()
            if sound_name:
                result = search_tiktok_sound(sound_name)
                save_result(f"sound_{sound_name}", result)
        elif choice == '4':
            video_id = input(f"\n{Colors.INPUT}Video ID girin: {Colors.RESET}").strip()
            if video_id:
                result = search_tiktok_video(video_id)
                if result:
                    save_result(f"video_{video_id}", result)
        elif choice == '5':
            result = advanced_tiktok_search()
            if result:
                save_result("advanced_search", result)
        elif choice == '6':
            tiktok_analytics_tools()
        elif choice == '7':
            tiktok_download_tools()
        elif choice == '8':
            tiktok_profile_info()
        elif choice == '9':
            tiktok_osint_resources()
        else:
            print(f"{Colors.ERROR}[-] Geçersiz seçim!{Colors.RESET}")
        
        input(f"\n{Colors.INPUT}Devam etmek için Enter'a basın...{Colors.RESET}")

def main():
    """Ana fonksiyon"""
    try:
        tiktok_search_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}[!] İşlem iptal edildi{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.ERROR}[-] Beklenmeyen hata: {e}{Colors.RESET}")

if __name__ == "__main__":
    main()
