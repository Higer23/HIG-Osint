#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Facebook Search Module - Facebook OSINT Araştırma Modülü
"""

import os
import sys
import json
import requests
import webbrowser
from datetime import datetime
from colorama import Fore, Style
from pathlib import Path
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
║                  FACEBOOK ARAŞTIRMA MODÜLÜ                       ║
║                  Facebook Search OSINT Module                    ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(header)

def save_result(filename, data):
    """Sonuçları kaydet"""
    try:
        reports_dir = Path('reports')
        reports_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = reports_dir / f"facebook_{filename}_{timestamp}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"{Colors.SUCCESS}[+] Sonuçlar kaydedildi: {filepath}{Colors.RESET}")
        return True
    except Exception as e:
        print(f"{Colors.ERROR}[-] Kayıt hatası: {e}{Colors.RESET}")
        return False

def search_facebook_people(query):
    """Facebook'ta kişi ara"""
    print(f"\n{Colors.INFO}[*] Facebook'ta kişi aranıyor: {query}{Colors.RESET}")
    
    # Facebook arama URL'leri
    search_urls = {
        'Genel Arama': f"https://www.facebook.com/search/top/?q={quote(query)}",
        'Kişi Arama': f"https://www.facebook.com/search/people/?q={quote(query)}",
        'Fotoğraf Arama': f"https://www.facebook.com/search/photos/?q={quote(query)}",
        'Video Arama': f"https://www.facebook.com/search/videos/?q={quote(query)}",
        'Gönderi Arama': f"https://www.facebook.com/search/posts/?q={quote(query)}",
        'Sayfa Arama': f"https://www.facebook.com/search/pages/?q={quote(query)}",
        'Grup Arama': f"https://www.facebook.com/search/groups/?q={quote(query)}",
        'Etkinlik Arama': f"https://www.facebook.com/search/events/?q={quote(query)}"
    }
    
    print(f"\n{Colors.SUCCESS}[+] Facebook Arama Linkleri:{Colors.RESET}")
    for search_type, url in search_urls.items():
        print(f"  - {search_type}: {url}")
    
    # Tarayıcıda aç seçeneği
    choice = input(f"\n{Colors.INPUT}Bu linkleri tarayıcıda açmak ister misiniz? (E/H): {Colors.RESET}").strip().upper()
    if choice in ['E', 'Y', 'EVET', 'YES']:
        for search_type, url in search_urls.items():
            print(f"{Colors.INFO}[*] Açılıyor: {search_type}{Colors.RESET}")
            webbrowser.open(url)
    
    return search_urls

def search_by_email(email):
    """E-posta ile Facebook profil ara"""
    print(f"\n{Colors.INFO}[*] E-posta ile Facebook profili aranıyor: {email}{Colors.RESET}")
    
    urls = {
        'Facebook Arama': f"https://www.facebook.com/search/top/?q={quote(email)}",
        'Facebook Şifre Sıfırlama': f"https://www.facebook.com/login/identify/?ctx=recover",
    }
    
    print(f"\n{Colors.SUCCESS}[+] Kullanışlı Linkler:{Colors.RESET}")
    print(f"  1. Facebook Arama: {urls['Facebook Arama']}")
    print(f"  2. Şifre Sıfırlama Sayfası: {urls['Facebook Şifre Sıfırlama']}")
    print(f"\n{Colors.WARNING}[!] İpucu: Şifre sıfırlama sayfasında e-postayı girerek")
    print(f"    hesabın var olup olmadığını kontrol edebilirsiniz.{Colors.RESET}")
    
    return urls

def search_by_phone(phone):
    """Telefon numarası ile Facebook profil ara"""
    print(f"\n{Colors.INFO}[*] Telefon ile Facebook profili aranıyor: {phone}{Colors.RESET}")
    
    urls = {
        'Facebook Arama': f"https://www.facebook.com/search/top/?q={quote(phone)}",
        'Facebook Şifre Sıfırlama': f"https://www.facebook.com/login/identify/?ctx=recover",
    }
    
    print(f"\n{Colors.SUCCESS}[+] Kullanışlı Linkler:{Colors.RESET}")
    print(f"  1. Facebook Arama: {urls['Facebook Arama']}")
    print(f"  2. Şifre Sıfırlama Sayfası: {urls['Facebook Şifre Sıfırlama']}")
    print(f"\n{Colors.WARNING}[!] İpucu: Şifre sıfırlama sayfasında telefon numarasını girerek")
    print(f"    hesabın var olup olmadığını kontrol edebilirsiniz.{Colors.RESET}")
    
    return urls

