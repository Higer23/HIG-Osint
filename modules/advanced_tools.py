#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ARES-V5 Advanced Intelligence Framework
======================================
Modüler, asenkron OSINT ve hedef profilleme aracı.
asyncio + aiohttp + Playwright tabanlı yüksek performanslı veri toplama sistemi.

Platform: Termux (Android) & Windows CMD uyumlu
Standards: PEP8 compliant, full docstring coverage
"""

import asyncio
import aiohttp
import sys
import os
import re
import json
from datetime import datetime
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
import platform
import subprocess
import shutil

# Platform-specific imports
if os.name == 'nt' or platform.system() == 'Windows':
    try:
        from colorama import Fore, Style, init
        init(autoreset=True)
    except ImportError:
        Fore = Style = lambda x: ''
else:
    # Termux/Android colors
    class Colors:
        HEADER = '\033[96m\033[1m'
        INFO = '\033[94m\033[1m'
        SUCCESS = '\033[92m\033[1m'
        WARNING = '\033[93m\033[1m'
        ERROR = '\033[91m\033[1m'
        RESET = '\033[0m'

    Fore = Colors()

# Web scraping & browser automation
try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

# Template engine
try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape
    JINJA_AVAILABLE = True
except ImportError:
    JINJA_AVAILABLE = False

# Image processing
try:
    from PIL import Image
    from PIL.ExifTags import TAGS
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


@dataclass
class TargetProfile:
    """Hedef profili veri yapısı - OSINT operasyonları için standartlaştırılmış girdi."""
    name: str = ""
    surname: str = ""
    alias: str = ""
    education: str = ""
    address: str = ""
    hobbies: str = ""
    birth_date: str = ""
    emails: List[str] = None
    phones: List[str] = None
    social_profiles: Dict[str, str] = None
    websites: List[str] = None

    def __post_init__(self):
        if self.emails is None:
            self.emails = []
        if self.phones is None:
            self.phones = []
        if self.social_profiles is None:
            self.social_profiles = {}
        if self.websites is None:
            self.websites = []


class Colors:
    """Platform-agnostik renk tanımlamaları."""
    HEADER = Fore.CYAN + Style.BRIGHT if 'Fore' in locals() else ''
    INFO = Fore.BLUE + Style.BRIGHT if 'Fore' in locals() else ''
    SUCCESS = Fore.GREEN + Style.BRIGHT if 'Fore' in locals() else ''
    WARNING = Fore.YELLOW + Style.BRIGHT if 'Fore' in locals() else ''
    ERROR = Fore.RED + Style.BRIGHT if 'Fore' in locals() else ''
    RESET = Style.RESET_ALL if 'Style' in locals() else ''


class AresCore:
    """ARES-V5 Ana Çekirdek - Asenkron OSINT motoru."""
    
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.profile = TargetProfile()
        self.results: Dict[str, Any] = {
            'metadata': {
                'start_time': datetime.now().isoformat(),
                'platform': sys.platform,
                'target': {}
            },
            'emails': [],
            'phones': [],
            'social_profiles': {},
            'images': [],
            'websites': [],
            'breaches': [],
            'shodan': [],
            'archives': []
        }
        self.semaphore = asyncio.Semaphore(50)  # Rate limiting
        self.base_dir = Path("ares_reports")
        self.base_dir.mkdir(exist_ok=True)

    async def __aenter__(self):
        """Async context manager - HTTP session başlat."""
        connector = aiohttp.TCPConnector(
            limit=100,
            limit_per_host=30,
            ttl_dns_cache=300,
            use_dns_cache=True,
        )
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers=headers
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Session cleanup."""
        if self.session:
            await self.session.close()

    def print_banner(self):
        """ARES-V5 bannerını göster."""
        banner = f"""
{Colors.HEADER}
╔══════════════════════════════════════════════════════════════════════╗
║  ██████╗██╗  ██╗██████╗  ██████╗██╗  ██╗    ██╗  ██╗███████╗██████╗  ║
║  ██╔══██╗██║ ██╔╝██╔══██╗██╔═══██╗██║ ██╔╝    ██║  ██║██╔════╝██╔══██╗ ║
║  ██████╔╝█████╔╝ ██████╔╝██║   ██║█████╔╝     ███████║█████╗  ██████╔╝ ║
║  ██╔══██╗██╔═██╗ ██╔══██╗██║   ██║██╔═██╗     ██╔══██║██╔══╝  ██╔══██╗ ║
║  ██║  ██║██║  ██║██║  ██║╚██████╔╝██║  ██║    ██║  ██║███████╗██║  ██║ ║
║  ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ║
║                           Advanced Intelligence Framework v5.0        ║
╚══════════════════════════════════════════════════════════════════════╝
{Colors.RESET}
        """
        print(banner)


