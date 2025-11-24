# n8n Docker Kurulum ve Kullanım

## 📦 n8n Docker ile Başlatma

Eğer n8n'i daha önce kurmadıysanız:

```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  docker.n8n.io/n8nio/n8n
```

Windows için:

```cmd
docker run -it --rm --name n8n -p 5678:5678 -v %USERPROFILE%\.n8n:/home/node/.n8n docker.n8n.io/n8nio/n8n
```

---

## 🌐 n8n'e Erişim

Tarayıcıdan: http://localhost:5678

---

## 📝 Workflow İçe Aktarma

1. n8n arayüzünü aç
2. Sol üst köşe → "Import from File"
3. `4_n8n_workflows/workflow_v1.json` dosyasını seç
4. Workflow otomatik olarak yüklenecek

---

## 🔧 Credential Ayarlama

n8n içinde Instagram API için credential oluşturmanız gerekecek:

1. Credentials → Add Credential
2. "Instagram" ara
3. Access Token ve diğer bilgileri gir
4. Save

---

## ⏰ Cron Schedule

Workflow'da Cron trigger node'unu şu şekilde ayarlayın:

- **Dakika:** 30
- **Saat:** 09
- **Gün:** 1-5 (Pazartesi-Cuma)
- **Timezone:** Europe/Istanbul

---

## 🧪 Manuel Test

Workflow'u test etmek için:

1. Workflow'u aç
2. Sol üstteki "Execute Workflow" butonuna tıkla
3. Sonuçları kontrol et

---

## 📊 Logları İzleme

Docker container loglarını görmek için:

```bash
docker logs -f n8n
```

---

## 🛑 n8n'i Durdurma

```bash
docker stop n8n
```
