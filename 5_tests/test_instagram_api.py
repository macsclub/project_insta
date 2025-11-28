"""
Instagram Graph API Test Script
API credentials ve endpoint'lerin çalışıp çalışmadığını test eder
"""

import requests
import json
import sys
import os
from datetime import datetime


class InstagramAPITester:
    def __init__(self, credentials_path='../1_setup/api_credentials.json'):
        """Instagram API test sınıfı"""
        self.credentials = self._load_credentials(credentials_path)
        self.access_token = self.credentials['facebook']['page_access_token']
        self.ig_user_id = self.credentials['instagram']['business_account_id']
        self.page_id = self.credentials['facebook']['page_id']
        self.app_id = self.credentials['facebook']['app_id']
        self.base_url = "https://graph.facebook.com/v18.0"
        
        self.test_results = []
    
    def _load_credentials(self, path):
        """Credential dosyasını yükle"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Hata: {path} bulunamadı", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Hata: JSON parse hatası - {e}", file=sys.stderr)
            sys.exit(1)
    
    def _add_result(self, test_name, success, message, details=None):
        """Test sonucunu kaydet"""
        result = {
            'test': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        if details:
            result['details'] = details
        
        self.test_results.append(result)
        
        status = "✅" if success else "❌"
        print(f"{status} {test_name}: {message}")
        if details and not success:
            print(f"   Detay: {details}")
    
    def test_1_credentials_loaded(self):
        """Test 1: Credentials başarıyla yüklendi mi?"""
        try:
            required_fields = {
                'Access Token': self.access_token,
                'IG User ID': self.ig_user_id,
                'Page ID': self.page_id,
                'App ID': self.app_id
            }
            
            missing = [k for k, v in required_fields.items() if not v or v.startswith('YOUR_')]
            
            if missing:
                self._add_result(
                    "Credentials Yükleme",
                    False,
                    f"Eksik veya placeholder değerler: {', '.join(missing)}",
                    required_fields
                )
            else:
                self._add_result(
                    "Credentials Yükleme",
                    True,
                    "Tüm credentials başarıyla yüklendi"
                )
                return True
        except Exception as e:
            self._add_result("Credentials Yükleme", False, str(e))
        
        return False
    
    def test_2_access_token_validity(self):
        """Test 2: Access Token geçerli mi?"""
        try:
            url = f"{self.base_url}/me"
            params = {'access_token': self.access_token}
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self._add_result(
                    "Access Token Geçerliliği",
                    True,
                    f"Token geçerli - Page: {data.get('name', 'N/A')}",
                    data
                )
                return True
            else:
                error_data = response.json()
                self._add_result(
                    "Access Token Geçerliliği",
                    False,
                    f"HTTP {response.status_code}",
                    error_data
                )
        except Exception as e:
            self._add_result("Access Token Geçerliliği", False, str(e))
        
        return False
    
    def test_3_ig_user_id_validation(self):
        """Test 3: Instagram User ID doğru mu?"""
        try:
            url = f"{self.base_url}/{self.ig_user_id}"
            params = {
                'fields': 'id,username,profile_picture_url',
                'access_token': self.access_token
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self._add_result(
                    "IG User ID Doğrulama",
                    True,
                    f"Instagram hesabı: @{data.get('username', 'N/A')}",
                    data
                )
                return True
            else:
                error_data = response.json()
                self._add_result(
                    "IG User ID Doğrulama",
                    False,
                    f"HTTP {response.status_code}",
                    error_data
                )
        except Exception as e:
            self._add_result("IG User ID Doğrulama", False, str(e))
        
        return False
    
    def test_4_page_instagram_connection(self):
        """Test 4: Facebook Page - Instagram bağlantısı var mı?"""
        try:
            url = f"{self.base_url}/{self.page_id}"
            params = {
                'fields': 'instagram_business_account',
                'access_token': self.access_token
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'instagram_business_account' in data:
                    connected_ig_id = data['instagram_business_account']['id']
                    
                    if connected_ig_id == self.ig_user_id:
                        self._add_result(
                            "Page-Instagram Bağlantısı",
                            True,
                            "Facebook Page ve Instagram hesabı doğru şekilde bağlı",
                            data
                        )
                        return True
                    else:
                        self._add_result(
                            "Page-Instagram Bağlantısı",
                            False,
                            f"IG User ID uyuşmazlığı: {connected_ig_id} != {self.ig_user_id}",
                            data
                        )
                else:
                    self._add_result(
                        "Page-Instagram Bağlantısı",
                        False,
                        "Facebook Page'e bağlı Instagram hesabı yok",
                        data
                    )
            else:
                error_data = response.json()
                self._add_result(
                    "Page-Instagram Bağlantısı",
                    False,
                    f"HTTP {response.status_code}",
                    error_data
                )
        except Exception as e:
            self._add_result("Page-Instagram Bağlantısı", False, str(e))
        
        return False
    
    def test_5_api_permissions(self):
        """Test 5: Gerekli API izinleri var mı?"""
        try:
            url = f"{self.base_url}/me/permissions"
            params = {'access_token': self.access_token}
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                permissions = {p['permission']: p['status'] for p in data.get('data', [])}
                
                required_permissions = [
                    'instagram_basic',
                    'instagram_content_publish',
                    'pages_show_list',
                    'pages_read_engagement'
                ]
                
                granted = [p for p in required_permissions if permissions.get(p) == 'granted']
                missing = [p for p in required_permissions if permissions.get(p) != 'granted']
                
                if not missing:
                    self._add_result(
                        "API İzinleri",
                        True,
                        f"Tüm gerekli izinler verilmiş ({len(granted)}/{len(required_permissions)})",
                        {'granted': granted}
                    )
                    return True
                else:
                    self._add_result(
                        "API İzinleri",
                        False,
                        f"Eksik izinler: {', '.join(missing)}",
                        {'granted': granted, 'missing': missing}
                    )
            else:
                error_data = response.json()
                self._add_result(
                    "API İzinleri",
                    False,
                    f"HTTP {response.status_code}",
                    error_data
                )
        except Exception as e:
            self._add_result("API İzinleri", False, str(e))
        
        return False
    
    def test_6_rate_limit_check(self):
        """Test 6: Rate limit durumu"""
        try:
            url = f"{self.base_url}/{self.ig_user_id}"
            params = {'access_token': self.access_token}
            
            response = requests.get(url, params=params, timeout=10)
            
            # Rate limit header'ları kontrol et
            rate_limit_headers = {
                'X-Business-Use-Case-Usage': response.headers.get('X-Business-Use-Case-Usage'),
                'X-App-Usage': response.headers.get('X-App-Usage'),
                'X-Ad-Account-Usage': response.headers.get('X-Ad-Account-Usage')
            }
            
            self._add_result(
                "Rate Limit Kontrolü",
                True,
                "Rate limit bilgileri alındı",
                rate_limit_headers
            )
            return True
            
        except Exception as e:
            self._add_result("Rate Limit Kontrolü", False, str(e))
        
        return False
    
    def run_all_tests(self):
        """Tüm testleri sırayla çalıştır"""
        print("=" * 70)
        print("🧪 INSTAGRAM GRAPH API TEST SUITE")
        print("=" * 70)
        print(f"⏰ Test Zamanı: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        print(f"📱 Instagram User ID: {self.ig_user_id}")
        print(f"📄 Page ID: {self.page_id}")
        print("=" * 70)
        print()
        
        # Testleri çalıştır
        self.test_1_credentials_loaded()
        self.test_2_access_token_validity()
        self.test_3_ig_user_id_validation()
        self.test_4_page_instagram_connection()
        self.test_5_api_permissions()
        self.test_6_rate_limit_check()
        
        # Özet
        print()
        print("=" * 70)
        print("📊 TEST SONUÇLARI")
        print("=" * 70)
        
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r['success'])
        failed = total - passed
        
        print(f"✅ Başarılı: {passed}/{total}")
        print(f"❌ Başarısız: {failed}/{total}")
        print(f"📈 Başarı Oranı: {(passed/total*100):.1f}%")
        
        # JSON çıktısı
        print("\n📦 JSON Çıktısı:")
        print(json.dumps({
            'summary': {
                'total': total,
                'passed': passed,
                'failed': failed,
                'success_rate': f"{(passed/total*100):.1f}%"
            },
            'tests': self.test_results
        }, indent=2, ensure_ascii=False))
        
        print("=" * 70)
        
        return passed == total


def main():
    """Ana fonksiyon"""
    try:
        tester = InstagramAPITester()
        success = tester.run_all_tests()
        
        return 0 if success else 1
        
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
