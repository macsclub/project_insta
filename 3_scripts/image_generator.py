"""
Image Generator - PNG şablon üzerine menü metnini yazar
"""

from PIL import Image, ImageDraw, ImageFont
import os
import sys

# Config'den ayarları al
try:
    from config import FONT_PATH, FONT_SIZE, IMAGE_WIDTH, IMAGE_HEIGHT, ASSETS_DIR, TEMPLATE_PATH, LINE_SPACING
except ImportError:
    FONT_PATH = None
    FONT_SIZE = 140
    IMAGE_WIDTH = 2160
    IMAGE_HEIGHT = 3840
    ASSETS_DIR = '../2_assets'
    TEMPLATE_PATH = os.path.join(ASSETS_DIR, 'kaynak_gorsel.png')
    LINE_SPACING = 200


class ImageGenerator:
    def __init__(self, template_path=None, output_path='../5_tests/output/story.png'):
        self.template_path = template_path or TEMPLATE_PATH
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
            img = Image.open(self.template_path)
            # Template'i hedef boyuta resize et
            if img.size != (self.width, self.height):
                print(f"   ↳ Resize: {img.size} → ({self.width}, {self.height})")
                img = img.resize((self.width, self.height), Image.Resampling.LANCZOS)
            return img
        else:
            print(f"⚠️  Şablon bulunamadı, örnek şablon oluşturuluyor...")
            template = self.create_template()
            # Şablonu kaydet
            os.makedirs(os.path.dirname(self.template_path), exist_ok=True)
            template.save(self.template_path)
            print(f"✅ Örnek şablon oluşturuldu: {self.template_path}")
            return template
    
    def add_text_to_image(self, img, text, font_path=None):
        """Görsel üzerine metin yazar - 2160x3840 template için optimize edildi"""
        draw = ImageDraw.Draw(img)
        
        # Beyaz alan (2160x3840 template için)
        # Boyut: 1221 x 1645, Orta nokta: 1069 x 2093
        text_area_width = 1221
        text_area_height = 1645
        text_area_center_x = 1069
        text_area_center_y = 2093
        
        # Alan sınırları
        text_area_x_start = text_area_center_x - (text_area_width // 2)  # 458
        text_area_y_start = text_area_center_y - (text_area_height // 2)  # 1270
        
        # Maksimum yazı genişliği (beyaz alan - biraz padding)
        padding = 60
        max_text_width = text_area_width - (padding * 2)  # ~1101 px
        
        # Font ayarları - config'den veya parametre olarak
        font = None
        font_size = FONT_SIZE
        
        # Font yükleme fonksiyonu
        def load_font(size):
            # 1. Parametre olarak verilen font
            if font_path and os.path.exists(font_path):
                try:
                    return ImageFont.truetype(font_path, size)
                except Exception:
                    pass
            
            # 2. Config'deki font (LeagueSpartan-SemiBold)
            if FONT_PATH and os.path.exists(FONT_PATH):
                try:
                    return ImageFont.truetype(FONT_PATH, size)
                except Exception:
                    pass
            
            # 3. Windows fallback
            for win_font in ['C:/Windows/Fonts/LeagueSpartan-SemiBold.ttf', 'arial.ttf', 'C:/Windows/Fonts/arial.ttf']:
                try:
                    return ImageFont.truetype(win_font, size)
                except Exception:
                    continue
            
            # 4. Linux fallback
            linux_fonts = [
                '/app/assets/LeagueSpartan-SemiBold.ttf',
                '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
                '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
            ]
            for linux_font in linux_fonts:
                try:
                    return ImageFont.truetype(linux_font, size)
                except Exception:
                    continue
            
            return ImageFont.load_default()
        
        font = load_font(font_size)
        print(f"   ✓ Font yüklendi: {FONT_PATH}")
        
        # Metni satırlara böl (her satır bir yemek)
        original_lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Satır aralıkları
        food_spacing = LINE_SPACING  # Yemekler arası (büyük boşluk)
        wrap_spacing = int(LINE_SPACING * 0.65)  # Kaydırılmış satırlar arası (küçük boşluk)
        
        # Her yemek için satırları hazırla (gerekirse wrap)
        # Yapı: [(satır_metni, is_continuation), ...]
        processed_lines = []
        
        for food_name in original_lines:
            # Satır genişliğini ölç
            bbox = draw.textbbox((0, 0), food_name, font=font)
            text_width = bbox[2] - bbox[0]
            
            if text_width <= max_text_width:
                # Sığıyor, olduğu gibi ekle
                processed_lines.append((food_name, False))  # False = yeni yemek
            else:
                # Sığmıyor, kelime kelime böl
                words = food_name.split()
                current_line = ""
                is_first_line = True
                
                for word in words:
                    test_line = f"{current_line} {word}".strip()
                    bbox = draw.textbbox((0, 0), test_line, font=font)
                    test_width = bbox[2] - bbox[0]
                    
                    if test_width <= max_text_width:
                        current_line = test_line
                    else:
                        if current_line:
                            processed_lines.append((current_line, not is_first_line))
                            is_first_line = False
                        current_line = word
                
                if current_line:
                    processed_lines.append((current_line, not is_first_line))
        
        # Toplam yüksekliği hesapla
        total_height = 0
        for i, (line_text, is_continuation) in enumerate(processed_lines):
            if i == 0:
                total_height += font_size  # İlk satırın yüksekliği
            elif is_continuation:
                total_height += wrap_spacing  # Devam satırı
            else:
                total_height += food_spacing  # Yeni yemek
        
        # Dikey ortalama - Beyaz alanın ortasında
        y_start = text_area_center_y - (total_height // 2)
        
        # Siyah renk
        text_color = (0, 0, 0)
        
        for i, (line_text, is_continuation) in enumerate(processed_lines):
            # Boşluk ekle (ilk satır hariç)
            if i > 0:
                if is_continuation:
                    y_start += wrap_spacing
                else:
                    y_start += food_spacing
            
            # Metni yatay ortala
            bbox = draw.textbbox((0, 0), line_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_x = text_area_center_x - (text_width // 2)
            
            # Metin yaz
            draw.text((text_x, y_start), line_text, fill=text_color, font=font)
        
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