def facebook_id_lookup(fb_id):
    """Facebook ID'den profil bilgisi al"""
    print(f"\n{Colors.INFO}[*] Facebook ID sorgulanıyor: {fb_id}{Colors.RESET}")
    
    profile_url = f"https://www.facebook.com/profile.php?id={fb_id}"
    
    print(f"\n{Colors.SUCCESS}[+] Profil URL: {profile_url}{Colors.RESET}")
    
    # Ek bilgi linkleri
    additional_urls = {
        'Fotoğraflar': f"https://www.facebook.com/profile.php?id={fb_id}&sk=photos",
        'Arkadaşlar': f"https://www.facebook.com/profile.php?id={fb_id}&sk=friends",
        'Videolar': f"https://www.facebook.com/profile.php?id={fb_id}&sk=videos",
        'Hakkında': f"https://www.facebook.com/profile.php?id={fb_id}&sk=about",
    }
    
    print(f"\n{Colors.INFO}[*] Ek Bilgi Linkleri:{Colors.RESET}")
    for link_type, url in additional_urls.items():
        print(f"  - {link_type}: {url}")
    
    return {'profile_url': profile_url, 'additional_urls': additional_urls}

def facebook_username_lookup(username):
    """Facebook kullanıcı adından profil bilgisi al"""
    print(f"\n{Colors.INFO}[*] Facebook kullanıcı adı sorgulanıyor: {username}{Colors.RESET}")
    
    profile_url = f"https://www.facebook.com/{username}"
    
    print(f"\n{Colors.SUCCESS}[+] Profil URL: {profile_url}{Colors.RESET}")
    
    # Ek bilgi linkleri
    additional_urls = {
        'Fotoğraflar': f"https://www.facebook.com/{username}/photos",
        'Arkadaşlar': f"https://www.facebook.com/{username}/friends",
        'Videolar': f"https://www.facebook.com/{username}/videos",
        'Hakkında': f"https://www.facebook.com/{username}/about",
    }
    
    print(f"\n{Colors.INFO}[*] Ek Bilgi Linkleri:{Colors.RESET}")
    for link_type, url in additional_urls.items():
        print(f"  - {link_type}: {url}")
    
    # Tarayıcıda aç
    choice = input(f"\n{Colors.INPUT}Profili tarayıcıda açmak ister misiniz? (E/H): {Colors.RESET}").strip().upper()
    if choice in ['E', 'Y', 'EVET', 'YES']:
        webbrowser.open(profile_url)
    
    return {'profile_url': profile_url, 'additional_urls': additional_urls}

def advanced_facebook_search():
    """Gelişmiş Facebook arama parametreleri"""
    print(f"\n{Colors.MENU}=== Gelişmiş Facebook Arama ==={Colors.RESET}")
    
    print(f"\n{Colors.INFO}[*] Arama Parametreleri:{Colors.RESET}")
    keyword = input(f"  Anahtar kelime: ").strip()
    location = input(f"  Konum (opsiyonel): ").strip()
    education = input(f"  Eğitim/Okul (opsiyonel): ").strip()
    workplace = input(f"  İşyeri (opsiyonel): ").strip()
    
    # Gelişmiş arama query'si oluştur
    query_parts = [keyword]
    if location:
        query_parts.append(f"location:{location}")
    if education:
        query_parts.append(f"education:{education}")
    if workplace:
        query_parts.append(f"workplace:{workplace}")
    
    query = " ".join(query_parts)
    search_url = f"https://www.facebook.com/search/people/?q={quote(query)}"
    
    print(f"\n{Colors.SUCCESS}[+] Gelişmiş Arama URL: {search_url}{Colors.RESET}")
    
    choice = input(f"\n{Colors.INPUT}Aramayı tarayıcıda başlatmak ister misiniz? (E/H): {Colors.RESET}").strip().upper()
    if choice in ['E', 'Y', 'EVET', 'YES']:
        webbrowser.open(search_url)
    
    return search_url

def facebook_graph_search():
    """Facebook Graph Search örnekleri"""
    print(f"\n{Colors.MENU}=== Facebook Graph Search Örnekleri ==={Colors.RESET}")
    
    examples = {
        '1': ('İstanbul\'da yaşayan kişiler', 'people who live in Istanbul'),
        '2': ('Ankara\'da çalışan kişiler', 'people who work in Ankara'),
        '3': ('Belirli bir şirkette çalışan kişiler', 'people who work at [Şirket Adı]'),
        '4': ('Belirli bir üniversitede okuyan kişiler', 'people who study at [Üniversite Adı]'),
        '5': ('Belirli bir sayfa/grubu beğenen kişiler', 'people who like [Sayfa Adı]'),
        '6': ('Fotoğrafları beğenen kişiler', 'people who like photos'),
        '7': ('Belirli bir tarihte gönderiler', 'posts from [tarih]'),
    }
    
    print(f"\n{Colors.INFO}[*] Graph Search Örnekleri:{Colors.RESET}")
    for key, (description, query) in examples.items():
        print(f"  [{key}] {description}")
        print(f"      Query: {query}")
    
    print(f"\n{Colors.WARNING}[!] Not: Graph Search özelliği Facebook tarafından")
    print(f"    kısıtlanmıştır, ancak bazı sorgular hala çalışabilir.{Colors.RESET}")

