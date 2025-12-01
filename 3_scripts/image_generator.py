"""
Image Generator - PNG şablon üzerine menü metnini yazar
"""

from PIL import Image, ImageDraw, ImageFont
import os
import sys

# Config'den ayarları al
try:
    from config import FONT_PATH, FONT_SIZE, IMAGE_WIDTH, IMAGE_HEIGHT, ASSETS_DIR
except ImportError:
    FONT_PATH = None
    FONT_SIZE = 40
    IMAGE_WIDTH = 900
    IMAGE_HEIGHT = 1600
    ASSETS_DIR = '../2_assets'


class ImageGenerator:
    def __init__(self, template_path=None, output_path='../5_tests/output/story.png'):
        self.template_path = template_path or os.path.join(ASSETS_DIR, 'kaynak_gorsel.jpg')
        self.output_path = output_path
        self.width = IMAGE_WIDTH
        self.height = IMAGE_HEIGHT
        
    def create_template(self):
        """Örnek şablon oluşturur (gerçek şablon yoksa)"""
        # Gradient background (mavi tonları)
        img = Image.new('RGB', (self.width, self.height), color='#1a1a2e')
        draw = ImageDraw.Draw(img)
        
        # Basit gradient efekti
        for i in range(self.height):
            # Üstten alta mavi tonları
            ratio = i / self.height
            r = int(26 + (41 - 26) * ratio)
            g = int(26 + (128 - 26) * ratio)
            b = int(46 + (185 - 46) * ratio)
            draw.line([(0, i), (self.width, i)], fill=(r, g, b))
        
        # Logo/başlık alanı (üst kısım)
        draw.rectangle([(0, 0), (self.width, 300)], fill=(26, 26, 46, 200))
        
        # MACS logosu yazısı (üstte)
        try:
            font_large = ImageFont.truetype("arial.ttf", 80)
        except:
            font_large = ImageFont.load_default()
        
        text = "MACS KULÜBÜ"
        bbox = draw.textbbox((0, 0), text, font=font_large)
        text_width = bbox[2] - bbox[0]
        text_x = (self.width - text_width) // 2
        draw.text((text_x, 100), text, fill='white', font=font_large)
        
        # Alt kısım (footer)
        draw.rectangle([(0, self.height - 200), (self.width, self.height)], fill=(26, 26, 46, 200))
        
        try:
            font_small = ImageFont.truetype("arial.ttf", 40)
        except:
            font_small = ImageFont.load_default()
        
        footer_text = "ESOGÜ Yemekhane"
        bbox = draw.textbbox((0, 0), footer_text, font=font_small)
        text_width = bbox[2] - bbox[0]
        text_x = (self.width - text_width) // 2
        draw.text((text_x, self.height - 120), footer_text, fill='white', font=font_small)
        
        return img
    
    def load_template(self):
        """Şablon dosyasını yükler veya oluşturur"""
        if os.path.exists(self.template_path):
            print(f"📄 Şablon yükleniyor: {self.template_path}")
            return Image.open(self.template_path)
        else:
            print(f"⚠️  Şablon bulunamadı, örnek şablon oluşturuluyor...")
            template = self.create_template()
            # Şablonu kaydet
            os.makedirs(os.path.dirname(self.template_path), exist_ok=True)
            template.save(self.template_path)
            print(f"✅ Örnek şablon oluşturuldu: {self.template_path}")
            return template
    
    def add_text_to_image(self, img, text, font_path=None):
        """Görsel üzerine metin yazar"""
        draw = ImageDraw.Draw(img)
        
        # Font ayarları - config'den veya parametre olarak
        font = None
        font_size = FONT_SIZE
        
        # 1. Parametre olarak verilen font
        if font_path and os.path.exists(font_path):
            try:
                font = ImageFont.truetype(font_path, font_size)
            except Exception:
                pass
        
        # 2. Config'deki font
        if font is None and FONT_PATH and os.path.exists(FONT_PATH):
            try:
                font = ImageFont.truetype(FONT_PATH, font_size)
            except Exception:
                pass
        
        # 3. Windows fallback
        if font is None:
            for win_font in ['arial.ttf', 'C:/Windows/Fonts/arial.ttf']:
                try:
                    font = ImageFont.truetype(win_font, font_size)
                    break
                except Exception:
                    continue
        
        # 4. Linux fallback
        if font is None:
            linux_fonts = [
                '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
                '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
            ]
            for linux_font in linux_fonts:
                try:
                    font = ImageFont.truetype(linux_font, font_size)
                    break
                except Exception:
                    continue
        
        # 5. Hiçbiri yoksa default (çok küçük olacak ama çalışır)
        if font is None:
            print("⚠️  Font yüklenemedi, varsayılan font kullanılıyor")
            font = ImageFont.load_default()
        
        # Metni satırlara böl
        lines = text.split('\n')
        
        # Başlangıç pozisyonu (ortadaki beyaz alan)
        y_start = 550
        line_height = 55
        
        for line in lines:
            if not line.strip():
                y_start += line_height // 2  # Boş satır için yarım yükseklik
                continue
            
            # Metni ortala
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            text_x = (self.width - text_width) // 2
            
            # Gölge efekti (beyaz alan için hafif gri)
            draw.text((text_x + 1, y_start + 1), line, fill=(200, 200, 200), font=font)
            # Asıl metin (siyah - beyaz alan için)
            draw.text((text_x, y_start), line, fill=(0, 0, 0), font=font)
            
            y_start += line_height
        
        return img
    
    def generate_story(self, text, font_path=None):
        """Instagram story görseli oluşturur"""
        # Şablonu yükle
        img = self.load_template()
        
        # Metin ekle
        img = self.add_text_to_image(img, text, font_path)
        
        # Kaydet
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        img.save(self.output_path, quality=95)
        
        print(f"✅ Görsel oluşturuldu: {self.output_path}")
        print(f"   Boyut: {self.width}x{self.height} (Instagram Story)")
        
        return self.output_path


def main():
    """Ana fonksiyon"""
    
    # Metin dosyasından oku
    text_file = '../5_tests/output/formatted_text.txt'
    
    if len(sys.argv) > 1:
        text_file = sys.argv[1]
    
    try:
        with open(text_file, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"❌ Hata: Metin dosyası okunamadı - {e}", file=sys.stderr)
        return 1
    
    print("🎨 Image Generator Başlatıldı...")
    print("=" * 50)
    
    # Generator oluştur
    generator = ImageGenerator()
    
    # Görsel oluştur
    output_path = generator.generate_story(text)
    
    print("=" * 50)
    print(f"🎉 İşlem tamamlandı!")
    print(f"📁 Çıktı: {output_path}")
    
    return 0


if __name__ == "__main__":
    exit(main())
