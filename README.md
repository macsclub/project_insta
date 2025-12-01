# 📸 Instagram Yemekhane Menüsü Otomasyon Projesi

MACS Kulübü için otomatik Instagram hikayesi paylaşım sistemi.

## 🎯 Proje Amacı

Bu proje, Eskişehir Osmangazi Üniversitesi yemekhane menüsünü otomatik olarak çekip, tasarım şablonu üzerine işleyerek Instagram story olarak paylaşır.

## 📁 Proje Yapısı

```
project_insta/
├── 1_setup/              # API kurulum ve credential dosyaları
├── 2_assets/             # Template görsel ve fontlar
├── 3_scripts/            # Python scriptleri ve API
│   ├── api_server.py     # FastAPI sunucusu
│   ├── menu_scraper.py   # Menü çekme
│   ├── text_formatter.py # Metin formatlama
│   ├── image_generator.py# Görsel oluşturma
│   ├── config.py         # Konfigürasyon
│   ├── Dockerfile        # Python API Docker image
│   └── requirements.txt  # Python bağımlılıkları
├── 4_n8n_workflows/      # n8n workflow JSON dosyaları
├── 5_tests/              # Test scriptleri ve çıktılar
├── 6_docs/               # Dokümantasyon
├── output/               # Docker output klasörü
├── docker-compose.yml    # Docker Compose (n8n + Python API)
└── .env                  # Environment variables (gitignore'da)
```

## 🚀 Hızlı Başlangıç

### Gereksinimler

- Docker & Docker Compose
- Instagram Business Hesabı
- Facebook Developer App
- ImgBB API Key (ücretsiz)

### 1. Repository'yi Klonlayın

```bash
git clone https://github.com/macsclub/project_insta.git
cd project_insta
```

### 2. Environment Değişkenlerini Ayarlayın

```bash
cp .env.example .env
# .env dosyasını düzenleyin ve IMGBB_API_KEY'i ekleyin
```

### 3. Docker ile Başlatın

```bash
docker-compose up -d
```

### 4. Servislere Erişin

- **n8n**: http://localhost:5678
- **Python API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🔧 Mimari

```
┌─────────────┐      ┌─────────────────┐      ┌─────────────┐
│   n8n       │─────▶│   Python API    │─────▶│  Instagram  │
│   (Cron)    │      │   (FastAPI)     │      │  Graph API  │
└─────────────┘      └─────────────────┘      └─────────────┘
                            │
                            ▼
                     ┌─────────────┐
                     │   ImgBB     │
                     │ (Public URL)│
                     └─────────────┘
```

## 📡 API Endpoints

| Endpoint | Method | Açıklama |
|----------|--------|----------|
| `/health` | GET | API sağlık kontrolü |
| `/api/menu` | GET | Günün menüsünü JSON olarak döndürür |
| `/api/generate-story` | POST | Menü görseli oluşturur (lokal URL) |
| `/api/generate-story-public` | POST | Menü görseli oluşturur ve ImgBB'ye yükler |
| `/static/{filename}` | GET | Oluşturulan görselleri sunar |

## ⚙️ Konfigürasyon

### Environment Variables

| Değişken | Açıklama | Varsayılan |
|----------|----------|------------|
| `IMGBB_API_KEY` | ImgBB API anahtarı | - |
| `API_BASE_URL` | API'nin public URL'si | `http://localhost:8000` |
| `ASSETS_DIR` | Template görsellerin yolu | `/app/assets` |
| `OUTPUT_DIR` | Çıktı klasörü | `/app/output` |

## 📅 Otomasyon

n8n workflow'u şu şekilde çalışır:

1. **Schedule Trigger**: Pazartesi-Cuma 09:30
2. **HTTP Request**: Python API'yi çağırır
3. **IF**: Başarı kontrolü
4. **Instagram API**: Media container oluşturur
5. **Instagram API**: Story olarak yayınlar

## 🔧 Teknolojiler

- **Python 3.10** - Backend
- **FastAPI** - REST API
- **BeautifulSoup4** - Web scraping
- **Pillow** - Image processing
- **n8n** - Workflow automation
- **Docker** - Containerization
- **Instagram Graph API** - Story paylaşımı
- **ImgBB** - Image hosting

## 📖 Dokümantasyon

- [Facebook/Instagram API Kurulumu](1_setup/facebook_instagram_setup.md)
- [n8n Docker Setup](1_setup/n8n_docker_setup.md)
- [Instagram API Guide](6_docs/instagram_api_guide.md)
- [Deployment](6_docs/deployment.md)
- [Troubleshooting](6_docs/troubleshooting.md)

## 🧪 Lokal Test

```bash
# Python API'yi lokal çalıştırma
cd 3_scripts
pip install -r requirements.txt
python api_server.py

# Test endpoint
curl -X POST http://localhost:8000/api/generate-story-public
```

## 👥 Ekip

**MACS Kulübü** - Eskişehir Osmangazi Üniversitesi

## 📄 Lisans

Bu proje MACS Kulübü için geliştirilmiştir.
