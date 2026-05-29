@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

REM PYTHONUTF8=1 ayarla - conda kodlama hatalarini onle
set "PYTHONUTF8=1"

REM Yonetici modunda %CD%'nin system32'ye donmesi sorununu duzelt
REM Calisma dizini olarak betigin bulundugu dizini kullan
cd /d "%~dp0"
set "SCRIPT_DIR=%~dp0"
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

echo.
echo ========================================
echo Manga Cevirici - Tek Tikla Kurulum
echo Manga Translator UI - Installer
echo ========================================
echo.
echo Bu betik asagidaki adimlari otomatik tamamlayacak:
echo [1] Miniconda kur (Python ortam yoneticisi, gerekirse)
echo [2] Tasinalir Git indir (gerekirse)
echo [3] GitHub'dan kodu klonla
echo [4] Python ortami olustur ve bagimliliklari yukle
echo [5] Kurulumu tamamla
echo.
pause

REM ===== Adim 1: Miniconda kontrol/kurulum =====
echo.
echo [1/5] Miniconda (Python ortam yoneticisi) kontrol ediliyor...
echo ========================================

REM Yerel Miniconda kurulumu kontrol et
set MINICONDA_ROOT=%SCRIPT_DIR%\Miniconda3
set CONDA_INSTALLED=0
set PATH_HAS_NONASCII=0
set ALT_INSTALL_PATH=

REM Yolun ASCII olmayan karakter icerip icermedigini kontrol et
REM Daha guvenilir tespit icin PowerShell kullan
set "TEMP_CHECK_PATH=%SCRIPT_DIR%"
powershell -Command "$path = '%TEMP_CHECK_PATH%'; if ($path -match '[^\x00-\x7F]') { exit 1 } else { exit 0 }" >nul 2>&1
if errorlevel 1 (
    REM Yol ASCII olmayan karakter iceriyor, disk koku dizinini kullan
    set MINICONDA_ROOT=%~d0\Miniconda3
    set PATH_HAS_NONASCII=1
)

REM Once sistemde conda var mi kontrol et (genel kurulum)
where conda >nul 2>&1
if %ERRORLEVEL% neq 0 goto :check_local_conda

:found_system_conda
echo [OK] Sistemde Conda kurulu tespit edildi
echo.

REM Yontem 1: CONDA_EXE ortam degiskeninden al (en guvenilir)
if defined CONDA_EXE (
    REM CONDA_EXE genellikle D:\Miniconda3\Scripts\conda.exe'yi gosterir
    REM Kok dizini almak icin iki ust dizine cikmak gerekir
    for %%p in ("%CONDA_EXE%\..\..") do set "MINICONDA_ROOT=%%~fp"
)

REM Yontem 2: CONDA_PREFIX ortam degiskeninden al
if "!MINICONDA_ROOT!"=="" (
    if defined CONDA_PREFIX (
        set "MINICONDA_ROOT=%CONDA_PREFIX%"
    )
)

REM Yontem 3: conda info --base kullan (basarisiz olabilir)
if "!MINICONDA_ROOT!"=="" (
    for /f "delims=" %%i in ('conda info --base 2^>nul') do (
        REM Donen degerin gecerli bir yol olup olmadigini kontrol et
        set "TEMP_PATH=%%i"
        if exist "!TEMP_PATH!\Scripts\conda.exe" (
            set "MINICONDA_ROOT=%%i"
        )
    )
)

REM Yontem 4: where conda ciktisini ayristir
if "!MINICONDA_ROOT!"=="" (
    for /f "delims=" %%i in ('where conda 2^>nul') do (
        REM Yalnizca ilk bulunan conda.exe'yi al (Scripts dizinindeki)
        if "!MINICONDA_ROOT!"=="" (
            if "%%~xi"==".exe" (
                for %%p in ("%%~dpi..") do set "MINICONDA_ROOT=%%~fp"
            ) else if "%%~xi"==".bat" (
                REM .bat dosyasiysa iki ust dizine cik
                for %%p in ("%%~dpi..\..") do set "MINICONDA_ROOT=%%~fp"
            )
        )
    )
)

REM Conda bilgilerini goster (hata yonetimi ekle)
if not "!MINICONDA_ROOT!"=="" (
    echo Konum: !MINICONDA_ROOT!
    call conda --version 2>nul
    if !ERRORLEVEL! neq 0 (
        echo [UYARI] Conda surum bilgisi alinamadi
    )
) else (
    echo [UYARI] Conda kurulum yolu belirlenemedi
    echo Sistem conda komutu kullanilacak
)

echo.
pause

goto :check_git

:check_local_conda
REM Yerel Miniconda kontrol et
if exist "%MINICONDA_ROOT%\Scripts\conda.exe" goto :found_local_conda
goto :install_conda

:found_local_conda
echo [OK] Yerel Miniconda kurulu tespit edildi
echo Konum: %MINICONDA_ROOT%
call "%MINICONDA_ROOT%\Scripts\conda.exe" --version
goto :check_git

:install_conda

REM Bilgi: Yerel Miniconda kurulmasi gerekiyor
echo [BILGI] Yerel Miniconda tespit edilemedi
echo ========================================
echo.
echo Bu proje Python 3.12 ortami gerektiriyor
echo.

REM Yol ASCII olmayan karakter iceriyorsa aciklama goster ve yedek yol kullan
if !PATH_HAS_NONASCII!==1 goto :__PATH_WARNING
goto :__PATH_WARNING_END