def facebook_osint_resources():
    """Facebook OSINT kaynakları"""
    print(f"\n{Colors.MENU}=== Facebook OSINT Kaynakları ==={Colors.RESET}")
    
    resources = {
        'IntelligenceX': 'https://intelx.io/',
        'Sowdust GitHub Tools': 'https://github.com/sowdust/searchcode',
        'Facebook Search Tool': 'https://www.social-searcher.com/facebook-search/',
        'Lookup-ID.com': 'https://lookup-id.com/',
        'Find Facebook ID': 'https://findmyfbid.com/',
    }
    
    print(f"\n{Colors.SUCCESS}[+] Faydalı Araçlar:{Colors.RESET}")
    for tool, url in resources.items():
        print(f"  - {tool}: {url}")

def facebook_search_menu():
    """Facebook arama menüsü"""
    while True:
        clear_screen()
        print_header()
        
        menu = f"""{Colors.MENU}
╔═══════════════════════════════════════════════════════════════╗
║                 FACEBOOK ARAŞTIRMA MENÜSÜ                    ║
╚═══════════════════════════════════════════════════════════════╝

  {Colors.INPUT}[1]{Colors.RESET} 👤 Kişi Adı ile Ara
  {Colors.INPUT}[2]{Colors.RESET} 📧 E-posta ile Ara
  {Colors.INPUT}[3]{Colors.RESET} 📱 Telefon ile Ara
  {Colors.INPUT}[4]{Colors.RESET} 🆔 Facebook ID ile Ara
  {Colors.INPUT}[5]{Colors.RESET} 🔤 Kullanıcı Adı ile Ara
  {Colors.INPUT}[6]{Colors.RESET} 🔍 Gelişmiş Arama
  {Colors.INPUT}[7]{Colors.RESET} 📊 Graph Search Örnekleri
  {Colors.INPUT}[8]{Colors.RESET} 🛠️  OSINT Kaynakları
  {Colors.INPUT}[0]{Colors.RESET} 🔙 Ana Menüye Dön

{Colors.INPUT}Seçiminiz: {Colors.RESET}"""
        
        print(menu, end='')
        choice = input().strip()
        
        if choice == '0':
            break
        elif choice == '1':
            query = input(f"\n{Colors.INPUT}Kişi adı girin: {Colors.RESET}").strip()
            if query:
                result = search_facebook_people(query)
                save_result(f"people_search_{query}", result)
        elif choice == '2':
            email = input(f"\n{Colors.INPUT}E-posta adresi girin: {Colors.RESET}").strip()
            if email:
                result = search_by_email(email)
                save_result(f"email_search_{email}", result)
        elif choice == '3':
            phone = input(f"\n{Colors.INPUT}Telefon numarası girin: {Colors.RESET}").strip()
            if phone:
                result = search_by_phone(phone)
                save_result(f"phone_search_{phone}", result)
        elif choice == '4':
            fb_id = input(f"\n{Colors.INPUT}Facebook ID girin: {Colors.RESET}").strip()
            if fb_id:
                result = facebook_id_lookup(fb_id)
                save_result(f"id_lookup_{fb_id}", result)
        elif choice == '5':
            username = input(f"\n{Colors.INPUT}Kullanıcı adı girin: {Colors.RESET}").strip()
            if username:
                result = facebook_username_lookup(username)
                save_result(f"username_lookup_{username}", result)
        elif choice == '6':
            advanced_facebook_search()
        elif choice == '7':
            facebook_graph_search()
        elif choice == '8':
            facebook_osint_resources()
        else:
            print(f"{Colors.ERROR}[-] Geçersiz seçim!{Colors.RESET}")
        
        input(f"\n{Colors.INPUT}Devam etmek için Enter'a basın...{Colors.RESET}")

def main():
    """Ana fonksiyon"""
    try:
        facebook_search_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}[!] İşlem iptal edildi{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.ERROR}[-] Beklenmeyen hata: {e}{Colors.RESET}")

if __name__ == "__main__":
    main()
