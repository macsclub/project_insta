"""
Facebook/Instagram Access Token Yenileme Scripti
Long-lived token'ları otomatik yeniler ve kaydeder
"""

import requests
import json
import sys
import os
from datetime import datetime, timedelta


class TokenRefresher:
    def __init__(self, credentials_path='../1_setup/api_credentials.json'):
        """Token yenileme sınıfı"""
        self.credentials_path = credentials_path
        self.credentials = self._load_credentials()
        self.base_url = "https://graph.facebook.com/v18.0"
    
    def _load_credentials(self):
        """Credential dosyasını yükle"""
        try:
            with open(self.credentials_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Hata: {self.credentials_path} bulunamadı", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Hata: JSON parse hatası - {e}", file=sys.stderr)
            sys.exit(1)
    
    def _save_credentials(self):
        """Güncellenmiş credentials'ı kaydet"""
        try:
            with open(self.credentials_path, 'w', encoding='utf-8') as f:
                json.dump(self.credentials, f, indent=2, ensure_ascii=False)
            print(f"✅ Credentials kaydedildi: {self.credentials_path}")
            return True
        except Exception as e:
            print(f"❌ Hata: Credentials kaydedilemedi - {e}", file=sys.stderr)
            return False
    
    def exchange_short_to_long_token(self, short_lived_token):
        """
        Kısa ömürlü token'ı uzun ömürlü token'a çevirir
        
        Args:
            short_lived_token: Graph API Explorer'dan alınan kısa ömürlü token
            
        Returns:
            dict: {'access_token': str, 'expires_in': int} veya None
        """
        print("🔄 Kısa ömürlü token uzun ömürlü token'a çevriliyor...")
        
        app_id = self.credentials['facebook']['app_id']
        app_secret = self.credentials['facebook']['app_secret']
        
        url = f"{self.base_url}/oauth/access_token"
        params = {
            'grant_type': 'fb_exchange_token',
            'client_id': app_id,
            'client_secret': app_secret,
            'fb_exchange_token': short_lived_token
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                expires_in = data.get('expires_in', 5184000)  # ~60 gün
                expires_date = datetime.now() + timedelta(seconds=expires_in)
                
                print(f"✅ Long-lived USER token alındı")
                print(f"   Geçerlilik süresi: {expires_in} saniye (~{expires_in//86400} gün)")
                print(f"   Son kullanma tarihi: {expires_date.strftime('%d.%m.%Y %H:%M')}")
                
                return data
            else:
                error_data = response.json()
                print(f"❌ Hata: {error_data.get('error', {}).get('message', 'Bilinmeyen hata')}")
                return None
                
        except Exception as e:
            print(f"❌ Hata: {e}", file=sys.stderr)
            return None
    
    def get_page_access_token(self, user_access_token):
        """
        User access token ile page access token alır
        
        Args:
            user_access_token: Long-lived user access token
            
        Returns:
            dict: {'access_token': str, 'page_id': str, 'page_name': str} veya None
        """
        print("\n📄 Page access token alınıyor...")
        
        url = f"{self.base_url}/me/accounts"
        params = {'access_token': user_access_token}
        
        try:
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                pages = data.get('data', [])
                
                if not pages:
                    print("❌ Hata: Hiç sayfa bulunamadı")
                    return None
                
                # Mevcut page_id ile eşleşen sayfayı bul
                current_page_id = self.credentials['facebook']['page_id']
                
                for page in pages:
                    if page['id'] == current_page_id:
                        print(f"✅ Page access token alındı")
                        print(f"   Sayfa: {page['name']}")
                        print(f"   Page ID: {page['id']}")
                        
                        return {
                            'access_token': page['access_token'],
                            'page_id': page['id'],
                            'page_name': page['name']
                        }
                
                # Eşleşme yoksa ilk sayfayı göster
                print(f"⚠️  Mevcut page_id ({current_page_id}) bulunamadı")
                print(f"   Kullanılabilir sayfalar:")
                for i, page in enumerate(pages, 1):
                    print(f"   {i}. {page['name']} (ID: {page['id']})")
                
                # İlk sayfayı kullan
                first_page = pages[0]
                print(f"\n✅ İlk sayfa kullanılacak: {first_page['name']}")
                
                return {
                    'access_token': first_page['access_token'],
                    'page_id': first_page['id'],
                    'page_name': first_page['name']
                }
            else:
                error_data = response.json()
                print(f"❌ Hata: {error_data.get('error', {}).get('message', 'Bilinmeyen hata')}")
                return None
                
        except Exception as e:
            print(f"❌ Hata: {e}", file=sys.stderr)
            return None
    
    def verify_instagram_connection(self, page_id, page_access_token):
        """
        Page'in Instagram hesabına bağlı olduğunu doğrula
        
        Args:
            page_id: Facebook Page ID
            page_access_token: Page access token
            
        Returns:
            str: Instagram Business Account ID veya None
        """
        print("\n📱 Instagram bağlantısı kontrol ediliyor...")
        
        url = f"{self.base_url}/{page_id}"
        params = {
            'fields': 'instagram_business_account',
            'access_token': page_access_token
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'instagram_business_account' in data:
                    ig_id = data['instagram_business_account']['id']
                    print(f"✅ Instagram hesabı bağlı")
                    print(f"   IG Business Account ID: {ig_id}")
                    return ig_id
                else:
                    print("❌ Bu Page'e bağlı Instagram Business hesabı yok")
                    return None
            else:
                error_data = response.json()
                print(f"❌ Hata: {error_data.get('error', {}).get('message', 'Bilinmeyen hata')}")
                return None
                
        except Exception as e:
            print(f"❌ Hata: {e}", file=sys.stderr)
            return None
    
    def refresh_token(self, short_lived_token):
        """
        Token yenileme işleminin tamamı
        
        Args:
            short_lived_token: Graph API Explorer'dan alınan token
            
        Returns:
            bool: Başarılı ise True
        """
        print("=" * 70)
        print("🔐 FACEBOOK/INSTAGRAM TOKEN YENİLEME")
        print("=" * 70)
        print(f"⏰ {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        print("=" * 70)
        print()
        
        # Adım 1: Short → Long User Token
        user_token_data = self.exchange_short_to_long_token(short_lived_token)
        if not user_token_data:
            return False
        
        user_access_token = user_token_data['access_token']
        
        # Adım 2: Page Access Token Al
        page_data = self.get_page_access_token(user_access_token)
        if not page_data:
            return False
        
        # Adım 3: Instagram Bağlantısını Doğrula
        ig_id = self.verify_instagram_connection(page_data['page_id'], page_data['access_token'])
        if not ig_id:
            print("\n⚠️  Instagram hesabı bağlı değil ama devam ediliyor...")
        
        # Adım 4: Credentials'ı Güncelle
        print("\n💾 Credentials güncelleniyor...")
        
        self.credentials['facebook']['page_access_token'] = page_data['access_token']
        self.credentials['facebook']['page_id'] = page_data['page_id']
        
        if ig_id:
            self.credentials['instagram']['business_account_id'] = ig_id
        
        # Kaydet
        if not self._save_credentials():
            return False
        
        # Özet
        print()
        print("=" * 70)
        print("✅ TOKEN YENİLEME BAŞARILI!")
        print("=" * 70)
        print(f"📄 Page: {page_data['page_name']}")
        print(f"🆔 Page ID: {page_data['page_id']}")
        if ig_id:
            print(f"📱 IG Business Account: {ig_id}")
        print(f"⏰ Yenilenme Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        print(f"📅 Tahmini Son Kullanma: {(datetime.now() + timedelta(days=60)).strftime('%d.%m.%Y')}")
        print("=" * 70)
        print()
        print("⚠️  NOT: Token'ı ~60 gün sonra tekrar yenilemeyi unutmayın!")
        print("=" * 70)
        
        return True


def main():
    """Ana fonksiyon"""
    print()
    print("🔐 Facebook/Instagram Token Yenileme Aracı")
    print()
    
    if len(sys.argv) > 1:
        # Komut satırından token verildi
        short_lived_token = sys.argv[1]
    else:
        # Kullanıcıdan token iste
        print("📝 Kısa ömürlü token'ı giriniz:")
        print()
        print("1. https://developers.facebook.com/tools/explorer/ adresine gidin")
        print("2. Uygulamanızı seçin")
        print("3. 'Get Page Access Token' butonuna tıklayın")
        print("4. Gerekli izinleri seçin:")
        print("   - pages_show_list")
        print("   - pages_read_engagement")
        print("   - instagram_basic")
        print("   - instagram_content_publish")
        print("5. 'Generate Access Token' butonuna tıklayın")
        print("6. Token'ı kopyalayıp buraya yapıştırın")
        print()
        
        short_lived_token = input("Token: ").strip()
        
        if not short_lived_token:
            print("❌ Token boş olamaz!")
            return 1
    
    # Token yenile
    refresher = TokenRefresher()
    success = refresher.refresh_token(short_lived_token)
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
