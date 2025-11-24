"""
Text Formatter - Menü metnini Instagram hikayesi için formatlar
"""

import json
import sys
from datetime import datetime


class TextFormatter:
    def __init__(self, menu_data):
        self.menu_data = menu_data
    
    def format_for_story(self):
        """Menü verisini Instagram hikayesi için formatlar"""
        
        if not self.menu_data or not self.menu_data.get('yemekler'):
            return self._format_no_menu()
        
        # Başlık
        tarih = self.menu_data.get('tarih', 'Tarih bilinmiyor')
        
        # Emoji ekle
        lines = []
        lines.append("BUGÜNÜN MENÜSÜ")
        lines.append(f"📅 {tarih}")
        lines.append("")  # Boş satır
        
        # Yemekleri ekle
        yemekler = self.menu_data.get('yemekler', [])
        
        for i, yemek in enumerate(yemekler, 1):
            isim = yemek.get('isim', '').strip()
            
            # Karbonhidrat bilgisini temizle (görsel kalabalığı önlemek için)
            # "ETLİ MEVSİM TÜRLÜSÜ Karbonhidrat: 12 g" -> "ETLİ MEVSİM TÜRLÜSÜ"
            if 'Karbonhidrat:' in isim:
                isim = isim.split('Karbonhidrat:')[0].strip()
            
            # Emoji ekle
            emoji = self._get_emoji(i, isim)
            lines.append(f"{emoji} {isim}")
        
        # Footer
        lines.append("")
        lines.append("AFİYET OLSUN! 🍽️")
        
        return "\n".join(lines)
    
    def _get_emoji(self, index, yemek_isim):
        """Yemek türüne göre emoji döndürür"""
        yemek_lower = yemek_isim.lower()
        
        if 'çorba' in yemek_lower or 'corba' in yemek_lower:
            return "🍲"
        elif 'pilav' in yemek_lower or 'makarna' in yemek_lower:
            return "🍝"
        elif 'et' in yemek_lower or 'tavuk' in yemek_lower:
            return "🍖"
        elif 'börek' in yemek_lower or 'borek' in yemek_lower:
            return "🥐"
        elif 'ayran' in yemek_lower or 'süt' in yemek_lower:
            return "🥛"
        elif 'salata' in yemek_lower:
            return "🥗"
        elif 'tatlı' in yemek_lower or 'tatli' in yemek_lower:
            return "🍰"
        else:
            return "🍽️"
    
    def _format_no_menu(self):
        """Menü yoksa alternatif mesaj"""
        return """BUGÜNÜN MENÜSÜ

⚠️ Bugün için menü
   bulunamadı

Hafta sonu veya tatil
günü olabilir.

MACS Kulübü 🎓"""
    
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
                {"isim": "PATATESLİ BÖREK Karbonhidrat: 45 gr", "kalori": "(420 kcal)"},
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
