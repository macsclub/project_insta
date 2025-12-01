"""
Konfigürasyon dosyası - Tüm sabit değerler burada tutulur
Environment variable desteği ile Docker uyumlu
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Menü URL'si
MENU_URL = os.environ.get('MENU_URL', "https://yemekhane.ogu.edu.tr/")

# Görsel ayarları
IMAGE_WIDTH = int(os.environ.get('IMAGE_WIDTH', 900))
IMAGE_HEIGHT = int(os.environ.get('IMAGE_HEIGHT', 1600))

# Asset ve Output dizinleri (Docker uyumlu)
ASSETS_DIR = os.environ.get('ASSETS_DIR', str(BASE_DIR.parent / '2_assets'))
OUTPUT_DIR = os.environ.get('OUTPUT_DIR', str(BASE_DIR.parent / '5_tests' / 'output'))

# Template dosya yolu
TEMPLATE_PATH = os.environ.get('TEMPLATE_PATH', os.path.join(ASSETS_DIR, 'kaynak_gorsel.jpg'))

# Font ayarları - Linux/Windows uyumlu
# Docker'da /usr/share/fonts altında, Windows'ta arial.ttf
def get_font_path():
    """Platform uyumlu font yolu döndürür"""
    # Önce environment variable kontrol et
    env_font = os.environ.get('FONT_PATH')
    if env_font and os.path.exists(env_font):
        return env_font
    
    # Proje içindeki font
    project_font = os.path.join(ASSETS_DIR, 'fonts', 'Roboto-Bold.ttf')
    if os.path.exists(project_font):
        return project_font
    
    # Linux fontları
    linux_fonts = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
        '/usr/share/fonts/truetype/freefont/FreeSansBold.ttf',
    ]
    for font in linux_fonts:
        if os.path.exists(font):
            return font
    
    # Windows fontları
    windows_fonts = [
        'C:/Windows/Fonts/arial.ttf',
        'C:/Windows/Fonts/segoeui.ttf',
        'arial.ttf',  # System path'te olabilir
    ]
    for font in windows_fonts:
        if os.path.exists(font):
            return font
    
    # Hiçbiri yoksa None döndür (Pillow default font kullanacak)
    return None

FONT_PATH = get_font_path()
FONT_SIZE = int(os.environ.get('FONT_SIZE', 40))
FONT_COLOR = (0, 0, 0)  # Siyah

# Metin pozisyon ayarları
TEXT_START_X = int(os.environ.get('TEXT_START_X', 100))
TEXT_START_Y = int(os.environ.get('TEXT_START_Y', 550))
LINE_SPACING = int(os.environ.get('LINE_SPACING', 55))

# API ayarları
API_BASE_URL = os.environ.get('API_BASE_URL', 'http://localhost:8000')
API_PORT = int(os.environ.get('API_PORT', 8000))

# Instagram API (Credentials'dan okunacak, burada default)
INSTAGRAM_ACCESS_TOKEN = os.environ.get('INSTAGRAM_ACCESS_TOKEN', '')
INSTAGRAM_USER_ID = os.environ.get('INSTAGRAM_USER_ID', '')
FACEBOOK_PAGE_ID = os.environ.get('FACEBOOK_PAGE_ID', '')
