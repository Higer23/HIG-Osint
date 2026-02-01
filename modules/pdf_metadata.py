#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PDF Metadata Module - PDF Metadata Analiz Modülü
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from colorama import Fore, Style

try:
    import PyPDF2
except ImportError:
    print("[!] PyPDF2 modülü bulunamadı. Yükleniyor...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF2", "--break-system-packages"])
    import PyPDF2

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
║                  PDF METADATA ANALİZ MODÜLÜ                      ║
║                  PDF Metadata Analysis Module                    ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(header)

def save_result(filename, data):
    """Sonuçları kaydet"""
    try:
        reports_dir = Path('reports')
        reports_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = reports_dir / f"pdf_metadata_{filename}_{timestamp}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"{Colors.SUCCESS}[+] Sonuçlar kaydedildi: {filepath}{Colors.RESET}")
        return True
    except Exception as e:
        print(f"{Colors.ERROR}[-] Kayıt hatası: {e}{Colors.RESET}")
        return False

def extract_pdf_metadata(pdf_path):
    """PDF metadata'sını çıkart"""
    print(f"\n{Colors.INFO}[*] PDF metadata'sı çıkartılıyor: {pdf_path}{Colors.RESET}")
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Temel bilgiler
            result = {
                'filename': os.path.basename(pdf_path),
                'num_pages': len(pdf_reader.pages),
                'metadata': {},
                'file_info': {}
            }
            
            # Metadata bilgilerini al
            if pdf_reader.metadata:
                metadata = pdf_reader.metadata
                
                # Metadata alanları
                metadata_fields = {
                    '/Title': 'Başlık',
                    '/Author': 'Yazar',
                    '/Subject': 'Konu',
                    '/Creator': 'Oluşturan Yazılım',
                    '/Producer': 'PDF Üretici',
                    '/CreationDate': 'Oluşturma Tarihi',
                    '/ModDate': 'Değiştirme Tarihi',
                    '/Keywords': 'Anahtar Kelimeler',
                    '/Trapped': 'Trapped'
                }
                
                print(f"\n{Colors.SUCCESS}[+] Temel Bilgiler:{Colors.RESET}")
                print(f"  - Dosya Adı: {result['filename']}")
                print(f"  - Sayfa Sayısı: {result['num_pages']}")
                
                print(f"\n{Colors.SUCCESS}[+] PDF Metadata:{Colors.RESET}")
                for key, label in metadata_fields.items():
                    if key in metadata:
                        value = metadata[key]
                        result['metadata'][label] = str(value)
                        print(f"  - {label}: {value}")
            else:
                print(f"{Colors.WARNING}[!] Metadata bulunamadı{Colors.RESET}")
            
            # Dosya bilgileri
            stat = os.stat(pdf_path)
            result['file_info'] = {
                'size': f"{stat.st_size / 1024:.2f} KB",
                'created': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            }
            
            print(f"\n{Colors.SUCCESS}[+] Dosya Bilgileri:{Colors.RESET}")
            print(f"  - Boyut: {result['file_info']['size']}")
            print(f"  - Oluşturulma: {result['file_info']['created']}")
            print(f"  - Değiştirilme: {result['file_info']['modified']}")
            
            return result
            
    except FileNotFoundError:
        print(f"{Colors.ERROR}[-] Dosya bulunamadı: {pdf_path}{Colors.RESET}")
        return None
    except Exception as e:
        print(f"{Colors.ERROR}[-] Metadata çıkarma hatası: {e}{Colors.RESET}")
        return None

def extract_pdf_text(pdf_path, max_pages=5):
    """PDF'den metin çıkart"""
    print(f"\n{Colors.INFO}[*] PDF'den metin çıkartılıyor (ilk {max_pages} sayfa)...{Colors.RESET}")
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            text_content = []
            num_pages = min(len(pdf_reader.pages), max_pages)
            
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                text_content.append({
                    'page': page_num + 1,
                    'text': text[:500]  # İlk 500 karakter
                })
                
                print(f"{Colors.INFO}[*] Sayfa {page_num + 1} işlendi{Colors.RESET}")
            
            print(f"\n{Colors.SUCCESS}[+] {num_pages} sayfa metni çıkartıldı{Colors.RESET}")
            
            # İlk sayfanın bir önizlemesini göster
            if text_content:
                print(f"\n{Colors.SUCCESS}[+] İlk Sayfa Önizlemesi:{Colors.RESET}")
                print(text_content[0]['text'][:200] + "...")
            
            return text_content
            
    except Exception as e:
        print(f"{Colors.ERROR}[-] Metin çıkarma hatası: {e}{Colors.RESET}")
        return None

