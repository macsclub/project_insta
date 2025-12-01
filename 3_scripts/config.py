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

# Görsel ayarları - 2160x3840 (Instagram Story 1080x1920'nin 2x'i)
IMAGE_WIDTH = int(os.environ.get('IMAGE_WIDTH', 2160))
IMAGE_HEIGHT = int(os.environ.get('IMAGE_HEIGHT', 3840))

# Asset ve Output dizinleri (Docker uyumlu)
ASSETS_DIR = os.environ.get('ASSETS_DIR', str(BASE_DIR.parent / '2_assets'))
OUTPUT_DIR = os.environ.get('OUTPUT_DIR', str(BASE_DIR.parent / '5_tests' / 'output'))

# Template dosya yolu
TEMPLATE_PATH = os.environ.get('TEMPLATE_PATH', os.path.join(ASSETS_DIR, 'kaynak_gorsel.png'))

# Font ayarları - LeagueSpartan-SemiBold
def get_font_path():
    """Platform uyumlu font yolu döndürür"""
    # Önce environment variable kontrol et
    env_font = os.environ.get('FONT_PATH')
    if env_font and os.path.exists(env_font):
        return env_font
    
    # Proje içindeki ana font - LeagueSpartan
    project_font = os.path.join(ASSETS_DIR, 'LeagueSpartan-SemiBold.ttf')
    if os.path.exists(project_font):
        return project_font
    
    # Docker için kopyalanmış font
    docker_font = '/app/assets/LeagueSpartan-SemiBold.ttf'
    if os.path.exists(docker_font):
        return docker_font
    
    # Linux fallback fontları
    linux_fonts = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
    ]
    for font in linux_fonts:
        if os.path.exists(font):
            return font
    
    # Windows fallback
    windows_fonts = [
        'C:/Windows/Fonts/arial.ttf',
        'arial.ttf',
    ]
    for font in windows_fonts:
        if os.path.exists(font):
            return font
    
    return None

FONT_PATH = get_font_path()
# Font boyutu - 1483px genişliğindeki beyaz alan için optimize edildi
FONT_SIZE = int(os.environ.get('FONT_SIZE', 120))
FONT_COLOR = (0, 0, 0)  # Siyah

# Metin pozisyon ayarları - 2160x3840 template için
# Yazılar template'in ortasında, dikey olarak merkezlenecek
TEXT_START_X = int(os.environ.get('TEXT_START_X', 0))  # Yatay ortalama için 0
TEXT_START_Y = int(os.environ.get('TEXT_START_Y', 1600))  # Dikey başlangıç
LINE_SPACING = int(os.environ.get('LINE_SPACING', 180))  # Satır aralığı

# API ayarları
API_BASE_URL = os.environ.get('API_BASE_URL', 'http://localhost:8000')
API_PORT = int(os.environ.get('API_PORT', 8000))

# Instagram API (Credentials'dan okunacak, burada default)
INSTAGRAM_ACCESS_TOKEN = os.environ.get('INSTAGRAM_ACCESS_TOKEN', '')
INSTAGRAM_USER_ID = os.environ.get('INSTAGRAM_USER_ID', '')
FACEBOOK_PAGE_ID = os.environ.get('FACEBOOK_PAGE_ID', '')
