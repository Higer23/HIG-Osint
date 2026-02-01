# HIG-Osint

![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen.svg)
![License](https://img.shields.io/badge/license-GPL--3.0-red.svg)
![Platform](https://img.shields.io/badge/platform-Termux%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)

```
╔═══════════════════════════════════════════════════════════════════════════╗
║  ██╗  ██╗██╗ ██████╗        ██████╗ ███████╗██╗███╗   ██╗████████╗      ║
║  ██║  ██║██║██╔════╝       ██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝      ║
║  ███████║██║██║  ███╗█████╗██║   ██║███████╗██║██╔██╗ ██║   ██║         ║
║  ██╔══██║██║██║   ██║╚════╝██║   ██║╚════██║██║██║╚██╗██║   ██║         ║
║  ██║  ██║██║╚██████╔╝      ╚██████╔╝███████║██║██║ ╚████║   ██║         ║
║  ╚═╝  ╚═╝╚═╝ ╚═════╝        ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝         ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

## 📋 İçindekiler

- [Hakkında](#-hakkında)
- [Özellikler](#-özellikler)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Modüller](#-modüller)
- [Ekran Görüntüleri](#-ekran-görüntüleri)
- [Yasal Uyarı](#-yasal-uyarı)
- [Katkıda Bulunma](#-katkıda-bulunma)
- [Lisans](#-lisans)
- [İletişim](#-iletişim)

## 🎯 Hakkında

**HIG-Osint**, Mr.Holmes ve X-osint araçlarının en iyi özelliklerini birleştiren gelişmiş bir OSINT (Open Source Intelligence) aracıdır. Termux, Linux ve Windows platformlarında sorunsuz çalışacak şekilde özel olarak tasarlanmıştır.

### 👨‍💻 Geliştirici
- **Ad:** Halil Gercek
- **Email:** higeryazilim@gmail.com
- **GitHub:** https://github.com/Higer23/HIG-Osint

### 🔗 Kaynak Projeler
Bu araç aşağıdaki mükemmel projelerin birleştirilmiş ve geliştirilmiş versiyonudur:
- **Mr.Holmes** - Luca Garofalo (Lucksi)
- **X-osint** - TermuxHackz

## ✨ Özellikler

### 🔍 Araştırma Modülleri

#### 👤 Sosyal Medya Araştırması
- **Kullanıcı Adı Araştırma** - 300+ platform
- **Twitter/X Profil Analizi**
- **Instagram Profil Analizi**
- **TikTok Profil Analizi**
- **LinkedIn Profil Analizi**
- **Facebook Profil Analizi**

#### 📧 İletişim Araştırması
- **E-posta Doğrulama ve Analiz**
- **Telefon Numarası Lokasyon Tespiti**
- **Veri İhlali Kontrolü (HIBP)**
- **SMTP ve MX Kaydı Doğrulama**

#### 🌐 Network ve Web
- **IP Adresi Coğrafi Konum**
- **Domain/Website Analizi**
- **Port Tarama**
- **Subdomain Keşfi**
- **Google Dorks**

#### 📸 Medya Analizi
- **Görsel OSINT (EXIF Verisi)**
- **PDF Metadata Analizi**
- **Konum Takibi**

#### 🔐 Güvenlik
- **Hash Çözümleme**
- **Şifre Gücü Kontrolü**
- **Veri İhlali Araştırması**

### 🎨 Kullanıcı Deneyimi
- ✅ Renkli ve kullanıcı dostu arayüz
- ✅ Otomatik bağımlılık yönetimi
- ✅ Detaylı rapor oluşturma
- ✅ Multi-platform desteği (Termux/Linux/Windows)
- ✅ Türkçe dil desteği

## 📥 Kurulum

### Termux İçin Kurulum

```bash
# Depoyu klonlayın
git clone https://github.com/Higer23/HIG-Osint.git
cd HIG-Osint

# Kurulum scriptini çalıştırın
chmod +x install_termux.sh
./install_termux.sh
```

### Linux İçin Kurulum

```bash
# Depoyu klonlayın
git clone https://github.com/Higer23/HIG-Osint.git
cd HIG-Osint

# Kurulum scriptini çalıştırın
chmod +x install_linux.sh
./install_linux.sh
```

### Windows İçin Kurulum

```cmd
# Depoyu klonlayın
git clone https://github.com/Higer23/HIG-Osint.git
cd HIG-Osint

# Kurulum scriptini çalıştırın
install_windows.bat
```

### Manuel Kurulum

```bash
# Python bağımlılıklarını yükleyin
pip install -r requirements.txt --break-system-packages  # Termux için
# veya
pip install -r requirements.txt  # Linux/Windows için

# Programı çalıştırın
python higosint.py
```

## 🚀 Kullanım

### Temel Kullanım

```bash
# Basit başlatma
python higosint.py

# Veya kurulum sonrası
higosint

# Veya doğrudan çalıştırma
./higosint.py
```

### Modül Örnekleri

#### Kullanıcı Adı Araştırma
```bash
HIG-Osint > [01] Kullanıcı Adı Araştırma
Kullanıcı adı: johndoe
# 300+ sitede arama yapılır
```

#### E-posta Analizi
```bash
HIG-Osint > [02] E-posta Araştırma
E-posta: example@gmail.com
# Format, MX, SMTP kontrolü
# Veri ihlali taraması
# Sosyal medya hesap tespiti
```

#### Telefon Numarası
```bash
HIG-Osint > [03] Telefon Numarası Araştırma
Telefon: +905551234567
# Operatör bilgisi
# Lokasyon tespiti
# Online arama linkleri
```

## 📚 Modüller

### Mevcut Modüller

| No | Modül | Açıklama |
|----|-------|----------|
| 01 | Kullanıcı Adı Araştırma | 300+ platformda kullanıcı adı taraması |
| 02 | E-posta Araştırma | E-posta doğrulama ve analiz |
| 03 | Telefon Numarası | Telefon numarası lokasyon ve bilgi |
| 04 | Domain/Website | Web sitesi analizi |
| 05 | Kişi Araştırma | Kişisel bilgi toplama |
| 06 | Twitter/X | Twitter profil analizi |
| 07 | Instagram | Instagram profil analizi |
| 08 | TikTok | TikTok profil analizi |
| 09 | LinkedIn | LinkedIn profil analizi |
| 10 | Facebook | Facebook profil analizi |
| 11 | IP Adresi | IP coğrafi konum ve bilgi |
| 12 | Google Dorks | Gelişmiş Google araması |
| 13 | Konum Takibi | GPS koordinat analizi |
| 14 | Görsel OSINT | EXIF metadata çıkarma |
| 15 | Hash Çözümleme | Hash tanımlama ve kırma |
| 16 | Port Tarama | Network port taraması |
| 17 | Subdomain | Alt domain keşfi |
| 18 | PDF Metadata | PDF dosya analizi |
| 19 | Gelişmiş Araçlar | Ek OSINT araçları |
| 20 | Ayarlar | Konfigürasyon |

## 📸 Ekran Görüntüleri

```
Ana Menü - Renkli ve kullanıcı dostu arayüz
Kullanıcı Adı Araştırma - 300+ platform taraması
E-posta Analizi - Detaylı doğrulama
Telefon Numarası - Lokasyon tespiti
Rapor Oluşturma - Profesyonel çıktılar
```

## ⚠️ Yasal Uyarı

**ÖNEMLİ:** Bu araç yalnızca yasal ve etik OSINT araştırmaları için tasarlanmıştır.

### Kullanım Kuralları
- ✅ Sadece kendinize ait veya izniniz olan bilgileri araştırın
- ✅ Yerel yasalara ve düzenlemelere uygun hareket edin
- ✅ Etik sınırlar içinde kalın
- ❌ İzinsiz veri toplama, takip veya istihbarat faaliyeti YASAKTIR
- ❌ Kişisel verilerin gizliliğine saygı gösterin

**Geliştirici Sorumluluk Reddi:** Bu aracın kötüye kullanımından kaynaklanan tüm yasal sorumluluk kullanıcıya aittir. Geliştirici (Halil Gercek), aracın yasadışı veya etik olmayan kullanımından sorumlu değildir.

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen şu adımları izleyin:

1. Bu depoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/YeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -m 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/YeniOzellik`)
5. Pull Request oluşturun

### Katkıda Bulunma Kuralları
- Kod standartlarına uyun
- Değişikliklerinizi test edin
- Dokümantasyon ekleyin
- Türkçe ve İngilizce açıklama yapın

## 📜 Lisans

Bu proje GNU General Public License v3.0 altında lisanslanmıştır.

### Kaynak Proje Lisansları
- **Mr.Holmes:** GNU GPL v3.0
- **X-osint:** GPL v3.0

Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 📞 İletişim

### Geliştirici: Halil Gercek

- 📧 **Email:** higeryazilim@gmail.com
- 🐙 **GitHub:** https://github.com/Higer23
- 🌐 **Proje:** https://github.com/Higer23/HIG-Osint

### Destek ve Geri Bildirim

- 🐛 **Bug Raporu:** [Issues](https://github.com/Higer23/HIG-Osint/issues)
- 💡 **Özellik İsteği:** [Issues](https://github.com/Higer23/HIG-Osint/issues)
- 💬 **Tartışma:** [Discussions](https://github.com/Higer23/HIG-Osint/discussions)

## 🙏 Teşekkürler

Bu projeyi mümkün kılan kaynak proje geliştiricilerine teşekkürler:
- **Luca Garofalo (Lucksi)** - Mr.Holmes
- **TermuxHackz** - X-osint

## 📊 Durum

![GitHub stars](https://img.shields.io/github/stars/Higer23/HIG-Osint?style=social)
![GitHub forks](https://img.shields.io/github/forks/Higer23/HIG-Osint?style=social)
![GitHub issues](https://img.shields.io/github/issues/Higer23/HIG-Osint)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Higer23/HIG-Osint)

---

**⭐ Projeyi beğendiyseniz yıldız vermeyi unutmayın!**

**Made with ❤️ by Halil Gercek**
