#!/bin/bash

# ==================== macOS İlk Kurulum Betiği ====================
# Apple Silicon Mac için tasarlanmıştır
# Windows'taki "Adim1-IlkKurulum.bat" dosyasına karşılık gelir
# Python ortamı yönetimi için Miniconda/Miniforge kullanır
# =====================================================================

set -e

# Çalışma dizini olarak betiğin bulunduğu dizini kullan
cd "$(dirname "$0")"
SCRIPT_DIR="$(pwd)"

# Yapılandırma
CONDA_ENV_NAME="manga-env"
MINICONDA_DIR="$SCRIPT_DIR/Miniforge3" # Miniforge3 dizinini kullan
# Miniforge kullan (varsayılan olarak conda-forge kullanır, Hizmet Şartları sorununu çözer)
MINICONDA_URL="https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh"
PYTHON_VERSION="3.12"

# Renk tanımları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "=============================================="
echo "  Manga Çevirici - İlk Kurulum"
echo "=============================================="
echo ""

# Apple Silicon kontrolü
check_apple_silicon() {
    if [[ $(uname -m) != "arm64" ]]; then
        echo -e "${YELLOW}[UYARI] Bu betik Apple Silicon için tasarlanmıştır${NC}"
        echo "   Algılanan mimari: $(uname -m)"
        # Intel sürümü Miniforge kullan
        MINICONDA_URL="https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-x86_64.sh"
        read -p "Devam edilsin mi? (e/h) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Ee]$ ]]; then
            exit 1
        fi
    else
        echo -e "${GREEN}[OK] Apple Silicon (arm64) algılandı${NC}"
    fi
}

# Xcode Komut Satırı Araçlarını kontrol et
check_xcode_tools() {
    echo ""
    echo -e "${BLUE}[*] Xcode Komut Satırı Araçları kontrol ediliyor...${NC}"
    
    if xcode-select -p &> /dev/null; then
        echo -e "${GREEN}[OK] Xcode Komut Satırı Araçları kurulu${NC}"
    else
        echo -e "${YELLOW}[UYARI] Xcode Komut Satırı Araçları kurulması gerekiyor${NC}"
        read -p "Şimdi kurulsun mu? (e/h) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Ee]$ ]]; then
            xcode-select --install
            echo "Kurulum tamamlandıktan sonra bu betiği yeniden çalıştırın"
            exit 0
        fi
    fi
}

# Git kontrolü
check_git() {
    echo ""
    echo -e "${BLUE}[*] Git kontrol ediliyor...${NC}"
    
    if command -v git &> /dev/null; then
        echo -e "${GREEN}[OK] Git kurulu${NC}"
        git --version
    else
        echo -e "${YELLOW}[UYARI] Git algılanamadı${NC}"
        echo ""
        echo "Git genellikle Xcode Komut Satırı Araçları ile birlikte gelir"
        echo "Xcode Komut Satırı Araçları kurulu olmasına rağmen Git algılanamıyorsa,"
        echo "şu yollarla kurabilirsiniz:"
        echo ""
        echo "  1. Homebrew kullanın: brew install git"
        echo "  2. Xcode Komut Satırı Araçları'nı yeniden kurun: xcode-select --install"
        echo ""
        read -p "Devam edilsin mi? (e/h) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Ee]$ ]]; then
            exit 1
        fi
    fi
}

