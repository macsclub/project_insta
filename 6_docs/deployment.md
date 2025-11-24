# Deployment Rehberi

## 🚀 Projeyi Canlıya Alma

### Ön Gereksinimler

- ✅ Instagram Business hesabı hazır
- ✅ Facebook Page bağlantılı
- ✅ API credentials oluşturulmuş
- ✅ n8n Docker container çalışıyor
- ✅ Tüm scriptler test edilmiş

---

## Adım 1: Python Environment Kurulumu

```bash
cd 3_scripts
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## Adım 2: Konfigürasyon

1. `1_setup/api_credentials.example.json` dosyasını kopyalayın
2. `1_setup/api_credentials.json` olarak kaydedin
3. Gerçek API bilgilerini doldurun

---

## Adım 3: Template Hazırlama

1. Tasarım ekibinden gelen PNG şablonu `2_assets/` klasörüne ekleyin
2. `config.py` dosyasında `TEMPLATE_PATH` değerini güncelleyin

---

## Adım 4: Scraper Test

```bash
cd 3_scripts
python menu_scraper.py
```

Menü başarıyla çekildi mi kontrol edin.

---

## Adım 5: Image Generator Test

```bash
python image_generator.py
```

`5_tests/output/` klasöründe görsel oluştu mu kontrol edin.

---

## Adım 6: n8n Workflow Import

1. n8n arayüzünü aç
2. `4_n8n_workflows/workflow_v1.json` dosyasını import et
3. Credentials'ları ayarla

---

## Adım 7: Manuel Test

1. n8n'de workflow'u manuel çalıştır
2. Her adımın başarılı olduğunu kontrol et
3. Instagram'da hikayenin yayınlandığını doğrula

---

## Adım 8: Cron Aktivasyonu

1. Workflow'daki Cron node'unu aç
2. Schedule'ı ayarla: **Pazartesi-Cuma, 09:30**
3. Workflow'u "Active" yap

---

## Adım 9: Monitoring

İlk hafta her gün kontrol edin:
- Hikaye yayınlandı mı?
- Error log var mı?
- Görsel kalitesi uygun mu?

---

## 🔒 Güvenlik

- `.env` dosyaları git'e eklemeyin
- API credentials'ları şifreleyin
- Access token'ları periyodik yenileyin

---

## 🔄 Güncellemeler

Template değişirse:
1. Yeni PNG'yi `2_assets/` klasörüne ekle
2. `config.py`'de path'i güncelle
3. Test et
4. Canlıya al

---

## ✅ Checklist

- [ ] Python environment kuruldu
- [ ] Requirements yüklendi
- [ ] API credentials ayarlandı
- [ ] Template eklendi
- [ ] Scraper test edildi
- [ ] Image generator test edildi
- [ ] n8n workflow import edildi
- [ ] Manuel test başarılı
- [ ] Cron aktif
- [ ] İlk otomatik çalışma doğrulandı
