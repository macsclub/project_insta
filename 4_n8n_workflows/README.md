# n8n Workflow Dosyaları

Bu klasör n8n workflow JSON dosyalarını içerir.

## Dosyalar

- `workflow.json` - Instagram menü otomasyon workflow'u

## Workflow İçe Aktarma

1. n8n arayüzünü aç (http://localhost:5678)
2. Sol menüden "Workflows" → "Add Workflow"
3. Sağ üst "..." menüsünden "Import from File"
4. `workflow.json` dosyasını seç
5. **ÖNEMLİ:** Aşağıdaki değerleri kendi bilgilerinle değiştir:
   - `YOUR_INSTAGRAM_USER_ID` → Instagram Business Account ID
   - `YOUR_PAGE_ACCESS_TOKEN` → Facebook Page Access Token
6. Workflow'u kaydet ve aktifleştir

## Workflow Yapısı

```
Schedule Trigger (08:30, Pazartesi-Cuma)
    ↓
HTTP Request (Python API - generate-story-public)
    ↓
IF (success == true)
    ↓
HTTP Request (Instagram API - Media Container)
    ↓
HTTP Request (Instagram API - Publish Story)
```

## Gerekli API Anahtarları

Bu değerleri n8n workflow'unda elle girmeniz gerekiyor:

| Değişken | Nereden Alınır |
|----------|----------------|
| `YOUR_INSTAGRAM_USER_ID` | Facebook Business Suite → Instagram → Settings |
| `YOUR_PAGE_ACCESS_TOKEN` | Facebook Graph API Explorer |

## Token Yenileme

Page Access Token ~60 gün geçerlidir. Yenilemek için:

```bash
cd 3_scripts
python refresh_token.py
```

## Test

1. n8n'de workflow'u aç
2. "Test Workflow" butonuna tıkla
3. Tüm adımların başarılı olduğunu kontrol et
4. Instagram hesabında story'nin paylaşıldığını doğrula
