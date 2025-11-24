# 📸 Instagram Yemekhane Menüsü Otomasyon Projesi

MACS Kulübü için otomatik Instagram hikayesi paylaşım sistemi.

## 📁 Proje Yapısı

```
project_instagram/
├── 1_setup/          # API kurulum ve credential dosyaları
├── 2_assets/         # Template görsel ve fontlar
├── 3_scripts/        # Python scriptleri
├── 4_n8n_workflows/  # n8n workflow JSON dosyaları
├── 5_tests/          # Test scriptleri ve çıktılar
└── 6_docs/           # Dokümantasyon
```

## 🚀 Hızlı Başlangıç

### 1. Python Environment

```bash
cd 3_scripts
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. API Kurulumu

`1_setup/facebook_instagram_setup.md` dosyasındaki adımları takip edin.

### 3. n8n Kurulumu

`1_setup/n8n_docker_setup.md` dosyasına bakın.

### 4. Test

```bash
cd 3_scripts
python menu_scraper.py
```

## 📖 Dokümantasyon

- [API Kurulum Rehberi](1_setup/facebook_instagram_setup.md)
- [n8n Docker Setup](1_setup/n8n_docker_setup.md)
- [Instagram API Guide](6_docs/instagram_api_guide.md)
- [Deployment](6_docs/deployment.md)
- [Troubleshooting](6_docs/troubleshooting.md)

## 🔧 Teknolojiler

- Python 3.x
- BeautifulSoup4 (Web scraping)
- Pillow (Image processing)
- n8n (Workflow automation)
- Instagram Graph API

## 📅 Çalışma Zamanı

Her gün Pazartesi-Cuma, saat 09:30'da otomatik çalışır.

## 👥 Ekip

MACS Kulübü - Eskişehir Osmangazi Üniversitesi

## 📄 Lisans

Bu proje MACS Kulübü için geliştirilmiştir.
