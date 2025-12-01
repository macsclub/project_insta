"""
Instagram Menü Otomasyon API
FastAPI ile REST API sunucusu
"""

import os
import sys
import base64
import requests
from datetime import datetime
from typing import Optional
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel

# Modülleri import et
from menu_scraper import MenuScraper
from text_formatter import TextFormatter
from image_generator import ImageGenerator

# ============================================================
# CONFIGURATION
# ============================================================

# Base paths - Docker ve lokal uyumlu
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = os.environ.get('ASSETS_DIR', str(BASE_DIR.parent / '2_assets'))
OUTPUT_DIR = os.environ.get('OUTPUT_DIR', str(BASE_DIR.parent / '5_tests' / 'output'))

# API Base URL - Instagram API için public URL
# Docker/VPS'te bu değişkenin doğru ayarlanması gerekir
API_BASE_URL = os.environ.get('API_BASE_URL', 'http://localhost:8000')

# ImgBB API Key (Ücretsiz: https://api.imgbb.com/)
IMGBB_API_KEY = os.environ.get('IMGBB_API_KEY', '')

# Output dizinini oluştur
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="Instagram Menü Otomasyon API",
    description="MACS Kulübü - Yemekhane menüsü Instagram story otomasyonu",
    version="1.0.0"
)

# Static files - oluşturulan görselleri public olarak sun
# /static/images/story.png şeklinde erişilebilir olacak
app.mount("/static", StaticFiles(directory=OUTPUT_DIR), name="static")

# ============================================================
# MODELS
# ============================================================

class MenuResponse(BaseModel):
    success: bool
    tarih: Optional[str] = None
    yemekler: Optional[list] = None
    message: str

class StoryResponse(BaseModel):
    success: bool
    image_url: Optional[str] = None
    image_path: Optional[str] = None
    tarih: Optional[str] = None
    timestamp: str
    message: str

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str

# ============================================================
# ENDPOINTS
# ============================================================

@app.get("/", response_model=HealthResponse)
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    API sağlık kontrolü
    n8n bu endpoint ile API'nin çalışıp çalışmadığını kontrol edebilir
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )


