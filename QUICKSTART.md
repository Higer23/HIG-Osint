# HIG-Osint Hızlı Başlangıç Kılavuzu

## 🚀 Hızlı Kurulum ve Kullanım

### 1️⃣ Termux'ta Kurulum (En Hızlı)

```bash
# Gerekli paketleri yükle
pkg update && pkg upgrade -y
pkg install python git -y

# HIG-Osint'i indir
git clone https://github.com/Higer23/HIG-Osint.git
cd HIG-Osint

# Otomatik kurulum
chmod +x install_termux.sh
./install_termux.sh

# Başlat
higosint
```

### 2️⃣ Linux'ta Kurulum

```bash
# Gerekli paketleri yükle
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip git -y

# HIG-Osint'i indir
git clone https://github.com/Higer23/HIG-Osint.git
cd HIG-Osint

# Otomatik kurulum
chmod +x install_linux.sh
./install_linux.sh

# Başlat
higosint
```

### 3️⃣ Windows'ta Kurulum

```cmd
# Python'un kurulu olduğundan emin olun: https://python.org

# HIG-Osint'i indir
git clone https://github.com/Higer23/HIG-Osint.git
cd HIG-Osint

# Otomatik kurulum
install_windows.bat

# Başlat
python higosint.py
```

## 📖 İlk Kullanım

### Ana Menü
Program başlatıldığında ana menü görüntülenir:
```
[01] Kullanıcı Adı Araştırma
[02] E-posta Araştırma
[03] Telefon Numarası Araştırma
...
[00] Çıkış
```

### Örnek: Kullanıcı Adı Araştırma

1. Ana menüden `01` seçin
2. Kullanıcı adını girin: `johndoe`
3. Program 300+ platformda arama yapar
4. Sonuçları gösterir
5. Rapor kaydetmek isterseniz `E` basın

### Örnek: E-posta Araştırma

1. Ana menüden `02` seçin
2. E-posta adresini girin: `example@gmail.com`
3. Program şunları kontrol eder:
   - Format geçerliliği
   - MX kaydı
   - SMTP sunucu
   - Veri ihlalleri
   - Sosyal medya hesapları
4. Detaylı rapor oluşturulur

### Örnek: Telefon Numarası

1. Ana menüden `03` seçin
2. Numarayı uluslararası formatta girin: `+905551234567`
3. Program şunları gösterir:
   - Ülke ve bölge
   - Operatör bilgisi
   - Numara türü
   - Zaman dilimi
   - Online arama linkleri

## 🔧 Sorun Giderme

### Python Bulunamadı
```bash
# Termux
pkg install python

# Linux
sudo apt install python3

# Windows
# https://python.org adresinden indirin
```

### Modül Bulunamadı Hatası
```bash
# Bağımlılıkları yeniden yükle
pip install -r requirements.txt --break-system-packages  # Termux
pip install -r requirements.txt  # Linux/Windows
```

### İzin Hatası
```bash
# Dosyaları çalıştırılabilir yap
chmod +x higosint.py
chmod +x install_*.sh
```

## 💡 İpuçları

### En İyi Sonuçlar İçin
- Telefon numaralarını `+` ile başlayacak şekilde girin
- E-posta adreslerini tam formatta girin
- Kullanıcı adlarını @ işareti olmadan girin
- Raporları kaydetmeyi unutmayın

### Performans
- İnternet bağlantınızın hızlı olduğundan emin olun
- Birden fazla aramayı sırayla yapın
- Sonuçları incelemek için zaman ayırın

### Gizlilik
- VPN kullanmayı düşünün
- Proxy ayarlarını yapılandırın
- Yasal sınırlar içinde kalın

## 📞 Destek

Sorun yaşıyorsanız:
1. README.md dosyasını okuyun
2. Issues bölümünü kontrol edin
3. Yeni issue açın
4. higeryazilim@gmail.com adresine mail atın

## 🎓 Eğitim Kaynakları

- OSINT Framework: https://osintframework.com
- OSINT Techniques: https://www.osinttechniques.com
- Bellingcat: https://www.bellingcat.com

---

**Başarılı OSINT araştırmaları! 🎯**

Halil Gercek
higeryazilim@gmail.com
https://github.com/Higer23/HIG-Osint