def analyze_pdf_security(pdf_path):
    """PDF güvenlik ayarlarını analiz et"""
    print(f"\n{Colors.INFO}[*] PDF güvenlik ayarları kontrol ediliyor...{Colors.RESET}")
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            security_info = {
                'is_encrypted': pdf_reader.is_encrypted,
                'permissions': {}
            }
            
            print(f"\n{Colors.SUCCESS}[+] Güvenlik Bilgileri:{Colors.RESET}")
            print(f"  - Şifreli: {'Evet' if security_info['is_encrypted'] else 'Hayır'}")
            
            # Eğer şifreliyse izinleri kontrol et
            if pdf_reader.is_encrypted:
                print(f"\n{Colors.WARNING}[!] Bu PDF şifrelidir{Colors.RESET}")
                print(f"{Colors.INFO}[*] Şifre gerektirmeden okunabildiyse, kullanıcı şifresi yok demektir{Colors.RESET}")
            
            return security_info
            
    except Exception as e:
        print(f"{Colors.ERROR}[-] Güvenlik analizi hatası: {e}{Colors.RESET}")
        return None

def extract_pdf_links(pdf_path):
    """PDF'deki linkleri çıkart"""
    print(f"\n{Colors.INFO}[*] PDF'deki linkler çıkartılıyor...{Colors.RESET}")
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            links = []
            
            for page_num, page in enumerate(pdf_reader.pages):
                if '/Annots' in page:
                    annotations = page['/Annots']
                    
                    for annotation in annotations:
                        obj = annotation.get_object()
                        
                        if '/A' in obj:
                            action = obj['/A']
                            if '/URI' in action:
                                uri = action['/URI']
                                links.append({
                                    'page': page_num + 1,
                                    'url': uri
                                })
            
            if links:
                print(f"\n{Colors.SUCCESS}[+] Bulunan Linkler ({len(links)} adet):{Colors.RESET}")
                for link in links[:20]:  # İlk 20'yi göster
                    print(f"  - Sayfa {link['page']}: {link['url']}")
                
                if len(links) > 20:
                    print(f"\n{Colors.INFO}[*] ... ve {len(links) - 20} link daha{Colors.RESET}")
            else:
                print(f"\n{Colors.WARNING}[!] Link bulunamadı{Colors.RESET}")
            
            return links
            
    except Exception as e:
        print(f"{Colors.ERROR}[-] Link çıkarma hatası: {e}{Colors.RESET}")
        return None

def remove_pdf_metadata(pdf_path, output_path=None):
    """PDF metadata'sını temizle"""
    print(f"\n{Colors.INFO}[*] PDF metadata'sı temizleniyor...{Colors.RESET}")
    
    try:
        if output_path is None:
            name, ext = os.path.splitext(pdf_path)
            output_path = f"{name}_no_metadata{ext}"
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            pdf_writer = PyPDF2.PdfWriter()
            
            # Tüm sayfaları kopyala
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)
            
            # Metadata'sız kaydet
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)
        
        print(f"{Colors.SUCCESS}[+] Metadata temizlendi{Colors.RESET}")
        print(f"{Colors.SUCCESS}[+] Kaydedildi: {output_path}{Colors.RESET}")
        
        return output_path
        
    except Exception as e:
        print(f"{Colors.ERROR}[-] Metadata temizleme hatası: {e}{Colors.RESET}")
        return None

def analyze_pdf_structure(pdf_path):
    """PDF yapısını analiz et"""
    print(f"\n{Colors.INFO}[*] PDF yapısı analiz ediliyor...{Colors.RESET}")
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            structure_info = {
                'total_pages': len(pdf_reader.pages),
                'has_outline': False,
                'has_forms': False,
                'has_javascript': False
            }
            
            # Outline (içindekiler) kontrolü
            if pdf_reader.outline:
                structure_info['has_outline'] = True
            
            print(f"\n{Colors.SUCCESS}[+] Yapı Bilgileri:{Colors.RESET}")
            print(f"  - Toplam Sayfa: {structure_info['total_pages']}")
            print(f"  - İçindekiler: {'Var' if structure_info['has_outline'] else 'Yok'}")
            
            # Sayfa boyutları
            print(f"\n{Colors.INFO}[*] Sayfa Boyutları:{Colors.RESET}")
            first_page = pdf_reader.pages[0]
            if '/MediaBox' in first_page:
                media_box = first_page['/MediaBox']
                width = float(media_box[2]) - float(media_box[0])
                height = float(media_box[3]) - float(media_box[1])
                print(f"  - Boyut: {width:.2f} x {height:.2f} points")
                print(f"  - Boyut (mm): {width*0.352778:.2f} x {height*0.352778:.2f} mm")
            
            return structure_info
            
    except Exception as e:
        print(f"{Colors.ERROR}[-] Yapı analizi hatası: {e}{Colors.RESET}")
        return None

