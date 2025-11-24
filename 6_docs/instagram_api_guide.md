# Instagram Graph API Kullanım Rehberi

## 📌 API Endpoints

### 1. Media Upload (Container Oluştur)

```bash
POST https://graph.facebook.com/v18.0/{ig-user-id}/media
```

**Parametreler:**
- `image_url`: Görsel URL'si (public erişilebilir olmalı)
- `caption`: Hikaye açıklaması (opsiyonel)
- `access_token`: Page Access Token

**Örnek:**

```bash
curl -X POST \
  "https://graph.facebook.com/v18.0/YOUR_IG_USER_ID/media" \
  -d "image_url=https://example.com/story.png" \
  -d "access_token=YOUR_ACCESS_TOKEN"
```

**Dönüş:**
```json
{
  "id": "123456789"
}
```

---

### 2. Media Publish (Hikaye Olarak Yayınla)

```bash
POST https://graph.facebook.com/v18.0/{ig-user-id}/media_publish
```

**Parametreler:**
- `creation_id`: Önceki adımdan gelen media ID
- `access_token`: Page Access Token

**Örnek:**

```bash
curl -X POST \
  "https://graph.facebook.com/v18.0/YOUR_IG_USER_ID/media_publish" \
  -d "creation_id=123456789" \
  -d "access_token=YOUR_ACCESS_TOKEN"
```

**Dönüş:**
```json
{
  "id": "987654321"
}
```

---

## ⚠️ Önemli Notlar

1. **Görsel URL Public Olmalı:** Instagram API, görseli bir URL'den indirmek ister. Görselin public erişilebilir bir URL'de olması gerekir.

2. **Rate Limits:** API çağrılarında limit var. Saatlik/günlük limitler için Facebook dökümanlarını inceleyin.

3. **Token Geçerliliği:** Long-lived token'lar ~60 gün geçerlidir. Token yenilemek için setup guide'ına bakın.

4. **Test Modu:** Geliştirme sırasında gerçek Instagram hesabına yüklemeden önce API yanıtlarını test edin.

---

## 🔗 Referanslar

- [Instagram Graph API Docs](https://developers.facebook.com/docs/instagram-api)
- [Content Publishing](https://developers.facebook.com/docs/instagram-api/guides/content-publishing)
