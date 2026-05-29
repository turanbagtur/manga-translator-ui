#!/bin/bash

# ==================== macOS Güncelleme ve Bakım ====================
# Apple Silicon Mac için tasarlanmıştır
# Windows'taki "Adim4-GuncellemeVeBakim.bat" dosyasına karşılık gelir
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
BLUE='\033[0;34m'
NC='\033[0m'

echo "=============================================="
echo "  Manga Çevirici - Güncelleme ve Bakım"
echo "=============================================="
echo ""

# Conda'yı bul ve başlat
init_conda() {
    if [ -f "$MINICONDA_DIR/bin/conda" ]; then
        export PATH="$MINICONDA_DIR/bin:$PATH"
        eval "$("$MINICONDA_DIR/bin/conda" shell.bash hook)"
        return 0
    fi
    
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

# Bakım menüsünü çalıştır
echo ""
echo -e "${BLUE}[*] Bakım menüsü başlatılıyor...${NC}"
echo ""
if [ -f "packaging/launch.py" ]; then
    python packaging/launch.py --maintenance
else
    echo -e "${RED}[HATA] Bakım betiği bulunamadı: packaging/launch.py${NC}"
    exit 1
fi