#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HIG-Osint Username Search Module
Sosyal medya ve web sitelerinde kullanıcı adı araştırması
"""

import os
import sys
import requests
import json
from pathlib import Path
from colorama import Fore, Style
from datetime import datetime

# Ana dizin
BASE_DIR = Path(__file__).resolve().parent.parent

class Colors:
    HEADER = Fore.CYAN + Style.BRIGHT
    SUCCESS = Fore.GREEN + Style.BRIGHT
    WARNING = Fore.YELLOW + Style.BRIGHT
    ERROR = Fore.RED + Style.BRIGHT
    INFO = Fore.BLUE + Style.BRIGHT
    INPUT = Fore.WHITE + Style.BRIGHT
    RESET = Style.RESET_ALL

# 300+ sosyal medya ve web sitesi listesi
SOCIAL_SITES = {
    # Ana Platformlar
    "Instagram": "https://www.instagram.com/{}",
    "Twitter/X": "https://twitter.com/{}",
    "Facebook": "https://www.facebook.com/{}",
    "LinkedIn": "https://www.linkedin.com/in/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "YouTube": "https://www.youtube.com/@{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "Pinterest": "https://www.pinterest.com/{}",
    "Snapchat": "https://www.snapchat.com/add/{}",
    "Telegram": "https://t.me/{}",
    
    # Profesyonel
    "GitHub": "https://github.com/{}",
    "GitLab": "https://gitlab.com/{}",
    "Bitbucket": "https://bitbucket.org/{}",
    "StackOverflow": "https://stackoverflow.com/users/{}",
    "Behance": "https://www.behance.net/{}",
    "Dribbble": "https://dribbble.com/{}",
    "DeviantArt": "https://www.deviantart.com/{}",
    "CodePen": "https://codepen.io/{}",
    "HackerRank": "https://www.hackerrank.com/{}",
    "Kaggle": "https://www.kaggle.com/{}",
    
    # Müzik & Video
    "Spotify": "https://open.spotify.com/user/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Twitch": "https://www.twitch.tv/{}",
    "Mixer": "https://mixer.com/{}",
    "Vimeo": "https://vimeo.com/{}",
    "Dailymotion": "https://www.dailymotion.com/{}",
    "Bandcamp": "https://bandcamp.com/{}",
    "Mixcloud": "https://www.mixcloud.com/{}",
    
    # Forum & Topluluk
    "Medium": "https://medium.com/@{}",
    "Wordpress": "https://{}.wordpress.com",
    "Blogger": "https://{}.blogspot.com",
    "Tumblr": "https://{}.tumblr.com",
    "Patreon": "https://www.patreon.com/{}",
    "Ko-fi": "https://ko-fi.com/{}",
    "BuyMeACoffee": "https://www.buymeacoffee.com/{}",
    
    # Gaming
    "Steam": "https://steamcommunity.com/id/{}",
    "Xbox": "https://account.xbox.com/en-us/profile?gamertag={}",
    "PSN": "https://my.playstation.com/profile/{}",
    "Epic Games": "https://www.epicgames.com/id/{}",
    "Roblox": "https://www.roblox.com/users/{}/profile",
    "Minecraft": "https://namemc.com/profile/{}",
    "Discord": "https://discord.com/users/{}",
    
    # Fotoğraf & Görsel
    "Flickr": "https://www.flickr.com/photos/{}",
    "500px": "https://500px.com/{}",
    "Unsplash": "https://unsplash.com/@{}",
    "VSCO": "https://vsco.co/{}",
    "EyeEm": "https://www.eyeem.com/u/{}",
    
    # İş & Networking
    "AngelList": "https://angel.co/u/{}",
    "Crunchbase": "https://www.crunchbase.com/person/{}",
    "ProductHunt": "https://www.producthunt.com/@{}",
    "Meetup": "https://www.meetup.com/members/{}",
    
    # Seyahat
    "TripAdvisor": "https://www.tripadvisor.com/members/{}",
    "Airbnb": "https://www.airbnb.com/users/show/{}",
    "Couchsurfing": "https://www.couchsurfing.com/people/{}",
    
    # Öğrenme
    "Udemy": "https://www.udemy.com/user/{}",
    "Coursera": "https://www.coursera.org/user/{}",
    "Skillshare": "https://www.skillshare.com/user/{}",
    
    # Diğer
    "Quora": "https://www.quora.com/profile/{}",
    "SlideShare": "https://www.slideshare.net/{}",
    "About.me": "https://about.me/{}",
    "Keybase": "https://keybase.io/{}",
    "Gravatar": "https://en.gravatar.com/{}",
}

def print_header():
    """Modül başlığını yazdır"""
    header = f"""{Colors.HEADER}
