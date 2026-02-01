@echo off
REM HIG-Osint Windows Kurulum Scripti
REM Developer: Halil Gercek
REM Email: higeryazilim@gmail.com
REM GitHub: https://github.com/Higer23/HIG-Osint

cls
color 0B

echo.
echo ================================================================
echo                   HIG-OSINT KURULUM
echo               Windows Icin Ozel Kurulum
echo ================================================================
echo.

echo [*] HIG-Osint Windows'a kuruluyor...
echo.

REM Python kontrolu
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] Python bulunamadi!
    echo [!] Lutfen Python 3.8 veya uzeri yuklediginizden emin olun.
    echo [!] https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/5] Python versiyonu kontrol ediliyor...
python --version

echo.
echo [2/5] Pip guncelleniyor...
python -m pip install --upgrade pip

echo.
echo [3/5] Python bagimliliklari kuruluyor...
python -m pip install -r requirements.txt

echo.
echo [4/5] Ek Windows paketleri kuruluyor...
python -m pip install windows-curses pywin32

echo.
echo [5/5] Launcher olusturuluyor...

REM higosint.bat olustur
echo @echo off > higosint.bat
echo python "%~dp0higosint.py" %%* >> higosint.bat

echo.
echo ================================================================
echo          + KURULUM BASARIYLA TAMAMLANDI!
echo ================================================================
echo.
echo [*] HIG-Osint'i baslatmak icin su komutlari kullanabilirsiniz:
echo     - python higosint.py
echo     - higosint.bat
echo     - higosint (PATH'e eklediyseniz)
echo.
echo [*] Gelistirici: Halil Gercek
echo [*] Email: higeryazilim@gmail.com
echo [*] GitHub: https://github.com/Higer23/HIG-Osint
echo.
pause
