# Instagram Graph API Kullanım Rehberi

## 📌 Genel Bakış

Bu projede Instagram Graph API, yemekhane menüsü görsellerini Instagram Story olarak paylaşmak için kullanılır.

### Kullanılan API'ler:
- **Media Container API** - Görsel yükleme
- **Media Publish API** - Story yayınlama
- **Debug Token API** - Token durumu kontrolü

---

## 🔐 Token Yönetimi

### Token Türleri

| Token Türü | Süre | Kullanım |
|------------|------|----------|
| Short-lived User Token | ~1 saat | Graph API Explorer'dan alınır |
| Long-lived User Token | ~60 gün | Short-lived'dan dönüştürülür |
| Page Access Token | **Süresiz** | Long-lived user token ile alınır |

### Token Durumunu Kontrol Etme

```bash
cd 3_scripts
python refresh_token.py --check
```

**Örnek Çıktı:**
```
📊 Token Durumu:
   Geçerli: ✅ Evet
   Token Tipi: PAGE
   Token Süresi: ♾️  Süresiz (Never Expires)
   Veri Erişimi Süresi: 27.02.2026
   Veri Erişimi Kalan: 87 gün
```

### Token Yenileme

**Ne zaman yenilenmeli:**
- Veri erişimi süresi 14 günden az kaldığında
- API çağrıları "token expired" hatası verdiğinde

**Yenileme Adımları:**

1. [Graph API Explorer](https://developers.facebook.com/tools/explorer/)'a gidin
2. Uygulamanızı seçin
3. Şu izinleri ekleyin:
   - `pages_show_list`
   - `pages_read_engagement`
   - `instagram_basic`
   - `instagram_content_publish`
4. "Generate Access Token" tıklayın
5. Token'ı kopyalayın
6. Scripti çalıştırın:

```bash
cd 3_scripts
python refresh_token.py
# Seçenek 2'yi seçin ve token'ı yapıştırın
```

---

## 📌 API Endpoints

### 1. Media Container Oluştur (Story için)

```bash
POST https://graph.facebook.com/v18.0/{ig-user-id}/media
```

**Parametreler:**
| Parametre | Zorunlu | Açıklama |
|-----------|---------|----------|
| `image_url` | ✅ | Public erişilebilir görsel URL'si |
| `media_type` | ✅ | `STORIES` (story için) |
| `access_token` | ✅ | Page Access Token |

**Örnek:**

```bash
curl -X POST \
  "https://graph.facebook.com/v18.0/17841478682776821/media" \
  -d "image_url=https://i.ibb.co/xxx/story.png" \
  -d "media_type=STORIES" \
  -d "access_token=YOUR_TOKEN"
```

**Başarılı Yanıt:**
```json
{
  "id": "17844333108622760"
}
```

---

### 2. Media Publish (Story Yayınla)

```bash
POST https://graph.facebook.com/v18.0/{ig-user-id}/media_publish
```

**Parametreler:**
| Parametre | Zorunlu | Açıklama |
|-----------|---------|----------|
| `creation_id` | ✅ | Önceki adımdan gelen media ID |
| `access_token` | ✅ | Page Access Token |

**Örnek:**

```bash
curl -X POST \
  "https://graph.facebook.com/v18.0/17841478682776821/media_publish" \
  -d "creation_id=17844333108622760" \
  -d "access_token=YOUR_TOKEN"
```

**Başarılı Yanıt:**
```json
{
  "id": "18110064775551376"
}
```

---

### 3. Token Debug (Durum Kontrolü)

```bash
GET https://graph.facebook.com/debug_token
```

**Parametreler:**
| Parametre | Açıklama |
|-----------|----------|
| `input_token` | Kontrol edilecek token |
| `access_token` | Aynı token veya app token |

---

## ⚠️ Önemli Notlar

### Görsel Gereksinimleri

- **Format:** JPEG veya PNG
- **Boyut:** 1080x1920 piksel (9:16 oran) - Story için optimal
- **URL:** Public erişilebilir olmalı (ImgBB kullanılıyor)
- **Boyut Limiti:** Max 8MB

### Rate Limits

| Limit Türü | Değer |
|------------|-------|
| API çağrı/saat | 200 |
| Story/gün | 25 |
| Media container/saat | 25 |

### Yaygın Hatalar

| Hata Kodu | Açıklama | Çözüm |
|-----------|----------|-------|
| 190 | Token geçersiz/süresi dolmuş | Token yenile |
| 100 | Parametre hatası | Parametreleri kontrol et |
| 36003 | Rate limit aşıldı | Bekle ve tekrar dene |
| 9004 | Görsel indirilemedi | URL'nin public olduğundan emin ol |

---

## 🔗 Referanslar

- [Instagram Graph API Docs](https://developers.facebook.com/docs/instagram-api)
- [Content Publishing Guide](https://developers.facebook.com/docs/instagram-api/guides/content-publishing)
- [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
- [Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken/)