class DynamicInputSystem:
    """Dinamik CLI girdi sistemi - TargetProfile oluşturur."""
    
    @staticmethod
    def get_input(prompt: str, default: str = "") -> str:
        """Güvenli CLI input - skip desteği ile."""
        display_prompt = f"{Colors.INFO}[*] {prompt} (skip için Enter): {Colors.RESET}"
        value = input(display_prompt).strip()
        return value if value else default

    @classmethod
    async def collect_profile(cls) -> TargetProfile:
        """Kullanıcıdan tam TargetProfile toplar."""
        print(f"\n{Colors.HEADER}=== HEDEF PROFİLİ OLUŞTURMA ==={Colors.RESET}")
        
        profile = TargetProfile(
            name=cls.get_input("Ad"),
            surname=cls.get_input("Soyad"),
            alias=cls.get_input("Takma ad / Username"),
            education=cls.get_input("Eğitim bilgileri"),
            address=cls.get_input("Adres"),
            hobbies=cls.get_input("Hobiler / İlgi alanları"),
            birth_date=cls.get_input("Doğum tarihi (GG/AA/YYYY)")
        )
        
        print(f"\n{Colors.SUCCESS}[+] Profil kaydedildi: {profile.name} {profile.surname}{Colors.RESET}")
        return profile


class DeepWebArchiveScraper:
    """Deep Web & Archive scraper - Wayback + Paste sites."""
    
    EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    PHONE_REGEX = re.compile(r'[\+]?[0-9\s\-\(\)]{10,}')
    
    WAYBACK_CDXML = "http://archive.org/wayback/available?url={}"
    PASTE_SITES = [
        "pastebin.com/raw/", "paste2.org/raw/", "controlc.com/raw/",
        "pastes.io/raw/", "0paste.com/", "textbin.net/raw/"
    ]
    
    async def scrape_archives(self, session: aiohttp.ClientSession, 
                            keywords: List[str], semaphore: asyncio.Semaphore) -> List[Dict]:
        """Wayback Machine ve paste sitelerini tara."""
        results = []
        
        async with semaphore:
            # Wayback Machine
            for keyword in keywords[:5]:  # Rate limit
                try:
                    url = self.WAYBACK_CDXML.format(keyword)
                    async with session.get(url) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            if 'archived_snapshots' in data.get('archived_snapshots', {}):
                                snapshots = data['archived_snapshots']['closest']
                                results.append({
                                    'source': 'wayback',
                                    'url': snapshots['url'],
                                    'timestamp': snapshots['timestamp'],
                                    'status': snapshots['status']
                                })
                except:
                    continue
        
        # Paste sites (simplified)
        for paste_prefix in self.PASTE_SITES[:3]:
            for keyword in keywords[:3]:
                paste_id = keyword.split('.')[-2] if '.' in keyword else keyword[:8]
                paste_url = f"{paste_prefix}{paste_id}"
                try:
                    async with session.get(paste_url, timeout=5) as resp:
                        if resp.status == 200:
                            content = await resp.text()
                            emails = self.EMAIL_REGEX.findall(content)
                            if emails:
                                results.append({
                                    'source': 'paste',
                                    'url': paste_url,
                                    'found_emails': emails[:5]
                                })
                except:
                    continue
        
        return results