# Kod deposunu klonla veya güncelle
setup_repository() {
    echo ""
    echo -e "${BLUE}[*] Kod deposu kontrol ediliyor...${NC}"
    
    # Kod dosyalarının varlığını kontrol et (sıkıştırılmış dosyadan açılmış veya klonlanmış)
    if [ -d "manga_translator" ] && [ -d "desktop_qt_ui" ] && [ -f "packaging/VERSION" ]; then
        if [ -d ".git" ]; then
            echo -e "${GREEN}[OK] Git deposu algılandı${NC}"
            
            # Mevcut depo adresini al
            CURRENT_REPO=$(git config --get remote.origin.url 2>/dev/null || echo "")
            
            if [ -n "$CURRENT_REPO" ]; then
                echo "Mevcut depo: $CURRENT_REPO"
                echo ""
                read -p "En son sürüme güncellensin mi? (e/h) " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Ee]$ ]]; then
                    echo -e "${BLUE}[*] Uzak güncellemeler getiriliyor...${NC}"
                    git fetch origin
                    echo -e "${BLUE}[*] Uzak dala zorla senkronize ediliyor...${NC}"
                    git reset --hard origin/main
                    echo -e "${GREEN}[OK] Kod güncellendi${NC}"
                    
                    # Windows dosyalarını temizle
                    rm -f "Adim1-IlkKurulum.bat" "Adim2-QtArayuzuBaslat.bat" "Adim3-GuncellemeKontrolVeBaslat.bat" "Adim4-GuncellemeVeBakim.bat" 2>/dev/null
                    rm -f ".gitattributes" ".gitignore" "LICENSE.txt" 2>/dev/null
                    echo -e "${GREEN}[OK] Windows betikleri ve Git yapılandırma dosyaları temizlendi${NC}"
                fi
            fi
        else
            echo -e "${GREEN}[OK] Kod dosyaları algılandı (sıkıştırılmış dosyadan açılmış)${NC}"
            echo ""
            read -p "Sonraki güncellemeler için Git deposu başlatılsın mı? (e/h) " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Ee]$ ]]; then
                git init
                
                # Depo kaynağını seç
                echo ""
                echo "Depo kaynağı seçin:"
                echo "  [1] GitHub Resmi"
                echo "  [2] gh-proxy.com Aynası (Çin için önerilen)"
                read -p "Seçin (1/2, varsayılan 1): " repo_choice
                
                if [ "$repo_choice" = "2" ]; then
                    REPO_URL="https://gh-proxy.com/https://github.com/hgmzhn/manga-translator-ui.git"
                else
                    REPO_URL="https://github.com/hgmzhn/manga-translator-ui.git"
                fi
                
                git remote add origin "$REPO_URL"
                git fetch origin
                echo -e "${GREEN}[OK] Git deposu başlatıldı${NC}"
            fi
        fi
        return 0
    fi
    
    # Kod klonlanması gerekiyor
    echo -e "${YELLOW}[*] Kod algılanamadı, klonlanıyor...${NC}"
    echo ""
    echo "Depo kaynağı seçin:"
    echo "  [1] GitHub Resmi"
    echo "  [2] gh-proxy.com Aynası (Çin için önerilen)"
    read -p "Seçin (1/2, varsayılan 1): " repo_choice
    
    if [ "$repo_choice" = "2" ]; then
        REPO_URL="https://gh-proxy.com/https://github.com/hgmzhn/manga-translator-ui.git"
        echo "Kullanılan: gh-proxy.com aynası"
    else
        REPO_URL="https://github.com/hgmzhn/manga-translator-ui.git"
        echo "Kullanılan: GitHub resmi"
    fi
    
    echo ""
    echo -e "${BLUE}[*] Kod geçici dizine klonlanıyor...${NC}"
    TEMP_DIR="manga_translator_temp_$$"
    
    if git clone "$REPO_URL" "$TEMP_DIR"; then
        echo -e "${GREEN}[OK] Klonlama tamamlandı${NC}"
        
        # Dosyaları kopyala
        echo -e "${BLUE}[*] Dosyalar kopyalanıyor...${NC}"
        cp -r "$TEMP_DIR"/* "$SCRIPT_DIR/" 2>/dev/null || true
        cp -r "$TEMP_DIR"/.git "$SCRIPT_DIR/" 2>/dev/null || true
        cp "$TEMP_DIR"/.gitignore "$SCRIPT_DIR/" 2>/dev/null || true
        
        # Geçici dizini temizle
        rm -rf "$TEMP_DIR"
        
        # Windows dosyalarını temizle
        rm -f "Adim1-IlkKurulum.bat" "Adim2-QtArayuzuBaslat.bat" "Adim3-GuncellemeKontrolVeBaslat.bat" "Adim4-GuncellemeVeBakim.bat" 2>/dev/null
        rm -f ".gitattributes" ".gitignore" "LICENSE.txt" 2>/dev/null
        
        echo -e "${GREEN}[OK] Kod klonlama tamamlandı${NC}"
    else
        echo -e "${RED}[HATA] Klonlama başarısız${NC}"
        rm -rf "$TEMP_DIR" 2>/dev/null
        exit 1
    fi
}

# Miniforge kur veya algıla
setup_miniconda() {
    echo ""
    echo -e "${BLUE}[*] Conda ortamı kontrol ediliyor...${NC}"
    
    # Yerel Miniconda/Miniforge kontrol et
    if [ -f "$MINICONDA_DIR/bin/conda" ]; then
        echo -e "${GREEN}[OK] Yerel Conda algılandı: $MINICONDA_DIR${NC}"
        # TOS kabul et (varsa)
        "$MINICONDA_DIR/bin/conda" config --set channel_priority flexible 2>/dev/null || true
        return 0
    fi
    
    # Sistem Conda'sını kontrol et
    if command -v conda &> /dev/null; then
        SYSTEM_CONDA=$(which conda)
        echo -e "${GREEN}[OK] Sistem Conda'sı algılandı: $SYSTEM_CONDA${NC}"
        # Sistem Conda'sını kullan
        MINICONDA_DIR="$(dirname "$(dirname "$SYSTEM_CONDA")")"
        return 0
    fi
    
    # Miniforge kurulması gerekiyor
    echo -e "${YELLOW}[*] Conda algılanamadı, Miniforge indiriliyor...${NC}"
    echo -e "${YELLOW}    Miniforge, topluluk tarafından sürdürülen bir Conda dağıtımıdır${NC}"
    
    INSTALLER_PATH="$SCRIPT_DIR/miniforge_installer.sh"
    
    # İndir
    echo -e "${BLUE}[*] Miniforge indiriliyor...${NC}"
    curl -fL -o "$INSTALLER_PATH" "$MINICONDA_URL" || {
        echo -e "${RED}[HATA] Miniforge indirme başarısız${NC}"
        exit 1
    }
    
    # Kur
    echo -e "${BLUE}[*] Miniforge şu konuma kuruluyor: $MINICONDA_DIR...${NC}"
    bash "$INSTALLER_PATH" -b -p "$MINICONDA_DIR"
    
    # Kurulum paketini temizle
    rm -f "$INSTALLER_PATH"
    
    echo -e "${GREEN}[OK] Miniforge kurulumu tamamlandı${NC}"
}

# Conda'yı başlat
init_conda() {
    echo ""
    echo -e "${BLUE}[*] Conda başlatılıyor...${NC}"
    
    # PATH ayarla
    export PATH="$MINICONDA_DIR/bin:$PATH"
    
    # Conda Shell'i başlat
    eval "$("$MINICONDA_DIR/bin/conda" shell.bash hook)"
    
    # conda-forge kullan (yeni kurulum ise Miniforge zaten bunu varsayılan kullanır)
    conda config --add channels conda-forge 2>/dev/null || true
    conda config --set channel_priority flexible 2>/dev/null || true
    
    echo -e "${GREEN}[OK] Conda başlatıldı${NC}"
}

# Ortam oluştur veya etkinleştir
setup_environment() {
    echo ""
    echo -e "${BLUE}[*] Conda ortamı ayarlanıyor...${NC}"
    
    # Ortamın var olup olmadığını kontrol et
    if conda env list | grep -qE "^${CONDA_ENV_NAME}[[:space:]]"; then
        echo -e "${GREEN}[OK] Mevcut ortam algılandı: $CONDA_ENV_NAME${NC}"
        read -p "Silinip yeniden oluşturulsun mu? (e/h) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Ee]$ ]]; then
            conda env remove -n "$CONDA_ENV_NAME" -y
            conda create -n "$CONDA_ENV_NAME" python=$PYTHON_VERSION -y
            echo -e "${GREEN}[OK] Ortam yeniden oluşturuldu${NC}"
        fi
    else
        echo -e "${BLUE}[*] Yeni ortam oluşturuluyor: $CONDA_ENV_NAME (Python $PYTHON_VERSION)${NC}"
        conda create -n "$CONDA_ENV_NAME" python=$PYTHON_VERSION -y
        echo -e "${GREEN}[OK] Ortam oluşturuldu${NC}"
    fi
    
    # Ortamı etkinleştir
    conda activate "$CONDA_ENV_NAME"
    echo -e "${GREEN}[OK] Ortam etkinleştirildi: $CONDA_ENV_NAME${NC}"
}

# Bağımlılıkları kur
install_dependencies() {
    echo ""
    echo -e "${BLUE}[*] Bağımlılıklar kuruluyor...${NC}"
    
    # requirements_metal.txt dosyasının varlığını kontrol et
    if [ ! -f "requirements_metal.txt" ]; then
        echo -e "${RED}[HATA] requirements_metal.txt bulunamadı${NC}"
        exit 1
    fi
    
    # PyTorch kur (MPS sürümü)
    echo ""
    echo -e "${BLUE}[*] PyTorch kuruluyor (MPS sürümü)...${NC}"
    pip install torch torchvision torchaudio
    
    # Diğer bağımlılıkları kur
    echo ""
    echo -e "${BLUE}[*] Diğer bağımlılıklar kuruluyor...${NC}"
    pip install -r requirements_metal.txt --ignore-installed torch torchvision torchaudio
}

# Kurulumu doğrula
verify_installation() {
    echo ""
    echo -e "${BLUE}[*] Kurulum doğrulanıyor...${NC}"
    
    python -c "
import sys
print(f'Python: {sys.version}')
print()

import torch
print(f'PyTorch: {torch.__version__}')
print(f'MPS Kullanılabilir: {torch.backends.mps.is_available()}')
print(f'MPS Derlenmiş: {torch.backends.mps.is_built()}')
print()

if torch.backends.mps.is_available():
    device = torch.device('mps')
    x = torch.randn(2, 3, device=device)
    y = torch.randn(3, 4, device=device)
    z = torch.mm(x, y)
    print('[OK] MPS matris işlemi testi başarılı')
else:
    print('[UYARI] MPS kullanılamıyor, CPU kullanılacak')
print()

try:
    from manga_translator import MangaTranslator
    print('[OK] manga_translator modülü başarıyla içe aktarıldı')
except Exception as e:
    print(f'[UYARI] manga_translator modülü içe aktarılamadı: {e}')
"
}

# Ana akış
main() {
    check_apple_silicon
    check_xcode_tools
    check_git
    setup_repository
    setup_miniconda
    init_conda
    setup_environment
    install_dependencies
    verify_installation
    
    echo ""
    echo "=============================================="
    echo -e "${GREEN}[OK] Kurulum tamamlandı!${NC}"
    echo "=============================================="
    echo ""
    echo "Kullanım:"
    echo ""
    echo "  Başlatma betiğini doğrudan çalıştırın:"
    echo "    ./macOS_2_QtArayuzuBaslat.sh"
    echo ""
    echo "  Veya ortamı manuel etkinleştirip çalıştırın:"
    echo "    source $MINICONDA_DIR/bin/activate $CONDA_ENV_NAME"
    echo "    python desktop_qt_ui/main.py"
    echo ""
}

# Çalıştır
main