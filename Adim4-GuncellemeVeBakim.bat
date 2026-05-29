@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

REM PYTHONUTF8=1 ayarla - conda kodlama hatalarini onle
set "PYTHONUTF8=1"

REM Yonetici modunda %CD%'nin system32'ye donmesi sorununu duzelt
cd /d "%~dp0"
set "SCRIPT_DIR=%~dp0"
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

REM Conda ortamini kontrol et (adlandirilmis ve yol ortamlarini destekler)
set CONDA_ENV_NAME=manga-env
set CONDA_ENV_PATH=%SCRIPT_DIR%\conda_env
set MINICONDA_ROOT=%SCRIPT_DIR%\Miniconda3

REM Yolun ASCII olmayan karakter icerip icermedigini kontrol et
set "TEMP_CHECK_PATH=%SCRIPT_DIR%"
powershell -Command "$path = '%TEMP_CHECK_PATH%'; if ($path -match '[^\x00-\x7F]') { exit 1 } else { exit 0 }" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    REM Yol ASCII olmayan karakter iceriyor, disk kokunde Miniconda kullan
    set MINICONDA_ROOT=%~d0\Miniconda3
)

REM Once sistem conda'sini kontrol et
where conda >nul 2>&1
if %ERRORLEVEL% neq 0 goto :check_local_conda_s4

REM Sistem conda tespit edildi, gercek yolu al
REM Yontem 1: CONDA_EXE ortam degiskeninden al (en guvenilir)
if defined CONDA_EXE (
    for %%p in ("%CONDA_EXE%\..\..") do set "MINICONDA_ROOT=%%~fp"
)

REM Yontem 2: CONDA_PREFIX ortam degiskeninden al
if "!MINICONDA_ROOT!"=="" (
    if defined CONDA_PREFIX (
        set "MINICONDA_ROOT=%CONDA_PREFIX%"
    )
)

REM Yontem 3: conda info --base kullan
if "!MINICONDA_ROOT!"=="" (
    for /f "delims=" %%i in ('conda info --base 2^>nul') do (
        set "TEMP_PATH=%%i"
        if exist "!TEMP_PATH!\Scripts\conda.exe" (
            set "MINICONDA_ROOT=%%i"
        )
    )
)

REM Yontem 4: where conda ciktisini ayristir
if "!MINICONDA_ROOT!"=="" (
    for /f "delims=" %%i in ('where conda 2^>nul') do (
        if "!MINICONDA_ROOT!"=="" (
            if "%%~xi"==".exe" (
                for %%p in ("%%~dpi..") do set "MINICONDA_ROOT=%%~fp"
            ) else if "%%~xi"==".bat" (
                for %%p in ("%%~dpi..\..") do set "MINICONDA_ROOT=%%~fp"
            )
        )
    )
)

goto :check_env_s4

:check_local_conda_s4
REM Yerel Miniconda kontrol et (once betik dizini)
if exist "%SCRIPT_DIR%\Miniconda3\Scripts\conda.exe" (
    set MINICONDA_ROOT=%SCRIPT_DIR%\Miniconda3
    echo [BILGI] Yerel Miniconda tespit edildi: %MINICONDA_ROOT%
    call "%MINICONDA_ROOT%\Scripts\activate.bat"
    goto :check_env_s4
)

REM Disk koku dizinini kontrol et
if exist "%~d0\Miniconda3\Scripts\conda.exe" (
    set MINICONDA_ROOT=%~d0\Miniconda3
    echo [BILGI] Yerel Miniconda tespit edildi: %MINICONDA_ROOT%
    call "%MINICONDA_ROOT%\Scripts\activate.bat"
    goto :check_env_s4
)

echo [HATA] Conda tespit edilemedi
echo Lutfen once Adim1-IlkKurulum.bat dosyasini calistirarak Miniconda'yi kurun
pause
exit /b 1

:check_env_s4

