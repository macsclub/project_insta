"""
Main Script - Instagram Yemekhane Menüsü Otomasyonu
Tüm adımları sırayla çalıştırır: Scrape → Format → Generate Image
"""

import sys
import os
from datetime import datetime

# Kendi modüllerimizi import et
from menu_scraper import MenuScraper
from text_formatter import TextFormatter
from image_generator import ImageGenerator


class MenuAutomation:
    def __init__(self, output_dir='../5_tests/output'):
        self.output_dir = output_dir
        self.menu_json_path = os.path.join(output_dir, 'menu.json')
        self.formatted_text_path = os.path.join(output_dir, 'formatted_text.txt')
        self.story_image_path = os.path.join(output_dir, 'story.png')
        
        # Output dizinini oluştur
        os.makedirs(output_dir, exist_ok=True)
    
    def run(self):
        """Tüm adımları sırayla çalıştırır"""
        print("🚀 Instagram Menü Otomasyonu Başlatıldı")
        print("=" * 60)
        print(f"⏰ Tarih/Saat: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        print("=" * 60)
        
        # ADIM 1: Menüyü Web'den Çek
        print("\n📥 ADIM 1: Menüyü web sitesinden çekiliyor...")
        menu_data = self._scrape_menu()
        if not menu_data:
            print("❌ Menü çekilemedi. İşlem sonlandırılıyor.")
            return False
        
        # ADIM 2: Metni Formatla
        print("\n📝 ADIM 2: Metin formatlanıyor...")
        formatted_text = self._format_text(menu_data)
        if not formatted_text:
            print("❌ Metin formatlanamadı. İşlem sonlandırılıyor.")
            return False
        
        # ADIM 3: Görsel Oluştur
        print("\n🎨 ADIM 3: Instagram story görseli oluşturuluyor...")
        image_path = self._generate_image(formatted_text)
        if not image_path:
            print("❌ Görsel oluşturulamadı. İşlem sonlandırılıyor.")
            return False
        
        # BAŞARI
        print("\n" + "=" * 60)
        print("✅ TÜM İŞLEMLER BAŞARIYLA TAMAMLANDI!")
        print("=" * 60)
        print(f"📄 Menü JSON: {self.menu_json_path}")
        print(f"📝 Formatlanmış Metin: {self.formatted_text_path}")
        print(f"🖼️  Story Görseli: {self.story_image_path}")
        print("=" * 60)
        
        return True
    
    def _scrape_menu(self):
        """Menüyü web sitesinden çeker"""
        try:
            scraper = MenuScraper()
            menu_data = scraper.get_todays_menu()
            
            if menu_data:
                # JSON'a kaydet
                scraper.save_to_json(menu_data, self.menu_json_path)
                
                # Özet bilgi
                tarih = menu_data.get('tarih', 'Bilinmiyor')
                yemek_sayisi = len(menu_data.get('yemekler', []))
                print(f"   ✓ Tarih: {tarih}")
                print(f"   ✓ Yemek Sayısı: {yemek_sayisi}")
                
                return menu_data
            else:
                return None
                
        except Exception as e:
            print(f"   ❌ Hata: {e}", file=sys.stderr)
            return None
    
    def _format_text(self, menu_data):
        """Menü verisini formatlar"""
        try:
            formatter = TextFormatter(menu_data)
            formatted_text = formatter.get_formatted_text()
            
            # Dosyaya kaydet
            with open(self.formatted_text_path, 'w', encoding='utf-8') as f:
                f.write(formatted_text)
            
            print(f"   ✓ Metin formatlandı ve kaydedildi")
            
            # Önizleme (ilk 3 satır)
            lines = formatted_text.split('\n')[:3]
            for line in lines:
                print(f"   │ {line}")
            
            return formatted_text
            
        except Exception as e:
            print(f"   ❌ Hata: {e}", file=sys.stderr)
            return None
    
    def _generate_image(self, formatted_text):
        """Instagram story görseli oluşturur"""
        try:
            generator = ImageGenerator(output_path=self.story_image_path)
            image_path = generator.generate_story(formatted_text)
            
            print(f"   ✓ Görsel başarıyla oluşturuldu")
            print(f"   ✓ Boyut: 1080x1920 (Instagram Story)")
            
            return image_path
            
        except Exception as e:
            print(f"   ❌ Hata: {e}", file=sys.stderr)
            return None
    
    def get_story_path(self):
        """Oluşturulan story görselinin yolunu döndürür"""
        return self.story_image_path


def main():
    """Ana fonksiyon"""
    try:
        automation = MenuAutomation()
        success = automation.run()
        
        if success:
            # n8n için JSON output (opsiyonel)
            import json
            result = {
                "success": True,
                "timestamp": datetime.now().isoformat(),
                "story_image": automation.get_story_path(),
                "message": "Menü görseli başarıyla oluşturuldu"
            }
            print(f"\n📦 JSON Output:")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0
        else:
            return 1
            
    except Exception as e:
        print(f"\n❌ HATA: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
