"""
Yemekhane Menü Scraper
https://yemekhane.ogu.edu.tr/ sitesinden günlük menüyü çeker
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import sys


class MenuScraper:
    def __init__(self, url="https://yemekhane.ogu.edu.tr/"):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def fetch_page(self):
        """Web sayfasını çeker"""
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"❌ Hata: Web sayfası çekilemedi - {e}", file=sys.stderr)
            return None
    
    def parse_menu(self, html_content):
        """HTML'den menü verilerini ayıklar"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Bugünün menüsünü bul (class="bugun" olan div)
        bugun_menu = soup.find('div', class_='bugun')
        
        if not bugun_menu:
            print("❌ Hata: Bugünün menüsü bulunamadı", file=sys.stderr)
            return None
        
        # Tarihi al
        tarih_span = bugun_menu.find('span', class_='yemek-menu-ay')
        tarih = tarih_span.text.strip() if tarih_span else "Tarih bilinmiyor"
        
        # Yemekleri al
        yemek_listesi = bugun_menu.find('ul', class_='yemek-menu-liste')
        yemekler = []
        
        if yemek_listesi:
            for li in yemek_listesi.find_all('li', recursive=False):
                yemek_span = li.find('span', class_='yemek-menu-yemek')
                kalori_span = li.find('span', class_='yemek-menu-kalori')
                
                if yemek_span and yemek_span.find('a'):
                    yemek_adi = yemek_span.find('a').text.strip()
                    kalori = kalori_span.text.strip() if kalori_span else ""
                    
                    # Boş satırları atla
                    if yemek_adi:
                        yemekler.append({
                            'isim': yemek_adi,
                            'kalori': kalori
                        })
        
        return {
            'tarih': tarih,
            'yemekler': yemekler,
            'tarih_timestamp': datetime.now().isoformat(),
            'menu_tipi': 'Standart Menü'
        }
    
    def get_todays_menu(self):
        """Bugünün menüsünü çeker ve döndürür"""
        html_content = self.fetch_page()
        
        if not html_content:
            return None
        
        menu_data = self.parse_menu(html_content)
        return menu_data
    
    def save_to_json(self, menu_data, filepath='../5_tests/output/menu.json'):
        """Menü verisini JSON dosyasına kaydeder"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(menu_data, f, ensure_ascii=False, indent=2)
            print(f"✅ Menü başarıyla kaydedildi: {filepath}")
            return True
        except Exception as e:
            print(f"❌ Hata: JSON kaydedilemedi - {e}", file=sys.stderr)
            return False


def main():
    """Ana fonksiyon"""
    print("🍽️  Yemekhane Menü Scraper Başlatıldı...")
    print("=" * 50)
    
    scraper = MenuScraper()
    menu_data = scraper.get_todays_menu()
    
    if menu_data:
        print(f"\n📅 Tarih: {menu_data['tarih']}")
        print(f"📋 Menü Tipi: {menu_data['menu_tipi']}")
        print(f"\n🍴 Bugünün Menüsü:")
        print("-" * 50)
        
        if menu_data['yemekler']:
            for i, yemek in enumerate(menu_data['yemekler'], 1):
                print(f"{i}. {yemek['isim']} {yemek['kalori']}")
        else:
            print("⚠️  Bugün için menü bulunamadı (tatil veya hafta sonu olabilir)")
        
        print("-" * 50)
        
        # JSON'a kaydet
        scraper.save_to_json(menu_data)
        
        # JSON formatında da yazdır (n8n için)
        print("\n📦 JSON Çıktısı:")
        print(json.dumps(menu_data, ensure_ascii=False, indent=2))
        
        return 0
    else:
        print("\n❌ Menü çekilemedi!")
        return 1


if __name__ == "__main__":
    exit(main())
