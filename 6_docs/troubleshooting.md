# Sorun Giderme Rehberi

## 🔴 Sık Karşılaşılan Sorunlar

### 1. Menü Sitesi Açılmıyor / HTTP 403/404

**Sebep:** Site erişim hatası veya URL değişmiş olabilir.

**Çözüm:**
- URL'yi kontrol edin
- Tarayıcıdan manuel erişim deneyin
- User-Agent header ekleyin

---

### 2. HTML Parse Hatası

**Sebep:** Site yapısı değişmiş olabilir.

**Çözüm:**
- `5_tests/sample_menu.html` dosyasını güncelleyin
- Scraper'daki CSS selector'ları kontrol edin
- BeautifulSoup yerine lxml parser deneyin

---

### 3. Instagram API Token Hatası

**Sebep:** Access token geçersiz veya süresi dolmuş.

**Çözüm:**
- Token'ın geçerliliğini kontrol edin
- Yeni long-lived token oluşturun
- Permissions'ları kontrol edin

---

### 4. Görsel Yüklenemedi

**Sebep:** Görsel URL'si public değil veya format hatalı.

**Çözüm:**
- PNG formatı kullanın
- Görsel boyutunu kontrol edin (1080x1920)
- URL'nin public erişilebilir olduğundan emin olun

---

### 5. Font Bulunamadı

**Sebep:** Font dosyası yolu hatalı.

**Çözüm:**
- `2_assets/fonts/` klasöründe font olduğundan emin olun
- Font yolunu mutlak path olarak verin
- Alternatif default font kullanın

---

### 6. n8n Workflow Çalışmıyor

**Sebep:** Credentials yanlış veya node ayarları hatalı.

**Çözüm:**
- Tüm credentials'ları kontrol edin
- Her node'u manuel execute edin
- Error mesajlarını okuyun

---

### 7. Cron Tetiklenmiyor

**Sebep:** Cron expression yanlış veya workflow pasif.

**Çözüm:**
- Workflow'un "Active" olduğundan emin olun
- Timezone ayarını kontrol edin
- Manuel execution ile test edin

---

## 📞 Destek

Sorun devam ediyorsa:
1. Error log'larını toplayın
2. Adım adım ne yaptığınızı not edin
3. GitHub issue açın veya ekip ile iletişime geçin