:__PATH_WARNING
echo ========================================
echo [UYARI] Yolda ASCII olmayan karakter tespit edildi
echo ========================================
echo Mevcut yol: %SCRIPT_DIR%
echo.
echo Miniconda'nin ASCII olmayan yollarla uyumlulugu sinirlidir
echo Yedek kurulum yolu otomatik kullanilacak: !MINICONDA_ROOT!
echo (Ayni disk, farkli konum)
echo.
echo Oneri: Olasi diger sorunlari onlemek icin projeyi sadece ASCII
echo        karakterlerden olusan bir yola tasiyabilirsiniz
echo        Ornek: D:\manga-translator\
echo.
pause
echo.
goto :__PATH_WARNING_END

:__PATH_WARNING_END
echo.

echo Miniconda su konuma kurulacak: %MINICONDA_ROOT%
echo.
        echo Miniconda ozellikleri:
        echo   - Kucuk boyut (yaklasik 50MB)
        echo   - Birden fazla Python surumuyle calisabilir
        echo   - Ortam izolasyonu, birbirini etkilemez
        echo   - Dahili pip paket yoneticisi
        echo.
echo Miniconda kurulsun mu?
echo [1] Evet (Onerilen) - Otomatik indir ve kur
echo [2] Hayir - Manuel kur, sonra betigi yeniden calistir
echo [3] Kurulumu iptal et
echo.
set /p install_conda="Seciniz (1/2/3, varsayilan 1): "

if "%install_conda%"=="2" (
    echo.
    echo Miniconda indirmek icin asagidaki adresleri ziyaret edin:
    echo   Resmi: https://docs.conda.io/en/latest/miniconda.html
    echo   Ayna:  https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/
    echo.
    echo Kurulum sirasinda "Add to PATH" secenegini isaretleyin
    echo Kurulum tamamlaninca bu betigi yeniden calistirin
    pause
    exit /b 1
)

if "%install_conda%"=="3" (
    echo Kurulum iptal edildi
    pause
    exit /b 1
)

REM Miniconda indir ve kur
echo.
echo Miniconda indiriliyor...
echo.

REM Miniconda indirme baglantilari (Python 3.12 surumu)
set MINICONDA_OFFICIAL=https://repo.anaconda.com/miniconda/Miniconda3-py312_25.9.1-1-Windows-x86_64.exe
set MINICONDA_TUNA=https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-py312_25.9.1-1-Windows-x86_64.exe

echo Indirme kaynagi secin:
echo [1] Tsinghua Universitesi Aynasi (Cin icin onerilen, daha hizli)
echo [2] Anaconda Resmi
echo.
set /p conda_source="Seciniz (1/2, varsayilan 1): "

if "%conda_source%"=="2" (
    set MINICONDA_URL=%MINICONDA_OFFICIAL%
    echo Kullanilan: Anaconda resmi kaynak
) else (
    set MINICONDA_URL=%MINICONDA_TUNA%
    echo Kullanilan: Tsinghua Universitesi aynasi
)

echo.
echo Indiriliyor... (yaklasik 50MB, birka dakika surebilir)
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; $ProgressPreference = 'SilentlyContinue'; Write-Host 'Miniconda indiriliyor...'; try { Invoke-WebRequest -Uri '%MINICONDA_URL%' -OutFile 'Miniconda3-latest.exe' -UseBasicParsing; Write-Host '[OK] Indirme tamamlandi'; exit 0 } catch { Write-Host '[HATA] Indirme basarisiz: $_'; exit 1 }}"

if %ERRORLEVEL% neq 0 (
    echo.
    echo [HATA] Indirme basarisiz, lutfen internet baglantinizi kontrol edin
    echo.
    echo Yapabilecekleriniz:
    echo 1. Manuel indirme: %MINICONDA_URL%
    echo 2. Dosyayi kaydedin: Miniconda3-latest.exe
    echo 3. Mevcut dizine koyup betigi yeniden calistirin
    pause
    exit /b 1
)

echo.
echo Miniconda kuruluyor...
echo.
echo Kurulum secenekleri:
echo   - Kurulum konumu: %MINICONDA_ROOT%
echo   - Python surumu: 3.12
echo   - Yalnizca bu proje icin kullanilir
echo.
echo Sessiz kurulum baslatiliyor...
timeout /t 2 >nul

        REM Miniconda sessiz kurulum
        start /wait Miniconda3-latest.exe /InstallationType=JustMe /AddToPath=1 /RegisterPython=0 /S /D=%MINICONDA_ROOT%

        if %ERRORLEVEL% neq 0 (
            echo.
            echo [HATA] Miniconda kurulumu basarisiz
            echo.
            pause
            exit /b 1
        )

        echo.
        echo [OK] Miniconda kurulumu tamamlandi
        echo.

        REM Kurulum paketini temizle
        if exist "Miniconda3-latest.exe" (
            echo Kurulum paketi temizleniyor...
            del /f /q "Miniconda3-latest.exe" >nul 2>&1
            if %ERRORLEVEL% == 0 (
                echo [OK] Kurulum paketi temizlendi
            )
        )
        echo.

        REM Conda ortamini baslat
        echo Conda ortami baslatiliyor...
        call "%MINICONDA_ROOT%\Scripts\activate.bat"
        call conda init cmd.exe >nul 2>&1

        echo.
        echo [OK] Miniconda kuruldu ve yapilandirildi
        echo Kurulum konumu: %MINICONDA_ROOT%
        echo.
        echo Lutfen mevcut komut penceresini kapatin ve bu betigi yeniden calistirin
        echo (Ortam degiskenlerinin yeniden yuklenmesi gerekiyor)
        pause
        exit /b 0

