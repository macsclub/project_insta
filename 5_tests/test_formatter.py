"""
Bugünkü ve yarınki menüyü test et
"""
import sys
sys.path.insert(0, '../3_scripts')

from menu_scraper import MenuScraper
from text_formatter import TextFormatter

print("🧪 MENÜ FORMATTER TEST")
print("=" * 70)

# 1. Menüyü çek
scraper = MenuScraper()
menu_data = scraper.get_todays_menu()

if not menu_data:
    print("❌ Menü çekilemedi!")
    sys.exit(1)

print(f"\n📅 Tarih: {menu_data['tarih']}")
print(f"\n🍴 Ham Menü Verisi:")
print("-" * 70)
for i, yemek in enumerate(menu_data['yemekler'], 1):
    print(f"{i}. {yemek['isim']}")

# 2. Formatla
formatter = TextFormatter(menu_data)
formatted_text = formatter.get_formatted_text()

print(f"\n📱 STORY İÇİN FORMATLANMIŞ METİN:")
print("=" * 70)
print(formatted_text)
print("=" * 70)

# 3. Test senaryoları
print("\n🔍 TEST SONUÇLARI:")
print("-" * 70)

# Test 1: Karbonhidrat bilgisi temizlenmiş mi?
has_carb = any('karbonhidrat' in line.lower() for line in formatted_text.split('\n'))
print(f"✅ Karbonhidrat bilgisi temizlendi: {'HAYIR ❌' if has_carb else 'EVET ✅'}")

# Test 2: Tüm satırlar büyük harf mi?
lines = [line for line in formatted_text.split('\n') if line]
all_upper = all(line.isupper() for line in lines)
print(f"✅ Tüm yemekler büyük harf: {'EVET ✅' if all_upper else 'HAYIR ❌'}")

# Test 3: Kaç yemek var?
print(f"✅ Toplam yemek sayısı: {len(lines)}")

print("\n✨ Test tamamlandı!")