def pdf_metadata_menu():
    """PDF metadata menüsü"""
    while True:
        clear_screen()
        print_header()
        
        menu = f"""{Colors.MENU}
╔═══════════════════════════════════════════════════════════════╗
║                  PDF METADATA MENÜSÜ                         ║
╚═══════════════════════════════════════════════════════════════╝

  {Colors.INPUT}[1]{Colors.RESET} 📋 Metadata Çıkart
  {Colors.INPUT}[2]{Colors.RESET} 📝 Metin Çıkart
  {Colors.INPUT}[3]{Colors.RESET} 🔒 Güvenlik Analizi
  {Colors.INPUT}[4]{Colors.RESET} 🔗 Linkleri Çıkart
  {Colors.INPUT}[5]{Colors.RESET} 🧹 Metadata Temizle
  {Colors.INPUT}[6]{Colors.RESET} 🏗️  Yapı Analizi
  {Colors.INPUT}[7]{Colors.RESET} 📊 Tam Analiz (Hepsi)
  {Colors.INPUT}[0]{Colors.RESET} 🔙 Ana Menüye Dön

{Colors.INPUT}Seçiminiz: {Colors.RESET}"""
        
        print(menu, end='')
        choice = input().strip()
        
        if choice == '0':
            break
        elif choice == '1':
            pdf_path = input(f"\n{Colors.INPUT}PDF dosya yolunu girin: {Colors.RESET}").strip()
            if pdf_path and os.path.exists(pdf_path):
                result = extract_pdf_metadata(pdf_path)
                if result:
                    save_result(f"metadata_{os.path.basename(pdf_path)}", result)
            else:
                print(f"{Colors.ERROR}[-] Dosya bulunamadı{Colors.RESET}")
        elif choice == '2':
            pdf_path = input(f"\n{Colors.INPUT}PDF dosya yolunu girin: {Colors.RESET}").strip()
            if pdf_path and os.path.exists(pdf_path):
                max_pages = input(f"{Colors.INPUT}Kaç sayfa analiz edilsin? (varsayılan: 5): {Colors.RESET}").strip()
                max_pages = int(max_pages) if max_pages.isdigit() else 5
                result = extract_pdf_text(pdf_path, max_pages)
                if result:
                    save_result(f"text_{os.path.basename(pdf_path)}", result)
            else:
                print(f"{Colors.ERROR}[-] Dosya bulunamadı{Colors.RESET}")
        elif choice == '3':
            pdf_path = input(f"\n{Colors.INPUT}PDF dosya yolunu girin: {Colors.RESET}").strip()
            if pdf_path and os.path.exists(pdf_path):
                result = analyze_pdf_security(pdf_path)
                if result:
                    save_result(f"security_{os.path.basename(pdf_path)}", result)
            else:
                print(f"{Colors.ERROR}[-] Dosya bulunamadı{Colors.RESET}")
        elif choice == '4':
            pdf_path = input(f"\n{Colors.INPUT}PDF dosya yolunu girin: {Colors.RESET}").strip()
            if pdf_path and os.path.exists(pdf_path):
                result = extract_pdf_links(pdf_path)
                if result:
                    save_result(f"links_{os.path.basename(pdf_path)}", result)
            else:
                print(f"{Colors.ERROR}[-] Dosya bulunamadı{Colors.RESET}")
        elif choice == '5':
            pdf_path = input(f"\n{Colors.INPUT}PDF dosya yolunu girin: {Colors.RESET}").strip()
            if pdf_path and os.path.exists(pdf_path):
                output_path = input(f"{Colors.INPUT}Çıktı dosya yolu (boş bırakabilirsiniz): {Colors.RESET}").strip()
                remove_pdf_metadata(pdf_path, output_path if output_path else None)
            else:
                print(f"{Colors.ERROR}[-] Dosya bulunamadı{Colors.RESET}")
        elif choice == '6':
            pdf_path = input(f"\n{Colors.INPUT}PDF dosya yolunu girin: {Colors.RESET}").strip()
            if pdf_path and os.path.exists(pdf_path):
                result = analyze_pdf_structure(pdf_path)
                if result:
                    save_result(f"structure_{os.path.basename(pdf_path)}", result)
            else:
                print(f"{Colors.ERROR}[-] Dosya bulunamadı{Colors.RESET}")
        elif choice == '7':
            pdf_path = input(f"\n{Colors.INPUT}PDF dosya yolunu girin: {Colors.RESET}").strip()
            if pdf_path and os.path.exists(pdf_path):
                full_result = {}
                
                result = extract_pdf_metadata(pdf_path)
                if result:
                    full_result['metadata'] = result
                
                result = analyze_pdf_security(pdf_path)
                if result:
                    full_result['security'] = result
                
                result = extract_pdf_links(pdf_path)
                if result:
                    full_result['links'] = result
                
                result = analyze_pdf_structure(pdf_path)
                if result:
                    full_result['structure'] = result
                
                if full_result:
                    save_result(f"full_analysis_{os.path.basename(pdf_path)}", full_result)
            else:
                print(f"{Colors.ERROR}[-] Dosya bulunamadı{Colors.RESET}")
        else:
            print(f"{Colors.ERROR}[-] Geçersiz seçim!{Colors.RESET}")
        
        input(f"\n{Colors.INPUT}Devam etmek için Enter'a basın...{Colors.RESET}")

def main():
    """Ana fonksiyon"""
    try:
        pdf_metadata_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}[!] İşlem iptal edildi{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.ERROR}[-] Beklenmeyen hata: {e}{Colors.RESET}")

if __name__ == "__main__":
    main()
