cat > /home/claude/hig_modules/linkedin_search.py << 'EOFLINKEDIN'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
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
║            💼 LINKEDIN ARAŞTIRMA MODÜLÜ 💼                   ║
╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}""")

def main():
    os.system('clear' if os.name != 'nt' else 'cls')
    print_header()
    
    name = input(f"{Colors.INPUT}İsim Soyisim: {Colors.RESET}").strip()
    if not name:
        print(f"{Colors.ERROR}[!] Boş olamaz!{Colors.RESET}")
        return
    
    links = {
        "LinkedIn Arama": f"https://www.linkedin.com/search/results/people/?keywords={name}",
        "Google Site Search": f"https://www.google.com/search?q=site:linkedin.com+{name}",
        "LinkedIn Sales": f"https://www.linkedin.com/sales/search/people?keywords={name}",
        "LinkedIn Premium": f"https://www.linkedin.com/search/results/all/?keywords={name}",
    }
    
    print(f"\n{Colors.INFO}[*] LinkedIn araştırması...{Colors.RESET}\n")
    for site, url in links.items():
        print(f"{Colors.SUCCESS}→ {site:20} : {url}{Colors.RESET}")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = BASE_DIR / 'reports' / 'linkedin_search'
    report_dir.mkdir(parents=True, exist_ok=True)
    
    if input(f"\n{Colors.INPUT}Kaydet? (E/H): {Colors.RESET}").strip().upper() in ['E', 'Y', 'EVET', 'YES']:
        report_file = report_dir / f"{name.replace(' ', '_')}_{timestamp}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"LinkedIn Araştırma - {name}\n" + "="*65 + "\n")
            for site, url in links.items():
                f.write(f"{site}: {url}\n")
        print(f"{Colors.SUCCESS}✓ {report_file}{Colors.RESET}")
    
    input(f"\n{Colors.INPUT}Enter...{Colors.RESET}")

if __name__ == "__main__":
    main()
EOFLINKEDIN

cat > /home/claude/hig_modules/facebook_search.py << 'EOFFACEBOOK'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
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
║            📘 FACEBOOK ARAŞTIRMA MODÜLÜ 📘                   ║
╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}""")

def main():
    os.system('clear' if os.name != 'nt' else 'cls')
    print_header()
    
    query = input(f"{Colors.INPUT}İsim veya kullanıcı adı: {Colors.RESET}").strip()
    if not query:
        print(f"{Colors.ERROR}[!] Boş olamaz!{Colors.RESET}")
        return
    
    links = {
        "Kişi Arama": f"https://www.facebook.com/search/people/?q={query}",
        "Sayfa Arama": f"https://www.facebook.com/search/pages/?q={query}",
        "Grup Arama": f"https://www.facebook.com/search/groups/?q={query}",
        "Google": f"https://www.google.com/search?q=site:facebook.com+{query}",
        "Yandex": f"https://yandex.com/search/?text=site:facebook.com+{query}",
    }
    
    print(f"\n{Colors.INFO}[*] Facebook araştırması...{Colors.RESET}\n")
    for site, url in links.items():
        print(f"{Colors.SUCCESS}→ {site:20} : {url}{Colors.RESET}")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = BASE_DIR / 'reports' / 'facebook_search'
    report_dir.mkdir(parents=True, exist_ok=True)
    
    if input(f"\n{Colors.INPUT}Kaydet? (E/H): {Colors.RESET}").strip().upper() in ['E', 'Y', 'EVET', 'YES']:
        report_file = report_dir / f"{query.replace(' ', '_')}_{timestamp}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"Facebook Araştırma - {query}\n" + "="*65 + "\n")
            for site, url in links.items():
                f.write(f"{site}: {url}\n")
        print(f"{Colors.SUCCESS}✓ {report_file}{Colors.RESET}")
    
    input(f"\n{Colors.INPUT}Enter...{Colors.RESET}")

if __name__ == "__main__":
    main()
EOFFACEBOOK

echo "LinkedIn ve Facebook modülleri oluşturuldu"
