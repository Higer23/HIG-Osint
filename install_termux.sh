#!/data/data/com.termux/files/usr/bin/bash

# HIG-Osint Termux Kurulum Scripti
# Developer: Halil Gercek
# Email: higeryazilim@gmail.com
# GitHub: https://github.com/Higer23/HIG-Osint

clear

echo -e "\e[1;36m"
cat << "EOF"
╔══════════════════════════════════════════════════════════════╗
║                  HIG-OSINT KURULUM                          ║
║              Termux İçin Özel Kurulum                       ║
╚══════════════════════════════════════════════════════════════╝
EOF
echo -e "\e[0m"

echo -e "\e[1;33m[*] HIG-Osint Termux'a kuruluyor...\e[0m"
echo ""

# Paket güncellemeleri
echo -e "\e[1;34m[1/7] Paket listeleri güncelleniyor...\e[0m"
pkg update -y

echo -e "\e[1;34m[2/7] Paketler yükseltiliyor...\e[0m"
pkg upgrade -y

# Temel paketler
echo -e "\e[1;34m[3/7] Temel paketler kuruluyor...\e[0m"
pkg install -y python python-pip git wget curl openssl libxml2 libxslt

# Python paketleri
echo -e "\e[1;34m[4/7] Python bağımlılıkları kuruluyor...\e[0m"
pip install --upgrade pip --break-system-packages
pip install -r requirements.txt --break-system-packages

# Ek araçlar
echo -e "\e[1;34m[5/7] OSINT araçları kuruluyor...\e[0m"
pkg install -y nmap whois dnsutils traceroute

# ExifTool
echo -e "\e[1;34m[6/7] ExifTool kuruluyor...\e[0m"
pkg install -y exiftool

# Launcher oluşturma
echo -e "\e[1;34m[7/7] Launcher oluşturuluyor...\e[0m"

cat > $PREFIX/bin/higosint << 'LAUNCHER'
#!/data/data/com.termux/files/usr/bin/bash
cd ~/HIG-Osint
python higosint.py "$@"
LAUNCHER

chmod +x $PREFIX/bin/higosint

# İzinler
chmod +x higosint.py
find . -name "*.py" -exec chmod +x {} \;

echo ""
echo -e "\e[1;32m╔══════════════════════════════════════════════════════════════╗\e[0m"
echo -e "\e[1;32m║          ✓ KURULUM BAŞARIYLA TAMAMLANDI!                    ║\e[0m"
echo -e "\e[1;32m╚══════════════════════════════════════════════════════════════╝\e[0m"
echo ""
echo -e "\e[1;36m[*] HIG-Osint'i başlatmak için şu komutları kullanabilirsiniz:\e[0m"
echo -e "\e[1;33m    → python higosint.py\e[0m"
echo -e "\e[1;33m    → ./higosint.py\e[0m"
echo -e "\e[1;33m    → higosint\e[0m"
echo ""
echo -e "\e[1;36m[*] Geliştirici: Halil Gercek\e[0m"
echo -e "\e[1;36m[*] Email: higeryazilim@gmail.com\e[0m"
echo -e "\e[1;36m[*] GitHub: https://github.com/Higer23/HIG-Osint\e[0m"
echo ""