REM ===== Adim 2: Git kontrol/indir =====
:check_git
echo.
echo [2/5] Git kontrol ediliyor...
echo ========================================

REM Once yerel tasinalir Git surumunu kontrol et
if exist "%SCRIPT_DIR%\PortableGit\cmd\git.exe" (
    set "GIT=%SCRIPT_DIR%\PortableGit\cmd\git.exe"
    set "PATH=%SCRIPT_DIR%\PortableGit\cmd;%PATH%"
    echo [OK] Yerel tasinalir Git bulundu
    "%SCRIPT_DIR%\PortableGit\cmd\git.exe" --version
    goto :clone_repo
)

REM Sistemin PATH'indeki git'i kontrol et
where git >nul 2>&1
if %ERRORLEVEL% == 0 (
    set GIT=git
    echo [OK] Sistem Git bulundu
    git --version
    goto :clone_repo
)

echo [BILGI] Git bulunamadi
echo.
echo Git, kod cekme icin gereklidir, lutfen secin:
echo [1] Tasinalir Git indir (Onerilen, yaklasik 50MB)
echo [2] Cik, Git'i manuel kur
echo.
set /p git_choice="Seciniz (1/2): "

if "%git_choice%"=="2" (
    echo.
    echo Indirme adresi: https://git-scm.com/downloads
    pause
    exit /b 0
)

if not "%git_choice%"=="1" (
    echo Gecersiz secim
    goto :check_git
)

REM Git indir
echo.
echo Git tasinalir surumu indiriliyor...
echo.
echo Indirme kaynagi secin:
echo [1] GitHub Resmi
echo [2] gh-proxy.com Aynasi (Cin icin onerilen)
echo.
set /p git_source="Seciniz (1/2, varsayilan 2): "

set GIT_VERSION=2.43.0
set GIT_ARCH=64-bit

if "%git_source%"=="1" (
    set GIT_URL=https://github.com/git-for-windows/git/releases/download/v%GIT_VERSION%.windows.1/PortableGit-%GIT_VERSION%-%GIT_ARCH%.7z.exe
    echo Kullanilan: GitHub resmi kaynagi
) else (
    set GIT_URL=https://gh-proxy.com/https://github.com/git-for-windows/git/releases/download/v%GIT_VERSION%.windows.1/PortableGit-%GIT_VERSION%-%GIT_ARCH%.7z.exe
    echo Kullanilan: gh-proxy.com aynasi
)

echo.
echo Indiriliyor... (yaklasik 50MB, birka dakika surebilir)
if not exist "tmp" mkdir tmp
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; $ProgressPreference = 'SilentlyContinue'; Write-Host 'Indiriliyor...'; try { Invoke-WebRequest -Uri '%GIT_URL%' -OutFile 'tmp\PortableGit.7z.exe' -UseBasicParsing; Write-Host '[OK] Indirme tamamlandi'; exit 0 } catch { Write-Host '[HATA] Indirme basarisiz: $_'; exit 1 }}"

if %ERRORLEVEL% neq 0 (
    echo.
    echo Indirme basarisiz, internet baglantinizi kontrol edip yeniden deneyin
    pause
    exit /b 1
)

echo.
echo Git aciliyor...
tmp\PortableGit.7z.exe -o"PortableGit" -y >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Acma islemi basarisiz
    pause
    exit /b 1
)

del tmp\PortableGit.7z.exe >nul 2>&1
set GIT=PortableGit\cmd\git.exe
set "PATH=%CD%\PortableGit\cmd;%PATH%"
echo [OK] Git kurulumu tamamlandi
PortableGit\cmd\git.exe --version

REM ===== Adim 3: Depoyu klonla/guncelle =====
:clone_repo
echo.
echo [3/5] Kod deposu kontrol ediliyor...
echo ========================================
echo.

REM Sikistirilmis dosyadan acilip acilmadigini kontrol et (.git olmadan kod var)
if not exist ".git" (
    if exist "manga_translator" if exist "desktop_qt_ui" if exist "packaging\VERSION" (
        echo [BILGI] Sikistirilmis dosyadan acilmis kod dosyalari tespit edildi
        echo.
        echo Seciniz:
        echo [1] Git yapilandirmasini atla, dogrudan bagimliliklari yukle (Adim4 ile guncellenemez)
        echo [2] Git deposunu baslat ve uzak depoya bagla (Adim4 ile guncellenebilir)
        echo [3] Cik
        echo.
        set /p zip_choice="Seciniz (1/2/3, varsayilan 2): "
        
        if "!zip_choice!"=="3" (
            exit /b 0
        ) else if "!zip_choice!"=="1" (
            echo [OK] Git yapilandirmasi atlaniyor, mevcut kod kullaniliyor
            echo.
            goto :create_venv
        ) else (
            echo [BILGI] Git deposu baslatiliyor...
            "%GIT%" init
            if !ERRORLEVEL! neq 0 (
                echo [HATA] Git baslatma basarisiz
                pause
                exit /b 1
            )
            REM Hedef depo adresini al
            call :get_repo_url
            echo.
            echo Uzak depo ekleniyor...
            "%GIT%" remote add origin !REPO_URL!
            if !ERRORLEVEL! neq 0 (
                echo [HATA] Uzak depo eklenemedi
                pause
                exit /b 1
            )
            echo.
            echo Uzak dal getiriliyor...
            "%GIT%" fetch origin
            if !ERRORLEVEL! neq 0 (
                echo [UYARI] Uzak dal getirilemedi, ag sorunu olabilir
                echo [BILGI] Git yapilandirmasi atlanarak mevcut kod kullanilacak
                echo.
                goto :create_venv
            )
            echo.
            echo [OK] Git deposu baslatildi
            echo [BILGI] Guncelleme icin Adim4 kullanilabilir
            echo.
            goto :create_venv
        )
    )
)

