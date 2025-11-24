"""
Instagram Uploader - Graph API ile Story Upload
"""

import requests
import json
import os
import sys
import time


class InstagramUploader:
    def __init__(self, credentials_path='../1_setup/api_credentials.json'):
        """Instagram Graph API uploader"""
        self.credentials = self._load_credentials(credentials_path)
        self.access_token = self.credentials['facebook']['page_access_token']
        self.ig_user_id = self.credentials['instagram']['business_account_id']
        self.base_url = "https://graph.facebook.com/v18.0"
    
    def _load_credentials(self, path):
        """Credential dosyasını yükle"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Hata: {path} bulunamadı", file=sys.stderr)
            print("   api_credentials.example.json'u kopyalayıp doldurun", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Hata: JSON parse hatası - {e}", file=sys.stderr)
            sys.exit(1)
    
    def upload_story(self, image_path):
        """
        Instagram'a story olarak fotoğraf yükler
        
        Args:
            image_path: Yüklenecek görsel dosya yolu
            
        Returns:
            dict: API yanıtı (başarılı ise story ID)
        """
        
        if not os.path.exists(image_path):
            print(f"❌ Hata: Görsel bulunamadı - {image_path}", file=sys.stderr)
            return None
        
        print(f"📤 Story yükleniyor: {image_path}")
        
        # ADIM 1: Media Container Oluştur
        media_id = self._create_media_container(image_path)
        if not media_id:
            return None
        
        # ADIM 2: Story Olarak Yayınla
        result = self._publish_story(media_id)
        return result
    
    def _create_media_container(self, image_path):
        """
        Instagram Graph API ile media container oluşturur
        NOT: Görsel public bir URL'de olmalı veya binary olarak gönderilmeli
        """
        
        # Görsel dosyasını oku
        print("   1️⃣ Media container oluşturuluyor...")
        
        # NOT: Instagram Graph API görseli bir URL'den çeker
        # Lokal dosya için önce bir public URL'e yüklemeniz gerekir
        # Alternatif: n8n içinde Binary Data kullanabilirsiniz
        
        # Burada basit test için dosya yolunu gösteriyoruz
        # Production'da image_url parametresi kullanılmalı
        
        endpoint = f"{self.base_url}/{self.ig_user_id}/media"
        
        # Test için: Görselİ base64 veya multipart ile gönderme yerine
        # image_url kullanmanız gerekiyor (public erişilebilir)
        
        print("   ⚠️  NOT: Instagram API görseli public URL'den ister")
        print("   ⚠️  Production'da görseli bir sunucuya yükleyin veya")
        print("   ⚠️  n8n Binary Data kullanın")
        
        # Örnek payload (gerçek kullanımda image_url gerekli)
        payload = {
            'access_token': self.access_token,
            # 'image_url': 'https://example.com/story.png',  # Public URL gerekli
            # 'caption': 'BUGÜNÜN MENÜSÜ'  # Opsiyonel
        }
        
        # Şimdilik test için placeholder
        print("   ⚠️  Mock mode: API çağrısı simüle ediliyor")
        print(f"   IG User ID: {self.ig_user_id}")
        print(f"   Access Token: {self.access_token[:20]}...")
        
        # return "MOCK_MEDIA_ID_12345"  # Test için
        
        # Gerçek API çağrısı (image_url gerekli)
        try:
            response = requests.post(endpoint, data=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if 'id' in data:
                media_id = data['id']
                print(f"   ✅ Media ID alındı: {media_id}")
                return media_id
            else:
                print(f"   ❌ Hata: Media ID alınamadı - {data}", file=sys.stderr)
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ API Hatası: {e}", file=sys.stderr)
            return None
    
    def _publish_story(self, media_id):
        """Media ID'yi kullanarak story olarak yayınlar"""
        
        print("   2️⃣ Story yayınlanıyor...")
        
        endpoint = f"{self.base_url}/{self.ig_user_id}/media_publish"
        
        payload = {
            'creation_id': media_id,
            'access_token': self.access_token
        }
        
        try:
            response = requests.post(endpoint, data=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if 'id' in data:
                story_id = data['id']
                print(f"   ✅ Story yayınlandı! ID: {story_id}")
                return {
                    'success': True,
                    'story_id': story_id,
                    'media_id': media_id
                }
            else:
                print(f"   ❌ Hata: Story yayınlanamadı - {data}", file=sys.stderr)
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ API Hatası: {e}", file=sys.stderr)
            return None


def main():
    """Test amaçlı ana fonksiyon"""
    
    print("📱 Instagram Uploader Test")
    print("=" * 60)
    
    # Credentials kontrol
    uploader = InstagramUploader()
    
    print(f"✅ Credentials yüklendi")
    print(f"   IG User ID: {uploader.ig_user_id}")
    print(f"   Access Token: {uploader.access_token[:30]}...")
    
    # Örnek görsel yolu
    image_path = '../5_tests/output/story.png'
    
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    
    print(f"\n📸 Yüklenecek görsel: {image_path}")
    
    # Upload et
    result = uploader.upload_story(image_path)
    
    if result:
        print("\n" + "=" * 60)
        print("🎉 Başarılı!")
        print(json.dumps(result, indent=2))
    else:
        print("\n❌ Upload başarısız")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