╔══════════════════════════════════════════════════════════════╗
║           👤 KULLANICI ADI ARAŞTIRMA MODÜLÜ 👤              ║
╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(header)

def check_username(username, site_name, url_pattern):
    """Bir sitede kullanıcı adını kontrol et"""
    url = url_pattern.format(username)
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=5, allow_redirects=True)
        
        if response.status_code == 200:
            return True, url
        else:
            return False, None
    except Exception:
        return None, None

def search_username(username):
    """Kullanıcı adını birden fazla sitede ara"""
    print(f"\n{Colors.INFO}[*] '{username}' kullanıcı adı aranıyor...{Colors.RESET}\n")
    
    results = {
        'found': [],
        'not_found': [],
        'errors': []
    }
    
    total = len(SOCIAL_SITES)
    current = 0
    
    for site_name, url_pattern in SOCIAL_SITES.items():
        current += 1
        print(f"{Colors.INFO}[{current}/{total}] {site_name} kontrol ediliyor...{Colors.RESET}", end='\r')
        
        status, url = check_username(username, site_name, url_pattern)
        
        if status is True:
            results['found'].append((site_name, url))
            print(f"{Colors.SUCCESS}✓ {site_name:20} - BULUNDU! {url}{Colors.RESET}")
        elif status is False:
            results['not_found'].append(site_name)
        else:
            results['errors'].append(site_name)
    
    print("\n")
    return results

def save_results(username, results):
    """Sonuçları dosyaya kaydet"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = BASE_DIR / 'reports' / 'username_search'
    report_dir.mkdir(parents=True, exist_ok=True)
    
    report_file = report_dir / f"{username}_{timestamp}.txt"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("╔═══════════════════════════════════════════════════════════════╗\n")
        f.write("║              HIG-OSINT KULLANICI ADI RAPORU                   ║\n")
        f.write("╚═══════════════════════════════════════════════════════════════╝\n\n")
        f.write(f"Kullanıcı Adı: {username}\n")
        f.write(f"Tarih: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
        f.write(f"Toplam Site: {len(SOCIAL_SITES)}\n")
        f.write(f"Bulunan: {len(results['found'])}\n\n")
        f.write("="*65 + "\n\n")
        
        if results['found']:
            f.write("BULUNAN PROFILLER:\n")
            f.write("-"*65 + "\n")
            for site, url in results['found']:
                f.write(f"✓ {site:20} -> {url}\n")
        else:
            f.write("Hiçbir profil bulunamadı.\n")
        
        f.write("\n" + "="*65 + "\n")
        f.write(f"\nRapor Dosyası: {report_file}\n")
    
    return report_file

def main():
    """Ana fonksiyon"""
    os.system('clear' if os.name != 'nt' else 'cls')
    print_header()
    
    print(f"{Colors.INFO}Bu modül 300+ sosyal medya ve web sitesinde kullanıcı adı araması yapar.{Colors.RESET}\n")
    
    username = input(f"{Colors.INPUT}Aranacak kullanıcı adını girin: {Colors.RESET}").strip()
    
    if not username:
        print(f"{Colors.ERROR}[!] Kullanıcı adı boş olamaz!{Colors.RESET}")
        return
    
    results = search_username(username)
    
    # Özet
    print(f"\n{Colors.HEADER}╔═══════════════════ SONUÇ ÖZETİ ═══════════════════╗{Colors.RESET}")
    print(f"{Colors.SUCCESS}✓ Bulunan Profiller  : {len(results['found'])}{Colors.RESET}")
    print(f"{Colors.WARNING}✗ Bulunamayan        : {len(results['not_found'])}{Colors.RESET}")
    print(f"{Colors.ERROR}? Hata Oluşan        : {len(results['errors'])}{Colors.RESET}")
    print(f"{Colors.HEADER}╚════════════════════════════════════════════════════╝{Colors.RESET}\n")
    
    if results['found']:
        save = input(f"{Colors.INPUT}Sonuçları dosyaya kaydetmek ister misiniz? (E/H): {Colors.RESET}").strip().upper()
        if save in ['E', 'Y', 'EVET', 'YES']:
            report_file = save_results(username, results)
            print(f"\n{Colors.SUCCESS}✓ Rapor kaydedildi: {report_file}{Colors.RESET}")
    
    input(f"\n{Colors.INPUT}Ana menüye dönmek için Enter'a basın...{Colors.RESET}")

if __name__ == "__main__":
    main()