REM Hedef depo adresini al
call :get_repo_url

REM Kod deposunun zaten var olup olmadigini kontrol et
if exist ".git" (
    echo [BILGI] Mevcut Git deposu tespit edildi
    
    REM Mevcut depo adresini al
    for /f "delims=" %%i in ('"%GIT%" config --get remote.origin.url 2^>nul') do set CURRENT_REPO=%%i
    
    if defined CURRENT_REPO (
        echo Mevcut depo: !CURRENT_REPO!
        echo Hedef depo:  !REPO_URL!
        echo.
        
        REM Depo adreslerini karsilastirmak icin standartlastir (ayna oneklerini kaldir)
        set CURRENT_CLEAN=!CURRENT_REPO:.git=!
        set TARGET_CLEAN=!REPO_URL:.git=!
        
        REM Yaygin ayna oneklerini kaldir, github.com adresine donustur
        set CURRENT_CLEAN=!CURRENT_CLEAN:https://gh-proxy.com/https://github.com/=https://github.com/!
        set CURRENT_CLEAN=!CURRENT_CLEAN:https://ghproxy.com/https://github.com/=https://github.com/!
        set CURRENT_CLEAN=!CURRENT_CLEAN:https://mirror.ghproxy.com/https://github.com/=https://github.com/!
        set CURRENT_CLEAN=!CURRENT_CLEAN:https://ghfast.top/https://github.com/=https://github.com/!
        set CURRENT_CLEAN=!CURRENT_CLEAN:https://gitproxy.click/https://github.com/=https://github.com/!
        
        set TARGET_CLEAN=!TARGET_CLEAN:https://gh-proxy.com/https://github.com/=https://github.com/!
        set TARGET_CLEAN=!TARGET_CLEAN:https://ghproxy.com/https://github.com/=https://github.com/!
        set TARGET_CLEAN=!TARGET_CLEAN:https://mirror.ghproxy.com/https://github.com/=https://github.com/!
        set TARGET_CLEAN=!TARGET_CLEAN:https://ghfast.top/https://github.com/=https://github.com/!
        set TARGET_CLEAN=!TARGET_CLEAN:https://gitproxy.click/https://github.com/=https://github.com/!
        
        if "!CURRENT_CLEAN!"=="!TARGET_CLEAN!" (
            echo [OK] Depo adresi eslesti, en son surume zorla senkronize ediliyor...
            echo.
            
            echo Uzak guncellemeler getiriliyor...
            "%GIT%" fetch origin
            if !ERRORLEVEL! neq 0 (
                echo [UYARI] Guncelleme getirilemedi, ag sorunu olabilir
                echo.
                echo Seciniz:
                echo [1] Yeniden dene
                echo [2] Cik
                echo.
                set /p network_choice="Seciniz (1/2, varsayilan 1): "
                
                if "!network_choice!"=="2" goto :install_cancelled
                echo [BILGI] Guncelleme yeniden deneniyor...
                goto :clone_repo
            )
                echo Uzak ana dala zorla senkronize ediliyor...
                "%GIT%" reset --hard origin/main
                if !ERRORLEVEL! == 0 (
                    echo [OK] Kod en son suruyme guncellendi
                    echo.
                    echo macOS betikleri ve Git yapilandirma dosyalari temizleniyor...
                    if exist "macOS_1_IlkKurulum.sh" del /f /q "macOS_1_IlkKurulum.sh" >nul 2>&1
                    if exist "macOS_2_QtArayuzuBaslat.sh" del /f /q "macOS_2_QtArayuzuBaslat.sh" >nul 2>&1
                    if exist "macOS_3_GuncellemeKontrolVeBaslat.sh" del /f /q "macOS_3_GuncellemeKontrolVeBaslat.sh" >nul 2>&1
                    if exist "macOS_4_GuncellemeVeBakim.sh" del /f /q "macOS_4_GuncellemeVeBakim.sh" >nul 2>&1
                    if exist ".gitattributes" del /f /q ".gitattributes" >nul 2>&1
                    if exist ".gitignore" del /f /q ".gitignore" >nul 2>&1
                    if exist "LICENSE.txt" del /f /q "LICENSE.txt" >nul 2>&1
                    echo [OK] macOS betikleri ve Git yapilandirma dosyalari temizlendi
                    echo.
                    goto :create_venv
                ) else (
                    echo [UYARI] Senkronizasyon basarisiz, main dali deneniyor...
                    "%GIT%" checkout -f main
                    "%GIT%" reset --hard origin/main
                    if !ERRORLEVEL! == 0 (
                        echo [OK] Kod en son suruyme guncellendi
                        echo.
                        echo macOS betikleri ve Git yapilandirma dosyalari temizleniyor...
                        if exist "macOS_1_IlkKurulum.sh" del /f /q "macOS_1_IlkKurulum.sh" >nul 2>&1
                        if exist "macOS_2_QtArayuzuBaslat.sh" del /f /q "macOS_2_QtArayuzuBaslat.sh" >nul 2>&1
                        if exist "macOS_3_GuncellemeKontrolVeBaslat.sh" del /f /q "macOS_3_GuncellemeKontrolVeBaslat.sh" >nul 2>&1
                        if exist "macOS_4_GuncellemeVeBakim.sh" del /f /q "macOS_4_GuncellemeVeBakim.sh" >nul 2>&1
                        if exist ".gitattributes" del /f /q ".gitattributes" >nul 2>&1
                        if exist ".gitignore" del /f /q ".gitignore" >nul 2>&1
                        if exist "LICENSE.txt" del /f /q "LICENSE.txt" >nul 2>&1
                        echo [OK] macOS betikleri ve Git yapilandirma dosyalari temizlendi
                        echo.
                        goto :create_venv
                    ) else (
                        echo [UYARI] Senkronizasyon basarisiz
                        echo.
                        echo Seciniz:
                        echo [1] Yeniden dene
                        echo [2] Cik
                        echo.
                        set /p sync_choice="Seciniz (1/2, varsayilan 1): "
                        
                        if "!sync_choice!"=="2" goto :install_cancelled
                        echo [BILGI] Senkronizasyon yeniden deneniyor...
                        goto :clone_repo
                    )
                )
            )
        ) else (
            echo [UYARI] Depo adresi eslesmiyor, silip yeniden klonlanacak
            echo Mevcut depo: !CURRENT_REPO!
            echo Hedef depo:  !REPO_URL!
            echo.
        )
    ) else (
        echo [UYARI] Depo bilgileri okunamiyor, silip yeniden klonlanacak
        echo.
    )
    
    REM Temizlemeden once onay al
    echo ========================================
    echo ***  UYARI: Dosyalar Silinecek  ***
    echo ========================================
    echo.
    echo +----------------------------------------+
    echo ¦  TEHLIKELI ISLEM: Cok sayida dosya     ¦
    echo ¦  silinecek!                            ¦
    echo +----------------------------------------+
    echo.
    echo [Silinecek Kapsam]
    echo   Korunan dosyalar disindaki TUM dosya ve klasorler silinecek!
    echo.
    echo [Yalnizca asagidakiler korunacak]
    echo   * venv / conda_env (Python ortami)
    echo   * PortableGit (Tasinalir Git)
    echo   * Miniconda3 (Conda ortami)
    echo   * Kurulum betigi (Adim1-IlkKurulum.bat)
    echo.
    echo +----------------------------------------+
    echo ¦  Diger TUM dosya ve klasorler          ¦
    echo ¦  kalici olarak silinecek!              ¦
    echo +----------------------------------------+
    echo.
    echo Devam edilsin mi?
    echo [1] Evet - Sil ve yeniden klonla
    echo [2] Hayir - Kurulumu iptal et (onemli dosyalari once yedekleyin)
    echo.
    set /p confirm_delete="Seciniz (1/2, varsayilan 2): "
    
    if not "!confirm_delete!"=="1" (
        echo.
        echo Kurulum iptal edildi
        pause
        exit /b 1
    )
    
