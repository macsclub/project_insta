# Facebook ve Instagram API Kurulum Rehberi

## 🔵 Adım 1: Instagram Hesabını Business'a Dönüştür

1. Instagram uygulamasını aç
2. Profil → Ayarlar → Hesap Türü
3. "Profesyonel Hesaba Geç" seçeneğini seç
4. İşletme kategorisi seç

---

## 🔵 Adım 2: Facebook Sayfası Oluştur

1. Facebook'ta yeni bir sayfa oluştur
2. Sayfa adı: MACS Kulübü (veya uygun isim)
3. Kategori: Topluluk veya Kulüp

---

## 🔵 Adım 3: Instagram'ı Facebook Sayfasına Bağla

1. Facebook Sayfanıza git
2. Ayarlar → Instagram
3. "Hesap Bağla" butonuna tıkla
4. Instagram bilgilerinizle giriş yap

---

## 🔵 Adım 4: Facebook Developer Hesabı Oluştur

1. https://developers.facebook.com/ adresine git
2. "Get Started" butonuna tıkla
3. Hesabınızı doğrula

---

## 🔵 Adım 5: Yeni Uygulama Oluştur

1. "My Apps" → "Create App"
2. Uygulama türü: **Business**
3. Uygulama adı: "MACS Instagram Automation"
4. Oluştur

---

## 🔵 Adım 6: Instagram Graph API Ekle

1. Uygulamanızın Dashboard'una git
2. "Add Product" → **Instagram Graph API** seç
3. "Set Up" butonuna tıkla

---

## 🔵 Adım 7: Access Token Oluştur

1. Graph API Explorer'a git: https://developers.facebook.com/tools/explorer/
2. Uygulamanızı seçin
3. "Get User Access Token" butonuna tıkla
4. Şu izinleri seçin:
   - `pages_show_list`
   - `pages_read_engagement`
   - `instagram_basic`
   - `instagram_content_publish`
5. "Generate Access Token"
6. Token'ı kopyalayın

---

## 🔵 Adım 8: Long-Lived Token'a Dönüştür

Kısa ömürlü token'ı uzun ömürlü yapmak için:

```bash
curl -i -X GET "https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id=YOUR_APP_ID&client_secret=YOUR_APP_SECRET&fb_exchange_token=YOUR_SHORT_LIVED_TOKEN"
```

---

## 🔵 Adım 9: Page Access Token Al

```bash
curl -i -X GET "https://graph.facebook.com/v18.0/me/accounts?access_token=YOUR_LONG_LIVED_USER_TOKEN"
```

Dönen JSON'dan `page_id` ve `access_token` değerlerini kaydet.

---

## 🔵 Adım 10: Instagram Business Account ID Al

```bash
curl -i -X GET "https://graph.facebook.com/v18.0/YOUR_PAGE_ID?fields=instagram_business_account&access_token=YOUR_PAGE_ACCESS_TOKEN"
```

---

## ✅ Gerekli Bilgiler

Tüm bu adımları tamamladıktan sonra elinizde şunlar olmalı:

- ✅ App ID
- ✅ App Secret
- ✅ Page ID
- ✅ Page Access Token (Long-lived)
- ✅ Instagram Business Account ID

Bu bilgileri `api_credentials.example.json` dosyasına kopyalayın ve `api_credentials.json` olarak kaydedin.

⚠️ **ÖNEMLİ:** `api_credentials.json` dosyasını asla GitHub'a yüklemeyin!