REM Ortamin var olup olmadigini kontrol et (adlandirilmis ortam oncelikli)
REM Satirbasi eslesmesi icin /B secenegi kullan
call conda info --envs 2>nul | findstr /B /C:"%CONDA_ENV_NAME%" >nul 2>&1
if %ERRORLEVEL% == 0 (
    echo [BILGI] Adlandirilmis ortam tespit edildi: %CONDA_ENV_NAME%
    goto :env_check_ok_s4
)

REM Eski surum yol ortamini kontrol et
if exist "%CONDA_ENV_PATH%\python.exe" (
    echo [BILGI] Yol ortami tespit edildi (eski surum)
    goto :env_check_ok_s4
)

REM Hicbir ortam yok
echo [HATA] Conda ortami tespit edilemedi
echo Lutfen once Adim1-IlkKurulum.bat dosyasini calistirarak ortami olusturun
pause
exit /b 1

:env_check_ok_s4

REM Conda'nin baslatildigini dogrula
if not exist "%MINICONDA_ROOT%\Scripts\activate.bat" goto :try_activate_s4
call "%MINICONDA_ROOT%\Scripts\activate.bat"

:try_activate_s4
REM Yontem 1: conda activate adlandirilmis ortam
call conda activate "%CONDA_ENV_NAME%" 2>nul && goto :activated_ok_s4

REM Yontem 2: activate.bat ile adlandirilmis ortami etkinlestir
echo [BILGI] Yedek etkinlestirme yontemi deneniyor...
if not exist "%MINICONDA_ROOT%\Scripts\activate.bat" goto :try_manual_path_s4
call "%MINICONDA_ROOT%\Scripts\activate.bat" "%CONDA_ENV_NAME%" 2>nul && goto :activated_ok_s4

:try_manual_path_s4
REM Yontem 3: Ortam yolunu al ve PATH'i manuel ayarla
for /f "tokens=2" %%i in ('conda info --envs 2^>nul ^| findstr /B /C:"%CONDA_ENV_NAME%"') do set "ENV_PATH=%%i"
if not defined ENV_PATH goto :try_legacy_env_s4
if not exist "!ENV_PATH!\python.exe" goto :try_legacy_env_s4
echo [BILGI] Manuel PATH etkinlestirme yontemi kullaniliyor...
set "PATH=!ENV_PATH!;!ENV_PATH!\Library\mingw-w64\bin;!ENV_PATH!\Library\usr\bin;!ENV_PATH!\Library\bin;!ENV_PATH!\Scripts;!ENV_PATH!\bin;%PATH%"
set "CONDA_PREFIX=!ENV_PATH!"
set "CONDA_DEFAULT_ENV=%CONDA_ENV_NAME%"
echo [BILGI] Ortam etkinlestirildi: %CONDA_ENV_NAME%
goto :activated_ok_s4

:try_legacy_env_s4
REM Yontem 4: Eski surum yol ortami
if not exist "%CONDA_ENV_PATH%\python.exe" goto :activate_failed_s4
echo [BILGI] Yol ortami etkinlestiriliyor (eski surum)...
echo [BILGI] Manuel PATH etkinlestirme yontemi kullaniliyor...
set "PATH=%CONDA_ENV_PATH%;%CONDA_ENV_PATH%\Library\mingw-w64\bin;%CONDA_ENV_PATH%\Library\usr\bin;%CONDA_ENV_PATH%\Library\bin;%CONDA_ENV_PATH%\Scripts;%CONDA_ENV_PATH%\bin;%PATH%"
set "CONDA_PREFIX=%CONDA_ENV_PATH%"
set "CONDA_DEFAULT_ENV=%CONDA_ENV_PATH%"
goto :activated_ok_s4

:activate_failed_s4
echo [HATA] Ortam etkinlestirilemedi
echo Deneyin: Yeni komut istemi acp, conda init cmd.exe calistirin, sonra tekrar deneyin
pause
exit /b 1

:activated_ok_s4

REM Tasinalir Git'i PATH'e ekle
if exist "%SCRIPT_DIR%\PortableGit\cmd\git.exe" set "PATH=%SCRIPT_DIR%\PortableGit\cmd;%PATH%"

REM Python bakim menusunu cagir
python packaging\launch.py --maintenance
pause