:delete_and_clone
    REM Mevcut dosya ve klasorleri sil (venv, PortableGit, Python-3.12.12, Portable7z, Miniconda3, conda_env korunur)
    echo.
    echo Eski dosyalar temizleniyor...
    
    REM Klasorleri sil (venv, conda_env, PortableGit, Python-3.12.12, Portable7z, Miniconda3 korunur)
    for /d %%d in (*) do (
        if /i not "%%d"=="venv" if /i not "%%d"=="conda_env" if /i not "%%d"=="PortableGit" if /i not "%%d"=="Python-3.12.12" if /i not "%%d"=="Portable7z" if /i not "%%d"=="Miniconda3" (
            echo Klasor siliniyor: %%d
            rmdir /s /q "%%d" 2>nul
        )
    )
    
    REM Dosyalari sil (calistirilan betigi koru)
    for %%f in (*) do (
        if /i not "%%~nxf"=="Adim1-IlkKurulum.bat" (
            echo Dosya siliniyor: %%~nxf
            del /f /q "%%f" 2>nul
        )
    )
    
    REM Gizli .git klasorunu sil
    if exist ".git" (
        echo .git klasoru siliniyor...
        rmdir /s /q ".git" 2>nul
        if exist ".git" (
            echo [HATA] .git klasoru silinemedi, kullanimda olabilir - lutfen ilgili programlari kapatin
            echo Ilgili tum programlari kapatip yeniden deneyin
            pause
            exit /b 1
        )
    )
    
    echo [OK] Eski veriler temizlendi
    echo.
)

echo Depo adresi: !REPO_URL!
echo Kurulum dizini: %SCRIPT_DIR%
echo.
goto :do_clone

:get_repo_url
echo Klonlama kaynagi secin:
echo [1] GitHub Resmi (Yurt disi icin onerilen)
echo [2] gh-proxy.com Aynasi (Yurt ici icin onerilen)
echo [3] Depo adresini manuel gir
echo.
set /p repo_choice="Seciniz (1/2/3, varsayilan 1): "

if "!repo_choice!"=="1" (
    set REPO_URL=https://github.com/211014049/manga-translator-ui.git
    echo Kullanilan: GitHub resmi
) else if "!repo_choice!"=="3" (
    set /p REPO_URL="Depo adresini girin: "
    echo Kullanilan: Ozel adres
) else (
    set REPO_URL=https://github.com/211014049/manga-translator-ui.git
    echo Kullanilan: GitHub resmi
)
echo.
goto :eof

:do_clone

REM Gecici dizine klonla
set TEMP_DIR=manga_translator_temp_%RANDOM%
echo Kod gecici dizine klonlaniyor... (birkac dakika surebilir)
echo.
"%GIT%" clone !REPO_URL! %TEMP_DIR%

