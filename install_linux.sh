#!/bin/bash

# HIG-Osint Linux Kurulum Scripti
# Developer: Halil Gercek
# Email: higeryazilim@gmail.com
# GitHub: https://github.com/Higer23/HIG-Osint

clear

echo -e "\e[1;36m"
cat << "EOF"
╔══════════════════════════════════════════════════════════════╗
║                  HIG-OSINT KURULUM                          ║
║              Linux İçin Genel Kurulum                       ║
╚══════════════════════════════════════════════════════════════╝
EOF
echo -e "\e[0m"

echo -e "\e[1;33m[*] HIG-Osint Linux'a kuruluyor...\e[0m"
echo ""

# Root kontrolü
if [ "$EUID" -ne 0 ]; then 
    echo -e "\e[1;33m[!] Bu script'i root olarak çalıştırmanız önerilir.\e[0m"
    echo -e "\e[1;33m[!] Bazı paketler için sudo gerekebilir.\e[0m"
    echo ""
fi

# Paket yöneticisini tespit et
if command -v apt-get &> /dev/null; then
    PKG_MANAGER="apt-get"
    UPDATE_CMD="sudo apt-get update"
    INSTALL_CMD="sudo apt-get install -y"
elif command -v dnf &> /dev/null; then
    PKG_MANAGER="dnf"
    UPDATE_CMD="sudo dnf check-update"
    INSTALL_CMD="sudo dnf install -y"
elif command -v yum &> /dev/null; then
    PKG_MANAGER="yum"
    UPDATE_CMD="sudo yum check-update"
    INSTALL_CMD="sudo yum install -y"
elif command -v pacman &> /dev/null; then
    PKG_MANAGER="pacman"
    UPDATE_CMD="sudo pacman -Sy"
    INSTALL_CMD="sudo pacman -S --noconfirm"
else
    echo -e "\e[1;31m[!] Desteklenmeyen paket yöneticisi!\e[0m"
    exit 1
fi

echo -e "\e[1;34m[*] Tespit edilen paket yöneticisi: $PKG_MANAGER\e[0m"
echo ""

# Paket güncellemeleri
echo -e "\e[1;34m[1/6] Paket listeleri güncelleniyor...\e[0m"
$UPDATE_CMD

# Temel paketler
echo -e "\e[1;34m[2/6] Temel paketler kuruluyor...\e[0m"
$INSTALL_CMD python3 python3-pip git wget curl

# Python paketleri
echo -e "\e[1;34m[3/6] Python bağımlılıkları kuruluyor...\e[0m"
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt

# OSINT araçları
echo -e "\e[1;34m[4/6] OSINT araçları kuruluyor...\e[0m"
if [ "$PKG_MANAGER" = "apt-get" ]; then
    $INSTALL_CMD nmap whois dnsutils traceroute exiftool
elif [ "$PKG_MANAGER" = "dnf" ] || [ "$PKG_MANAGER" = "yum" ]; then
    $INSTALL_CMD nmap whois bind-utils traceroute perl-Image-ExifTool
elif [ "$PKG_MANAGER" = "pacman" ]; then
    $INSTALL_CMD nmap whois dnsutils traceroute perl-image-exiftool
fi

# İzinler
echo -e "\e[1;34m[5/6] Dosya izinleri ayarlanıyor...\e[0m"
chmod +x higosint.py
find . -name "*.py" -exec chmod +x {} \;
find . -name "*.sh" -exec chmod +x {} \;

# Symlink oluşturma
echo -e "\e[1;34m[6/6] Sistem geneli erişim ayarlanıyor...\e[0m"
INSTALL_DIR=$(pwd)

cat > /tmp/higosint << LAUNCHER
#!/bin/bash
cd $INSTALL_DIR
python3 higosint.py "\$@"
LAUNCHER

sudo mv /tmp/higosint /usr/local/bin/higosint
sudo chmod +x /usr/local/bin/higosint

echo ""
echo -e "\e[1;32m╔══════════════════════════════════════════════════════════════╗\e[0m"
echo -e "\e[1;32m║          ✓ KURULUM BAŞARIYLA TAMAMLANDI!                    ║\e[0m"
echo -e "\e[1;32m╚══════════════════════════════════════════════════════════════╝\e[0m"
echo ""
echo -e "\e[1;36m[*] HIG-Osint'i başlatmak için şu komutları kullanabilirsiniz:\e[0m"
echo -e "\e[1;33m    → python3 higosint.py\e[0m"
echo -e "\e[1;33m    → ./higosint.py\e[0m"
echo -e "\e[1;33m    → higosint\e[0m"
echo ""
echo -e "\e[1;36m[*] Geliştirici: Halil Gercek\e[0m"
echo -e "\e[1;36m[*] Email: higeryazilim@gmail.com\e[0m"
echo -e "\e[1;36m[*] GitHub: https://github.com/Higer23/HIG-Osint\e[0m"
echo ""
