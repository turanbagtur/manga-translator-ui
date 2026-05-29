#!/bin/bash

# ==================== macOS Qt Arayüzü Başlatma Betiği ====================
# Apple Silicon Mac için tasarlanmıştır
# Windows'taki "Adim2-QtArayuzuBaslat.bat" dosyasına karşılık gelir
# =====================================================================

# Çalışma dizini olarak betiğin bulunduğu dizini kullan
cd "$(dirname "$0")"
SCRIPT_DIR="$(pwd)"

# Yapılandırma
CONDA_ENV_NAME="manga-env"
MINICONDA_DIR="$SCRIPT_DIR/Miniforge3"

# Renk tanımları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=============================================="
echo "  Manga Çevirici - Qt Arayüzü Başlatılıyor"
echo "=============================================="
echo ""

# Conda'yı bul ve başlat
init_conda() {
    # Önce yerel Miniconda/Miniforge kontrol et
    if [ -f "$MINICONDA_DIR/bin/conda" ]; then
        export PATH="$MINICONDA_DIR/bin:$PATH"
        eval "$("$MINICONDA_DIR/bin/conda" shell.bash hook)"
        return 0
    fi
    
    # Sistem Conda'sını kontrol et
    if command -v conda &> /dev/null; then
        eval "$(conda shell.bash hook)"
        return 0
    fi
    
    return 1
}

# Conda'yı başlat
if ! init_conda; then
    echo -e "${RED}[HATA] Conda bulunamadı${NC}"
    echo "   Lütfen önce ./macOS_1_IlkKurulum.sh dosyasını çalıştırarak kurun"
    exit 1
fi

# Ortamı etkinleştir
if ! conda activate "$CONDA_ENV_NAME" 2>/dev/null; then
    echo -e "${RED}[HATA] Ortam bulunamadı: $CONDA_ENV_NAME${NC}"
    echo "   Lütfen önce ./macOS_1_IlkKurulum.sh dosyasını çalıştırarak kurun"
    exit 1
fi
echo -e "${GREEN}[OK] Ortam etkinleştirildi: $CONDA_ENV_NAME${NC}"

# PyQt6 kontrolü
if ! python -c "import PyQt6" 2>/dev/null; then
    echo -e "${RED}[HATA] PyQt6 kurulu değil${NC}"
    echo "   Bağımlılıkları kurmak için ./macOS_1_IlkKurulum.sh dosyasını çalıştırın"
    exit 1
fi

# Qt arayüzünü başlat
echo ""
echo -e "${GREEN}[*] Qt arayüzü başlatılıyor...${NC}"
echo ""
python desktop_qt_ui/main.py