echo.
echo [DEBUG] Klonlama sonucu kontrol ediliyor...
if exist "%TEMP_DIR%" (
    if exist "%TEMP_DIR%\.git" (
        goto :copy_files
    )
)

REM Buraya gelindiyse klonlama basarisiz demektir
echo.
echo [HATA] Klonlama basarisiz
echo.
echo Olasi nedenler:
echo 1. Ag baglantisi sorunu
echo 2. Hatali depo adresi
echo 3. GitHub erisimi kisitli (GHProxy aynasini secerek yeniden deneyin)
echo.
if exist "%TEMP_DIR%" rmdir /s /q "%TEMP_DIR%"
set /p retry="Yeniden denensin mi? (e/h): "
if /i "!retry!"=="e" goto :clone_repo
pause
exit /b 1

:copy_files

echo.
echo Dosyalar kopyalaniyor...

echo Klasorler kopyalaniyor...
for /d %%i in ("%TEMP_DIR%\*") do (
    if /i not "%%~nxi"=="PortableGit" (
        xcopy "%%i" "%SCRIPT_DIR%\%%~nxi\" /E /H /Y /I /Q
        if !ERRORLEVEL! neq 0 echo [HATA] Klasor kopyalanamadi: %%~nxi
    )
)

echo.
echo Dosyalar kopyalaniyor...
for %%i in ("%TEMP_DIR%\*") do (
    if /i not "%%~nxi"=="Adim1-IlkKurulum.bat" (
        copy /Y "%%i" "%SCRIPT_DIR%\" >nul
        if !ERRORLEVEL! neq 0 echo [HATA] Dosya kopyalanamadi: %%~nxi
    )
)

echo.
echo Gizli dosyalar kopyalaniyor...
if exist "%TEMP_DIR%\.git\" (
    xcopy "%TEMP_DIR%\.git" ".git\" /E /H /Y /I /Q
    if !ERRORLEVEL! neq 0 echo [HATA] .git kopyalanamadi
)

if exist "%TEMP_DIR%\.gitignore" (
    copy /Y "%TEMP_DIR%\.gitignore" . >nul
    if !ERRORLEVEL! neq 0 echo [HATA] .gitignore kopyalanamadi
)

echo.
echo macOS betikleri ve Git yapilandirma dosyalari temizleniyor...
if exist "macOS_1_IlkKurulum.sh" del /f /q "macOS_1_IlkKurulum.sh" >nul 2>&1
if exist "macOS_2_QtArayuzuBaslat.sh" del /f /q "macOS_2_QtArayuzuBaslat.sh" >nul 2>&1
if exist "macOS_3_GuncellemeKontrolVeBaslat.sh" del /f /q "macOS_3_GuncellemeKontrolVeBaslat.sh" >nul 2>&1
if exist "macOS_4_GuncellemeVeBakim.sh" del /f /q "macOS_4_GuncellemeVeBakim.sh" >nul 2>&1
if exist ".gitattributes" del /f /q ".gitattributes" >nul 2>&1
if exist ".gitignore" del /f /q ".gitignore" >nul 2>&1
if exist "LICENSE.txt" del /f /q "LICENSE.txt" >nul 2>&1
echo [OK] macOS betikleri ve Git yapilandirma dosyalari temizlendi

echo.
echo Gecici dizin temizleniyor...
rmdir /s /q "%TEMP_DIR%"
if !ERRORLEVEL! neq 0 (
    echo [HATA] Gecici dizin temizlenemedi
)

echo.
echo [OK] Kod klonlama tamamlandi

:create_venv

REM ===== Adim 4: Conda ortami olustur ve bagimliliklari yukle =====
echo.
echo.
echo ========================================
echo [4/5] Python ortami olusturuluyor ve bagimliliklar yukleniyor...
echo ========================================
echo.

REM Conda yolunu yeniden tespit et (degiskenin kullanilabilir oldugunu dogrula)
if not defined MINICONDA_ROOT (
    set MINICONDA_ROOT=%SCRIPT_DIR%\Miniconda3
    REM Yolun ASCII olmayan karakter icerip icermedigini kontrol et
    powershell -Command "$path = '%SCRIPT_DIR%'; if ($path -match '[^\x00-\x7F]') { exit 1 } else { exit 0 }" >nul 2>&1
    if errorlevel 1 (
        set MINICONDA_ROOT=%~d0\Miniconda3
    )
)

REM Sistemden Conda yolunu almaya calis
if defined CONDA_EXE (
    for %%p in ("%CONDA_EXE%\..\..") do set "MINICONDA_ROOT=%%~fp"
)
if not defined MINICONDA_ROOT (
    for /f "delims=" %%i in ('conda info --base 2^>nul') do set "MINICONDA_ROOT=%%i"
)

REM Conda'yi basla (conda komutunun kullanilabilir oldugunu dogrula)
echo Conda baslatiliyor...
if exist "%MINICONDA_ROOT%\Scripts\activate.bat" (
    call "%MINICONDA_ROOT%\Scripts\activate.bat"
    echo [OK] Conda baslatildi
    echo Konum: %MINICONDA_ROOT%
) else (
    REM Sistem conda'sini kullanmaya calis
    where conda >nul 2>&1
    if !ERRORLEVEL! neq 0 (
        echo [HATA] Conda bulunamadi
        echo Conda'nin dogru kuruldugunu dogrulayin
        echo.
        echo Beklenen konum: %MINICONDA_ROOT%
        pause
        exit /b 1
    )
    echo [OK] Sistem Conda kullaniliyor
)
echo.

