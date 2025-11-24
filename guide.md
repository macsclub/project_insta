📌 MACS - Instagram Yemekhane Menüsü Otomasyon Projesi
📣 1. Projenin Genel Açıklaması

Bu proje, MACS Kulübü’nün Instagram sayfasında her gün düzenli olarak paylaşılması gereken yemekhane menüsü hikâyesini tamamen otomatik hale getirmeyi amaçlar. Süreç, herhangi bir manuel müdahaleye ihtiyaç duyulmadan kendi kendine çalışacak şekilde tasarlanmıştır.

n8n otomasyon altyapısı kullanılarak, üniversitenin yemek menüsü web sitesinden veri çekilir, tasarım ekibinin hazırladığı PNG şablonun üzerine işlenir ve resmi Instagram Graph API üzerinden Instagram hikâyesi olarak paylaşılır.

Proje, haftaiçi her gün saat belirli bir vakitte tetiklenir ve çalışır.

🎯 2. Projenin Amacı

Bu projenin temel hedefi, MACS kulübünün sosyal medya paylaşım süreçlerini hızlandırmak, standartlaştırmak ve otomatikleştirmektir.

Projenin detaylı amaçları:

Her gün düzenli olarak yemek menüsü paylaşılmasını sağlamak.

Tasarım tutarlılığı için sabit bir görsel şablon kullanmak.

İnsan hatalarını, gecikmeleri ve manuel işlem yükünü ortadan kaldırmak.

Kulübün kurumsal sosyal medya yönetimini profesyonelleştirmek.

n8n üzerinden yönetilebilir, izlenebilir ve genişletilebilir bir otomasyon mimarisi oluşturmak.

🧩 3. Proje Bileşenleri

Bu proje 4 ana bileşenden oluşur:

1) Veri Kaynağı (Yemekhane Menüsü)

Üniversitenin resmi yemek menüsü web sayfasından günlük menü bilgisi çekilecektir.

Menü HTML olarak parse edilip metin formatında işlenecektir.

2) Tasarım Şablonu (PNG)

Tasarım Koordinatörlüğü tarafından hazırlanan 1080×1920 çözünürlüklü arka plan şablonu kullanılacaktır.

Menü metni, n8n'in Image Edit işlem adımlarıyla bu şablon üzerine otomatik olarak yazılacaktır.

3) n8n Otomasyon Altyapısı

Aşağıdaki nodelarla bir akış oluşturulacaktır:

Cron Node (Tetkileyici)

HTTP Request Node (Menü Çekme)

HTML Extract / Function Node (Menü ayıklama ve düzenleme)

Read Binary File Node (Tasarım şablonu)

Image Edit Node (Metin bindirme)

Instagram Graph API Node (Fotoğrafı hikâye olarak yükleme)

4) Instagram API Entegrasyonu

Instagram Business hesabı

Facebook Page bağlantısı

Facebook Developer App

Long-lived Page Access Token

IG User ID ve Page ID

🚀 4. Yol Haritası (Roadmap)

Proje 4 fazda tamamlanacaktır.

🟦 Faz 1 — Hazırlık (Instagram + Facebook + Developer tarafı)

Instagram hesabının Business/Professional formata geçirilmesi

IG hesabının bir Facebook Page ile eşleştirilmesi

Facebook Developer hesabının açılması

"Business" türünde bir uygulama oluşturulması

Instagram Graph API ürününün etkinleştirilmesi

Long-lived Page Access Token oluşturulması

IG User ID, Page ID, App ID ve App Secret bilgilerinin elde edilmesi

Çıktı: API için gerekli tüm kimlik bilgileri hazır.

🟩 Faz 2 — n8n Workflow İskeletinin Kurulması

Cron Node eklenerek çalışma saatlerinin belirlenmesi (örneğin 09:30, hafta içi)

HTTP Request Node ile üniversitenin menü sayfasından HTML verisinin çekilmesi

HTML içinden menü öğelerinin ayıklanması için HTML Extract veya Function Node hazırlanması

Menü metninin formatlanması, temizlenmesi, boş gün yönetimi gibi senaryoların tasarlanması

Çıktı: Menü otomatik olarak webden okunur ve işlenmiş hale gelir.

🟨 Faz 3 — Görsel Oluşturma (Template Üzerine Menü Yazma)

Tasarım ekibinden gelen 1080×1920 PNG şablonunun n8n'e binary olarak eklenmesi

Image Edit Node ile metin bindirme (font, renk, pozisyon, satır aralığı)

Hikâye formatına uygun final görselin oluşturulması

Çıktı: Menü yazısı işlenmiş, Instagram hikâyesine hazır görsel.

🟥 Faz 4 — Instagram Hikâye Yükleme (Graph API)

n8n üzerinde Instagram Graph API credential oluşturulması

/media endpoint'i ile görsel yüklenmesi ve media_id alınması

/media_publish endpoint'i ile hikâye olarak yayınlanması

Gerekirse hata yönetimi ve Discord bildirim entegrasyonu

Çıktı: Menü görseli Instagram'a her gün otomatik olarak hikâye şeklinde yüklenir.

📦 5. Genel Akışın Teknik Özeti
CRON (Mon–Fri 09:30)
       ↓
HTTP Request (Yemekhane menü HTML)
       ↓
HTML Extract → Temiz Menü Metni
       ↓
Function Node (Formatlama)
       ↓
Read Binary File (Template PNG)
       ↓
Image Edit Node (Metni tasarıma ekle)
       ↓
Instagram Graph API – Upload (media_id al)
       ↓
Instagram Graph API – Publish Story
       ↓
(Opsiyonel) Discord Webhook – "Paylaşıldı" bildirimi
✔ 6. Sonuç

Bu proje tamamlandığında, MACS kulübü sosyal medya yönetimi için tamamen otomatik bir altyapıya sahip olacaktır. İnsan hatası, gecikme veya unutma olmadan; her gün düzenli, profesyonel ve estetik hikâyeler Instagram'da yayınlanacaktır.

Bu sistem genişletilebilir, başka projelere bağlanabilir ve kulübün dijital ekosisteminin önemli bir parçası hâline gelebilir.