class VisualMediaExtractor:
    """Görsel & medya çıkarıcı - EXIF + metadata analizi."""
    
    async def extract_images(self, session: aiohttp.ClientSession, 
                           urls: List[str], semaphore: asyncio.Semaphore) -> List[Dict]:
        """Tüm img tag'lerini ve metadata'yı çıkar."""
        images = []
        
        for url in urls[:50]:  # Limit
            async with semaphore:
                try:
                    # Playwright ile dynamic content
                    if PLAYWRIGHT_AVAILABLE:
                        images.extend(await self._playwright_image_scrape(session, url))
                    else:
                        # Static scraping fallback
                        images.extend(await self._static_image_scrape(session, url))
                except:
                    continue
        
        return images
    
    async def _playwright_image_scrape(self, session: aiohttp.ClientSession, target_url: str):
        """Headless browser ile img extraction."""
        images = []
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            await page.goto(target_url, wait_until="networkidle")
            img_elements = await page.query_selector_all("img")
            
            for img in img_elements[:20]:
                src = await img.get_attribute("src")
                alt = await img.get_attribute("alt")
                if src:
                    images.append({
                        'url': src,
                        'alt': alt or '',
                        'filename': src.split('/')[-1],
                        'target_context': target_url
                    })
            
            await browser.close()
        return images
    
    async def _static_image_scrape(self, session: aiohttp.ClientSession, target_url: str):
        """Fallback static scraping."""
        try:
            async with session.get(target_url) as resp:
                html = await resp.text()
                img_matches = re.findall(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', html)
                alt_matches = re.findall(r'<img[^>]+alt=["\']([^"\']+)["\'][^>]*>', html)
                
                images = []
                for i, src in enumerate(img_matches[:20]):
                    images.append({
                        'url': src,
                        'alt': alt_matches[i] if i < len(alt_matches) else '',
                        'filename': src.split('/')[-1],
                        'target_context': target_url
                    })
                return images
        except:
            return []


class APIIntegrationLayer:
    """Asenkron API katmanı - Shodan, Hunter, HIBP."""
    
    def __init__(self, api_keys: Dict[str, str]):
        self.api_keys = api_keys
        self.shodan_key = api_keys.get('shodan')
        self.hunter_key = api_keys.get('hunter')
        self.hibp_key = api_keys.get('hibp')

    async def shodan_search(self, session: aiohttp.ClientSession, 
                          query: str, semaphore: asyncio.Semaphore) -> List[Dict]:
        """Shodan IP/Banner search - pasif mod desteği."""
        if not self.shodan_key:
            print(f"{Colors.WARNING}[!] Shodan API key yok, pasif mod{Colors.RESET}")
            return []
        
        async with semaphore:
            try:
                url = f"https://api.shodan.io/shodan/host/search?key={self.shodan_key}&query={query}"
                async with session.get(url) as resp:
                    data = await resp.json()
                    return data.get('matches', [])
            except:
                return []

    async def hunter_email_search(self, session: aiohttp.ClientSession, 
                                domain: str, semaphore: asyncio.Semaphore) -> List[str]:
        """Hunter.io email pattern search."""
        if not self.hunter_key:
            return []
        
        async with semaphore:
            try:
                url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={self.hunter_key}"
                async with session.get(url) as resp:
                    data = await resp.json()
                    return [e['value'] for e in data.get('data', {}).get('emails', [])]
            except:
                return []

    async def hibp_breach_check(self, session: aiohttp.ClientSession, 
                              email: str, semaphore: asyncio.Semaphore) -> List[Dict]:
        """Have I Been Pwned breach analysis."""
        if not self.hibp_key:
            return []
        
        async with semaphore:
            try:
                url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}?truncateResponse=false"
                headers = {'User-Agent': 'ARES-V5', 'hibp-api-key': self.hibp_key}
                async with session.get(url, headers=headers) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    return []
            except:
                return []