REM Adlandirilmis ortam kullan (Turkce yol sorunlarini onle)
set CONDA_ENV_NAME=manga-env
set CONDA_ENV_EXISTS=0

REM Conda hizmet sozlesmesini onceden kabul et (interaktif istemi onle)
call conda config --set channel_priority flexible >nul 2>&1
call conda tos accept >nul 2>&1

REM Ortamin var olup olmadigini kontrol et
echo Ortam kontrol ediliyor...
REM Satirbasi eslesmesi icin /B secenegi kullan, yol icindeki metni yanlis eslememek icin
call conda info --envs 2>nul | findstr /B /C:"%CONDA_ENV_NAME%" >nul 2>nul
if %ERRORLEVEL% == 0 goto :env_exists
REM Ortam yok, yeni ortam olustur
echo [BILGI] Ortam tespit edilemedi, yeni ortam olusturulacak
goto :create_new_env

:env_exists
set CONDA_ENV_EXISTS=1
echo [OK] Mevcut conda ortami tespit edildi: %CONDA_ENV_NAME%
echo.
echo Mevcut Conda ortami tespit edildi, yeniden olusturulsun mu?
echo [1] Mevcut ortami kullan (hizli)
echo [2] Ortami yeniden olustur (temiz kurulum)
echo.
set /p recreate_env="Seciniz (1/2, varsayilan 1): "

if "!recreate_env!"=="2" goto :delete_and_recreate

REM Kullanici mevcut ortami kullanmayi secti
echo.
echo [OK] Mevcut ortam kullaniliyor
goto :activate_env

:delete_and_recreate
echo.
echo Mevcut ortam siliniyor...
call conda deactivate >nul 2>&1
call conda env remove -n "%CONDA_ENV_NAME%" -y >nul 2>&1
set CONDA_ENV_EXISTS=0
echo [OK] Ortam silindi
echo.
REM Silindikten sonra yeni ortam olusturmaya devam et

REM Yeni ortam olustur
:create_new_env
echo.
echo [BILGI] Conda ortami olusturuluyor...
echo Ortam adi: %CONDA_ENV_NAME%
echo Python surumu: 3.12
echo.

REM Eski ortam kayit bilgilerini temizle
echo Conda ortam listesi temizleniyor...
call conda env remove -n "%CONDA_ENV_NAME%" -y >nul 2>&1

REM Kayitli olmayan bozuk ortam dizinlerini temizle
REM Conda'nin envs dizinini al
for /f "delims=" %%i in ('conda info --base 2^>nul') do set "CONDA_BASE=%%i"
if exist "%CONDA_BASE%\envs\%CONDA_ENV_NAME%" (
    echo Kayitsiz ortam dizini bulundu, temizleniyor...
    rmdir /s /q "%CONDA_BASE%\envs\%CONDA_ENV_NAME%" 2>nul
)

REM Conda hizmet sozlesmesini kabul et (interaktif istemi onle)
call conda config --set channel_priority flexible >nul 2>&1
call conda tos accept >nul 2>&1

REM Bozuk paket onbelleklerini temizle
echo Paket onbellegi temizleniyor...
call conda clean --all -y >nul 2>&1

REM Adlandirilmis ortami olustur
echo Ortam olusturuluyor: %CONDA_ENV_NAME%
call conda create -n "%CONDA_ENV_NAME%" python=3.12.* -y
if !ERRORLEVEL! neq 0 goto :create_env_failed
echo [OK] Conda ortami olusturuldu
goto :activate_env

:create_env_failed
echo.
echo [HATA] Conda ortami olusturulamadi
echo.
echo Kanal yapilandirmasi veya onbellek sorunu olabilir
echo.
echo Otomatik duzeltme denensin mi?
echo [1] Evet - Kanal yapilandirmasini sifirla ve yeniden dene
echo [2] Hayir - Kurulumu iptal et
echo.
set /p fix_choice="Seciniz (1/2, varsayilan 1): "

if "!fix_choice!"=="2" (
    echo Kurulum iptal edildi
    pause
    exit /b 1
)

echo.
echo Duzeltme deneniyor...
echo 1. Kanal yapilandirmasi sifirlaniyor...
call conda config --remove-key channels >nul 2>&1
echo 2. Indeks onbellegi temizleniyor...
call conda clean --index-cache -y >nul 2>&1
echo 3. Ortam olusturma yeniden deneniyor...
echo.
call conda create -n "%CONDA_ENV_NAME%" python=3.12.* -y
if !ERRORLEVEL! neq 0 goto :create_env_failed_final

echo [OK] Duzeltme basarili!
goto :activate_env

:create_env_failed_final
echo [HATA] Duzeltme basarisiz, ortam olusturma hala basarisiz
echo.
echo Olasi cozumler:
echo 1. Manuel calistirin: conda update -n base conda
echo 2. Miniconda'yi yeniden kurun
pause
exit /b 1

:activate_env
echo.
echo Ortam etkinlestiriliyor...

REM Conda'nin baslatildigini dogrula
if not exist "%MINICONDA_ROOT%\Scripts\activate.bat" goto :try_activate_s1
call "%MINICONDA_ROOT%\Scripts\activate.bat"

:try_activate_s1
REM Yontem 1: conda activate adlandirilmis ortam
call conda activate "%CONDA_ENV_NAME%" 2>nul && echo [OK] Adlandirilmis ortam etkinlestirildi: %CONDA_ENV_NAME% && goto :env_activated

