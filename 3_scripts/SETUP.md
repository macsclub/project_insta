# Python Sanal Ortam Kurulumu

## Python 3.10.11 için Sanal Ortam Oluşturma

### Adım 1: Python Versiyonunu Kontrol Et

```cmd
python --version
```

Çıktı: `Python 3.10.11` olmalı

---

### Adım 2: 3_scripts Klasörüne Git

```cmd
cd c:\Users\thega\Desktop\MACS\Projeler\Aktif Projeler\project_instagram\3_scripts
```

---

### Adım 3: Sanal Ortam Oluştur

```cmd
python -m venv venv
```

Bu komut `venv` adında bir klasör oluşturur. İçinde Python 3.10.11 ve pip bulunur.

---

### Adım 4: Sanal Ortamı Aktifleştir

**Windows (cmd):**
```cmd
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

Aktif olunca terminal başında `(venv)` yazısı görünür:
```
(venv) C:\Users\thega\...\3_scripts>
```

---

### Adım 5: pip'i Güncelle

```cmd
python -m pip install --upgrade pip
```

---

### Adım 6: Kütüphaneleri Yükle

```cmd
pip install -r requirements.txt
```

Bu komut `requirements.txt` dosyasındaki tüm kütüphaneleri yükler.

---

### Adım 7: Kurulumu Kontrol Et

```cmd
pip list
```

Çıktıda şunları görmelisiniz:
- beautifulsoup4
- requests
- Pillow
- lxml
- python-dotenv
- python-dateutil

---

## Sanal Ortamdan Çıkma

```cmd
deactivate
```

---

## Her Seferinde Yapılacaklar

Projede çalışmaya başlarken:

1. Terminal'i aç
2. 3_scripts klasörüne git:
   ```cmd
   cd c:\Users\thega\Desktop\MACS\Projeler\Aktif Projeler\project_instagram\3_scripts
   ```
3. Sanal ortamı aktifleştir:
   ```cmd
   venv\Scripts\activate
   ```
4. Kodları çalıştır

---

## Hata Giderme

### "venv\Scripts\activate.ps1 cannot be loaded" hatası (PowerShell)

PowerShell'de execution policy hatası. Çözüm:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Sonra tekrar:
```powershell
venv\Scripts\Activate.ps1
```

### Python bulunamadı

PATH'e Python ekli değil. Çözüm:
- Python'u tam path ile kullan: `C:\Python310\python.exe -m venv venv`

### pip install hataları

İnternet bağlantısını kontrol edin veya şu komutu deneyin:
```cmd
pip install --no-cache-dir -r requirements.txt
```

---

## Sanal Ortamı Silme

Eğer baştan kurmak isterseniz:

```cmd
deactivate
rmdir /s /q venv
```

Sonra tekrar Adım 3'ten başlayın.