@app.get("/api/menu", response_model=MenuResponse)
async def get_menu():
    """
    Günün menüsünü JSON olarak döndürür
    Sadece menü verisi, görsel oluşturmaz
    """
    try:
        scraper = MenuScraper()
        menu_data = scraper.get_todays_menu()
        
        if not menu_data:
            return MenuResponse(
                success=False,
                message="Menü çekilemedi. Site erişilemez veya hafta sonu olabilir."
            )
        
        return MenuResponse(
            success=True,
            tarih=menu_data.get('tarih'),
            yemekler=menu_data.get('yemekler'),
            message="Menü başarıyla çekildi"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Menü çekme hatası: {str(e)}")


@app.post("/api/generate-story", response_model=StoryResponse)
async def generate_story():
    """
    Ana endpoint - Menüyü çeker ve Instagram story görseli oluşturur
    
    Workflow:
    1. Yemekhane sitesinden menüyü çek
    2. Metni formatla
    3. Görsel oluştur
    4. Public URL döndür (Instagram API için)
    
    n8n bu endpoint'i çağıracak
    """
    try:
        print(f"[{datetime.now()}] 🚀 Story oluşturma başlatıldı...")
        
        # ADIM 1: Menüyü çek
        print("   📥 Menü çekiliyor...")
        scraper = MenuScraper()
        menu_data = scraper.get_todays_menu()
        
        if not menu_data:
            return StoryResponse(
                success=False,
                timestamp=datetime.now().isoformat(),
                message="Menü çekilemedi. Site erişilemez veya hafta sonu olabilir."
            )
        
        tarih = menu_data.get('tarih', 'Bilinmiyor')
        print(f"   ✓ Menü çekildi: {tarih}")
        
        # ADIM 2: Metni formatla
        print("   📝 Metin formatlanıyor...")
        formatter = TextFormatter(menu_data)
        formatted_text = formatter.get_formatted_text()
        print("   ✓ Metin formatlandı")
        
        # ADIM 3: Görsel oluştur
        print("   🎨 Görsel oluşturuluyor...")
        
        # Template ve output yolları
        template_path = os.path.join(ASSETS_DIR, 'kaynak_gorsel.png')
        output_filename = f"story_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        # Ayrıca sabit isimle de kaydet (kolay erişim için)
        latest_output_path = os.path.join(OUTPUT_DIR, 'story.png')
        
        generator = ImageGenerator(
            template_path=template_path,
            output_path=output_path
        )
        
        result_path = generator.generate_story(formatted_text)
        
        # story.png olarak da kopyala
        import shutil
        shutil.copy(output_path, latest_output_path)
        
        print(f"   ✓ Görsel oluşturuldu: {output_filename}")
        
        # Public URL oluştur
        # Bu URL Instagram Graph API'ye gönderilecek
        image_url = f"{API_BASE_URL}/static/{output_filename}"
        latest_url = f"{API_BASE_URL}/static/story.png"
        
        print(f"   ✓ Public URL: {image_url}")
        print(f"[{datetime.now()}] ✅ Story başarıyla oluşturuldu!")
        
        return StoryResponse(
            success=True,
            image_url=image_url,
            image_path=output_path,
            tarih=tarih,
            timestamp=datetime.now().isoformat(),
            message="Story görseli başarıyla oluşturuldu"
        )
        
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Hata: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Story oluşturma hatası: {str(e)}")


@app.get("/api/latest-story")
async def get_latest_story():
    """
    En son oluşturulan story görselinin bilgilerini döndürür
    """
    latest_path = os.path.join(OUTPUT_DIR, 'story.png')
    
    if not os.path.exists(latest_path):
        raise HTTPException(status_code=404, detail="Henüz oluşturulmuş story yok")
    
    # Dosya bilgilerini al
    stat = os.stat(latest_path)
    modified_time = datetime.fromtimestamp(stat.st_mtime)
    
    return {
        "success": True,
        "image_url": f"{API_BASE_URL}/static/story.png",
        "created_at": modified_time.isoformat(),
        "file_size": stat.st_size
    }


@app.get("/images/{filename}")
async def serve_image(filename: str):
    """
    Alternatif görsel sunma endpoint'i
    /images/story.png şeklinde erişim
    """
    file_path = os.path.join(OUTPUT_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Görsel bulunamadı")
    
    return FileResponse(file_path, media_type="image/png")


# ============================================================
# IMGBB UPLOAD HELPER
# ============================================================

def upload_to_imgbb(image_path: str) -> Optional[str]:
    """
    Görseli ImgBB'ye yükler ve public URL döndürür
    
    ImgBB ücretsiz plan: 
    - Günlük 100 upload
    - 32 MB max dosya boyutu
    - Kalıcı hosting
    """
    if not IMGBB_API_KEY:
        print("   ⚠️ IMGBB_API_KEY tanımlı değil, lokal URL kullanılacak")
        return None
    
    try:
        # Görseli base64'e çevir
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        # ImgBB API'ye yükle
        response = requests.post(
            'https://api.imgbb.com/1/upload',
            data={
                'key': IMGBB_API_KEY,
                'image': image_data,
                'name': f"menu_story_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                url = result['data']['url']
                print(f"   ✓ ImgBB'ye yüklendi: {url}")
                return url
        
        print(f"   ❌ ImgBB yükleme hatası: {response.text}")
        return None
        
    except Exception as e:
        print(f"   ❌ ImgBB hatası: {str(e)}")
        return None


@app.post("/api/generate-story-public")
async def generate_story_public():
    """
    Menüyü çeker, görsel oluşturur ve ImgBB'ye yükleyerek PUBLIC URL döndürür.
    Instagram Graph API için bu endpoint'i kullanın.
    """
    try:
        print(f"[{datetime.now()}] 🚀 Story oluşturma (public) başlatıldı...")
        
        # ADIM 1: Menüyü çek
        print("   📥 Menü çekiliyor...")
        scraper = MenuScraper()
        menu_data = scraper.get_todays_menu()
        
        if not menu_data:
            return {
                "success": False,
                "timestamp": datetime.now().isoformat(),
                "message": "Menü çekilemedi. Site erişilemez veya hafta sonu olabilir."
            }
        
        tarih = menu_data.get('tarih', 'Bilinmiyor')
        print(f"   ✓ Menü çekildi: {tarih}")
        
        # ADIM 2: Metni formatla
        print("   📝 Metin formatlanıyor...")
        formatter = TextFormatter(menu_data)
        formatted_text = formatter.get_formatted_text()
        print("   ✓ Metin formatlandı")
        
        # ADIM 3: Görsel oluştur
        print("   🎨 Görsel oluşturuluyor...")
        
        template_path = os.path.join(ASSETS_DIR, 'kaynak_gorsel.png')
        output_filename = f"story_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        latest_output_path = os.path.join(OUTPUT_DIR, 'story.png')
        
        generator = ImageGenerator(
            template_path=template_path,
            output_path=output_path
        )
        
        result_path = generator.generate_story(formatted_text)
        
        import shutil
        shutil.copy(output_path, latest_output_path)
        
        print(f"   ✓ Görsel oluşturuldu: {output_filename}")
        
        # ADIM 4: ImgBB'ye yükle (public URL için)
        print("   ☁️ ImgBB'ye yükleniyor...")
        public_url = upload_to_imgbb(output_path)
        
        if not public_url:
            # ImgBB başarısızsa lokal URL döndür
            public_url = f"{API_BASE_URL}/static/{output_filename}"
            print(f"   ⚠️ ImgBB kullanılamadı, lokal URL: {public_url}")
        
        print(f"[{datetime.now()}] ✅ Story başarıyla oluşturuldu!")
        
        return {
            "success": True,
            "image_url": public_url,
            "image_path": output_path,
            "tarih": tarih,
            "timestamp": datetime.now().isoformat(),
            "message": "Story görseli başarıyla oluşturuldu ve yüklendi"
        }
        
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Hata: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Story oluşturma hatası: {str(e)}")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("🚀 Instagram Menü Otomasyon API Başlatılıyor...")
    print("=" * 60)
    print(f"📁 Assets Dir: {ASSETS_DIR}")
    print(f"📁 Output Dir: {OUTPUT_DIR}")
    print(f"🌐 API Base URL: {API_BASE_URL}")
    print("=" * 60)
    print("📖 API Docs: http://localhost:8000/docs")
    print("=" * 60)
    
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Development modunda auto-reload
    )