REM Yontem 2: activate.bat ile adlandirilmis ortami etkinlestir
echo [BILGI] Yedek etkinlestirme yontemi deneniyor...
if not exist "%MINICONDA_ROOT%\Scripts\activate.bat" goto :try_manual_path_s1
call "%MINICONDA_ROOT%\Scripts\activate.bat" "%CONDA_ENV_NAME%" 2>nul && echo [OK] Adlandirilmis ortam etkinlestirildi: %CONDA_ENV_NAME% && goto :env_activated

:try_manual_path_s1
REM Yontem 3: Ortam yolunu al ve PATH'i manuel ayarla
for /f "tokens=2" %%i in ('conda info --envs 2^>nul ^| findstr /B /C:"%CONDA_ENV_NAME%"') do set "ENV_PATH=%%i"
if not defined ENV_PATH goto :activate_failed_s1
if not exist "!ENV_PATH!\python.exe" goto :activate_failed_s1
echo [BILGI] Manuel PATH etkinlestirme yontemi kullaniliyor...
set "PATH=!ENV_PATH!;!ENV_PATH!\Library\mingw-w64\bin;!ENV_PATH!\Library\usr\bin;!ENV_PATH!\Library\bin;!ENV_PATH!\Scripts;!ENV_PATH!\bin;%PATH%"
set "CONDA_PREFIX=!ENV_PATH!"
set "CONDA_DEFAULT_ENV=%CONDA_ENV_NAME%"
echo [OK] Ortam etkinlestirildi: %CONDA_ENV_NAME%
goto :env_activated

:activate_failed_s1
REM Tum etkinlestirme yontemleri basarisiz, kullaniciya sor
echo.
echo [UYARI] Ortam etkinlestirilemedi: %CONDA_ENV_NAME%
echo.
echo Olasi nedenler:
echo   1. Conda duzgun baslatilmamis
echo   2. Ortam bozulmus
echo.
echo Seciniz:
echo [1] Ortami yeniden olustur (mevcut ortami sil)
echo [2] Cik, manuel duzelt
echo.
set /p activate_choice="Seciniz (1/2): "
if "!activate_choice!"=="2" goto :activate_exit_s1

echo.
echo Ortam siliniyor...
call conda deactivate >nul 2>&1
call conda env remove -n "%CONDA_ENV_NAME%" -y 2>nul

REM Silme basarisiz mi kontrol et
call conda info --envs 2>nul | findstr /B /C:"%CONDA_ENV_NAME%" >nul 2>&1 && goto :delete_failed_s1

echo [OK] Ortam silindi
echo.
echo Ortam yeniden olusturuluyor...
echo.
goto :create_new_env

:activate_exit_s1
echo.
echo Onerilen adimlar:
echo   1. Bu pencereyi kapat, yeni komut istemi ac
echo   2. Calistirin: conda init cmd.exe
echo   3. Bu betigi yeniden calistirin
pause
exit /b 1

:delete_failed_s1
echo [HATA] Ortam silinemedi, kullanimda olabilir
echo Ilgili tum programlari kapatip yeniden deneyin
pause
exit /b 1

:env_activated

echo pip guncelleniyor...
python -m pip install --upgrade pip >nul 2>&1

echo Temel bagimliliklar yukleniyor...
python -m pip install packaging setuptools wheel >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [UYARI] Temel bagimlilik kurulumu basarisiz, devam ediliyor...
)

echo GPU destegi kontrol ediliyor...
echo.

REM Bagimlilik kurulumu icin projenin launch.py dosyasini cagir
python packaging\launch.py --install-deps-only

if %ERRORLEVEL% neq 0 (
    echo.
    echo [HATA] Bagimlilik kurulumu basarisiz
    echo.
    echo Daha sonra manuel olarak calistirilabilir:
    echo   Adim4-GuncellemeVeBakim.bat
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] Bagimlilik kurulumu tamamlandi

REM ===== Adim 5: Tamamlandi =====
echo.
echo [5/5] Kurulum tamamlandi!
echo ========================================
echo.
echo [OK] Tum adimlar tamamlandi!
echo.
echo Kurulum konumu: %SCRIPT_DIR%
echo.
echo Sonraki adim:
echo   Adim2-QtArayuzuBaslat.bat dosyasini cift tiklayin (Qt surumu)
echo   veya Adim3-GuncellemeKontrolVeBaslat.bat (otomatik guncelleme kontrolu)
echo.
echo Duzenli guncelleme icin:
echo   Adim4-GuncellemeVeBakim.bat dosyasini cift tiklayin
echo.
pause

REM pip onbellegini temizleme secenegi sun
echo.
echo ========================================
echo Disk Alani Optimizasyonu
echo ========================================
echo.
echo pip onbellek dosyalari buyuk alan kapliyor olabilir
echo Onbellek temizlemek kurulu paketleri etkilemez
echo.
set /p clean_cache="pip onbellegi temizlensin mi? (e/h, varsayilan h): "
if /i "%clean_cache%"=="e" (
    echo.
    echo pip onbellegi temizleniyor...
    python -m pip cache purge >nul 2>&1
    if errorlevel 1 (
        echo [UYARI] Onbellek temizleme basarisiz, yetki sorunu olabilir
    ) else (
        echo [OK] Onbellek temizlendi
    )
) else (
    echo [BILGI] Onbellek temizleme atlandi
)

REM Hemen calistirma secenegi sun
echo.
set /p run_now="Hemen calistirilsin mi? (e/h): "
if /i "%run_now%"=="e" (
    echo.
    echo Baslatiliyor...
    start Adim2-QtArayuzuBaslat.bat
)

echo.
echo Kurulum islemi tamamlandi
pause

:install_cancelled
echo.
echo Kurulum iptal edildi
pause
exit /b 1