class IntelligenceDossier:
    """Jinja2 + Bootstrap5 raporlama motoru."""
    
    def __init__(self, results: Dict, profile: TargetProfile):
        self.results = results
        self.profile = profile
        self.template_dir = Path(__file__).parent / "templates"
        
        if JINJA_AVAILABLE:
            self.env = Environment(
                loader=FileSystemLoader(self.template_dir),
                autoescape=select_autoescape(['html', 'xml'])
            )

    def generate_html_report(self, output_path: str):
        """Zengin HTML5 Intelligence Dossier üret."""
        if not JINJA_AVAILABLE:
            print(f"{Colors.ERROR}[-] Jinja2 yok, JSON report fallback{Colors.RESET}")
            self._save_json_report(output_path)
            return
        
        try:
            # Create template directory if missing
            self.template_dir.mkdir(exist_ok=True)
            
            # Main template
            template_content = self._create_bootstrap_template()
            template = self.env.from_string(template_content)
            
            html_content = template.render(
                profile=self.profile,
                results=self.results,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"{Colors.SUCCESS}[+] Dossier hazır: {output_path}{Colors.RESET}")
            
        except Exception as e:
            print(f"{Colors.ERROR}[-] Report hatası: {e}{Colors.RESET}")

    def _create_bootstrap_template(self) -> str:
        """Bootstrap 5 template string."""
        return """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ profile.name }} {{ profile.surname }} - Intelligence Dossier</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-dark text-light">
    <div class="container-fluid py-4">
        <div class="row">
            <div class="col-12">
                <h1 class="text-center mb-5">
                    <i class="fas fa-eye text-danger me-3"></i>
                    ARES-V5 Intelligence Dossier
                </h1>
                
                <!-- Target Profile -->
                <div class="card bg-primary mb-4">
                    <div class="card-header">
                        <h3><i class="fas fa-user me-2"></i>Hedef Profili</h3>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6">
                                <p><strong>Ad Soyad:</strong> {{ profile.name }} {{ profile.surname }}</p>
                                <p><strong>Alias:</strong> {{ profile.alias }}</p>
                                <p><strong>Eğitim:</strong> {{ profile.education }}</p>
                            </div>
                            <div class="col-md-6">
                                <p><strong>Adres:</strong> {{ profile.address }}</p>
                                <p><strong>Hobiler:</strong> {{ profile.hobbies }}</p>
                                <p><strong>Doğum Tarihi:</strong> {{ profile.birth_date }}</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Key Findings -->
                {% if results.emails %}
                <div class="card bg-success mb-4">
                    <div class="card-header">
                        <h4><i class="fas fa-envelope me-2"></i>Emails ({{ results.emails|length }})</h4>
                    </div>
                    <div class="card-body">
                        <ul class="list-group list-group-flush">
                        {% for email in results.emails %}
                            <li class="list-group-item bg-dark text-light">{{ email }}</li>
                        {% endfor %}
                        </ul>
                    </div>
                </div>
                {% endif %}

                <!-- Images -->
                {% if results.images %}
                <div class="card bg-info mb-4">
                    <div class="card-header">
                        <h4><i class="fas fa-images me-2"></i>İlişkili Görseller ({{ results.images|length }})</h4>
                    </div>
                    <div class="card-body">
                        <div class="row">
                        {% for img in results.images[:12] %}
                            <div class="col-md-3 mb-3">
                                <div class="card bg-dark">
                                    <img src="{{ img.url }}" class="card-img-top" style="height: 150px; object-fit: cover;">
                                    <div class="card-body p-2">
                                        <small>{{ img.filename[:30] }}</small>
                                    </div>
                                </div>
                            </div>
                        {% endfor %}
                        </div>
                    </div>
                </div>
                {% endif %}

                <!-- Archives & Deep Web -->
                {% if results.archives %}
                <div class="card bg-warning mb-4">
                    <div class="card-header">
                        <h4><i class="fas fa-archive me-2"></i>Arşiv & Deep Web ({{ results.archives|length }})</h4>
                    </div>
                    <div class="card-body">
                        <ul class="list-group list-group-flush">
                        {% for archive in results.archives %}
                            <li class="list-group-item bg-dark text-light">
                                <a href="{{ archive.url }}" class="text-light" target="_blank">{{ archive.url[:60] }}</a>
                                {% if archive.found_emails %}
                                    <span class="badge bg-danger ms-2">{{ archive.found_emails|length }} email</span>
                                {% endif %}
                            </li>
                        {% endfor %}
                        </ul>
                    </div>
                </div>
                {% endif %}

                <!-- Metadata -->
                <div class="card bg-secondary">
                    <div class="card-header">
                        <h5>Operasyon Metadata</h5>
                    </div>
                    <div class="card-body">
                        <p><strong>Tarih:</strong> {{ timestamp }}</p>
                        <p><strong>Platform:</strong> {{ results.metadata.platform }}</p>
                        <p><strong>Toplam Bulgu:</strong> {{ results.emails|length + results.images|length + results.archives|length }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
        """

    def _save_json_report(self, output_path: str):
        """Fallback JSON report."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = output_path.replace('.html', f'_{timestamp}.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({
                'profile': asdict(self.profile),
                'results': self.results,
                'generated': datetime.now().isoformat()
            }, f, indent=2, ensure_ascii=False)
        print(f"{Colors.SUCCESS}[+] JSON report: {json_path}{Colors.RESET}")


async def platform_setup():
    """Platform-specific dependency check & setup."""
    print(f"{Colors.INFO}[*] Platform tespit: {sys.platform} / {os.name}{Colors.RESET}")
    
    if sys.platform.startswith('linux') and shutil.which('termux-setup-storage'):
        # Termux setup
        print(f"{Colors.INFO}[*] Termux detected - dependencies check...{Colors.RESET}")
        required = ['python', 'pip']
        missing = []
        for pkg in required:
            if not shutil.which(pkg):
                missing.append(pkg)
        
        if missing:
            print(f"{Colors.WARNING}[!] Eksik: {', '.join(missing)} - termux-setup-storage && pkg install python{Colors.RESET}")
    
    elif os.name == 'nt':
        print(f"{Colors.INFO}[*] Windows CMD detected - colorama active{Colors.RESET}")


async def main_operation():
    """Ana OSINT operasyonu."""
    await platform_setup()
    
    async with AresCore() as ares:
        ares.print_banner()
        
        # 1. Profil toplama
        ares.profile = await DynamicInputSystem.collect_profile()
        ares.results['metadata']['target'] = asdict(ares.profile)
        
        # 2. API key kontrolü (opsiyonel)
        api_keys = {}
        print(f"\n{Colors.INFO}[*] API anahtarları (opsiyonel):{Colors.RESET}")
        for key in ['shodan', 'hunter', 'hibp']:
            value = input(f"  {key.upper()} key (boş geç): ").strip()
            if value:
                api_keys[key] = value
        
        apis = APIIntegrationLayer(api_keys)
        
        # 3. Ana tarama
        print(f"\n{Colors.HEADER}=== ASENKRON OSINT TARAMASI BAŞLATILIYOR ==={Colors.RESET}")
        
        # Archive scraping
        keywords = [f"{ares.profile.name}.{ares.profile.surname}", 
                   ares.profile.name.lower(), ares.profile.alias]
        ares.results['archives'] = await DeepWebArchiveScraper().scrape_archives(
            ares.session, keywords, ares.semaphore
        )
        
        # Social & websites (örnek)
        sample_sites = [
            f"https://twitter.com/{ares.profile.alias}",
            f"https://github.com/{ares.profile.alias}",
            f"https://linkedin.com/in/{ares.profile.name}-{ares.profile.surname}"
        ]
        
        # Image extraction
        ares.results['images'] = await VisualMediaExtractor().extract_images(
            ares.session, sample_sites, ares.semaphore
        )
        
        # API searches
        if ares.profile.name and ares.profile.surname:
            domain = f"{ares.profile.name.lower()}.{ares.profile.surname.lower()[:3]}".replace(' ', '')
            ares.results['emails'].extend(await apis.hunter_email_search(ares.session, domain, ares.semaphore))
        
        # 4. Raporlama
        dossier = IntelligenceDossier(ares.results, ares.profile)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = ares.base_dir / f"ARES_Dossier_{ares.profile.name}_{timestamp}.html"
        
        dossier.generate_html_report(str(report_path))
        
        # JSON backup
        json_path = report_path.with_suffix('.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(ares.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n{Colors.SUCCESS}=== OPERASYON TAMAMLANDI ==={Colors.RESET}")
        print(f"📁 Reports: {ares.base_dir}")
        print(f"📊 HTML: {report_path}")
        print(f"💾 JSON: {json_path}")


def print_requirements():
    """Gerekli kütüphaneler."""
    reqs = """
🛠️  GEREKLİ KÜTÜPHANELER (pip install):
    aiohttp asyncio playwright jinja2 colorama pillow python-whois dnspython

Termux için:
$ pkg install python chromium
$ playwright install chromium

Windows için:
pip install -r requirements.txt
    """
    print(reqs)


async def main():
    """Ana giriş noktası."""
    try:
        print(f"{Colors.HEADER}ARES-V5 başlatılıyor...{Colors.RESET}")
        print_requirements()
        
        while True:
            choice = input(f"\n{Colors.INPUT}[S]tart / [R]equirements / [Q]uit: {Colors.RESET}").strip().lower()
            
            if choice == 's':
                await main_operation()
            elif choice == 'r':
                print_requirements()
            elif choice == 'q':
                print(f"{Colors.SUCCESS}ARES-V5 sonlandırılıyor...{Colors.RESET}")
                break
            else:
                print(f"{Colors.ERROR}Geçersiz seçim!{Colors.RESET}")
                
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Operasyon iptal edildi.{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.ERROR}Hata: {e}{Colors.RESET}")


if __name__ == "__main__":
    if sys.platform == "win32":
        sys.argv = [sys.argv[0]]  # Colorama fix
    
    asyncio.run(main())
