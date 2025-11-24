# n8n Workflow Dosyaları

Bu klasör n8n workflow JSON dosyalarını içerir.

## Dosyalar

- `workflow_v1.json` - Ana Instagram menü otomasyon workflow'u

## Workflow İçe Aktarma

1. n8n arayüzünü aç (http://localhost:5678)
2. Sol üst → "Import from File"
3. `workflow_v1.json` dosyasını seç
4. Credentials'ları ayarla
5. Workflow'u aktifleştir

## Workflow Yapısı

```
Cron Trigger (09:30, Pazartesi-Cuma)
    ↓
HTTP Request (Menü sitesini çek)
    ↓
Function (HTML parse ve menü ayıkla)
    ↓
Function (Metin formatla)
    ↓
Read Binary File (Template PNG)
    ↓
Python Script (Görsel oluştur)
    ↓
Instagram Graph API (Media Upload)
    ↓
Instagram Graph API (Publish Story)
    ↓
[Opsiyonel] Discord Webhook (Bildirim)
```

## Notlar

- Workflow henüz oluşturulmadı. AŞAMA 4'te eklenecek.
- Test için önce manuel execution yapın
- Cron'u aktifleştirmeden önce tüm adımları test edin
