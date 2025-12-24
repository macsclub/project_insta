"""
Text Formatter - Menü metnini Instagram hikayesi için formatlar
"""

import json
import sys
import re
from datetime import datetime


class TextFormatter:
    def __init__(self, menu_data):
        self.menu_data = menu_data
    
    def _turkish_upper(self, text):
        """Türkçe karakterleri doğru şekilde büyük harfe çevirir"""
        # Türkçe karakter dönüşüm haritası
        turkish_map = {
            'i': 'İ',
            'ı': 'I',
            'ğ': 'Ğ',
            'ü': 'Ü',
            'ş': 'Ş',
            'ö': 'Ö',
            'ç': 'Ç'
        }
        
        result = []
        for char in text:
            if char in turkish_map:
                result.append(turkish_map[char])
            else:
                result.append(char.upper())
        
        return ''.join(result)
    
    def format_for_story(self):
        """Menü verisini Instagram hikayesi için formatlar - Sadece yemek isimleri"""
        
        if not self.menu_data or not self.menu_data.get('yemekler'):
            return self._format_no_menu()
        
        lines = []
        
        # Sadece yemekleri ekle - emoji, başlık, tarih yok
        yemekler = self.menu_data.get('yemekler', [])
        
        for yemek in yemekler:
            isim = yemek.get('isim', '').strip()
            
            # Karbonhidrat bilgisini temizle (hem büyük hem küçük harf)
            # "ETLİ MEVSİM TÜRLÜSÜ Karbonhidrat: 12 g" -> "ETLİ MEVSİM TÜRLÜSÜ"
            # "BULGUR PİLAVI karbonhidrat: 30 gr" -> "BULGUR PİLAVI"
            if 'karbonhidrat:' in isim.lower():
                # Case-insensitive temizleme
                isim = re.split(r'[Kk]arbonhidrat:', isim)[0].strip()
            
            # Yemek ismini Türkçe kurallarına göre büyük harfe çevir
            if isim:
                isim = self._turkish_upper(isim)
                lines.append(isim)
        
        return "\n".join(lines)
    
    def _format_no_menu(self):
        """Menü yoksa alternatif mesaj"""
        return "MENU BULUNAMADI"
    
    def get_formatted_text(self):
        """Formatlanmış metni döndürür"""
        return self.format_for_story()


def main():
    """Ana fonksiyon - Test amaçlı"""
    
    # JSON dosyasından oku veya stdin'den al
    if len(sys.argv) > 1:
        # Dosya yolundan oku
        filepath = sys.argv[1]
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                menu_data = json.load(f)
        except Exception as e:
            print(f"❌ Hata: JSON dosyası okunamadı - {e}", file=sys.stderr)
            return 1
    else:
        # Test için örnek veri
        menu_data = {
            "tarih": "24 Kas. Pazartesi",
            "yemekler": [
                {"isim": "ERİŞTELİ YEŞİL MERCİMEK ÇORBA", "kalori": "(170 kcal)"},
                {"isim": "ETLİ MEVSİM TÜRLÜSÜ Karbonhidrat: 12 g", "kalori": "(295 kcal)"},
                {"isim": "BULGUR PİLAVI karbonhidrat: 30 gr", "kalori": "(180 kcal)"},
                {"isim": "peynirli/patatesli börek", "kalori": "(350 kcal)"},
                {"isim": "şekerlı pılav", "kalori": "(250 kcal)"},
                {"isim": "AYRAN Karbonhidrat: 4 gr", "kalori": "(67 kcal)"}
            ],
            "menu_tipi": "Standart Menü"
        }
    
    formatter = TextFormatter(menu_data)
    formatted_text = formatter.get_formatted_text()
    
    print("📝 Formatlanmış Metin:")
    print("=" * 50)
    print(formatted_text)
    print("=" * 50)
    
    # Dosyaya kaydet
    output_file = '../5_tests/output/formatted_text.txt'
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(formatted_text)
        print(f"\n✅ Metin kaydedildi: {output_file}")
    except Exception as e:
        print(f"❌ Hata: Metin kaydedilemedi - {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())