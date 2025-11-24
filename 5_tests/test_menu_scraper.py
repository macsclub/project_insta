"""
Menu Scraper Unit Tests
pytest ile menü scraper testleri
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch, mock_open
import json

# Script dizinini path'e ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '3_scripts'))

from menu_scraper import MenuScraper


class TestMenuScraper:
    """MenuScraper sınıfı için testler"""
    
    @pytest.fixture
    def scraper(self):
        """Her test için yeni scraper instance'ı"""
        return MenuScraper()
    
    @pytest.fixture
    def sample_html(self):
        """Örnek HTML içeriği"""
        return """
        <html>
        <body>
            <div class="bugun yemek-menu-col">
                <div class="panel-heading">
                    <h3 class="panel-title">
                        <span class="yemek-menu-ay">24 Kas. Pazartesi</span>
                    </h3>
                </div>
                <div class="panel-body">
                    <ul class="list-unstyled yemek-menu-liste">
                        <li>
                            <span class="yemek-menu-yemek">
                                <a>ERİŞTELİ YEŞİL MERCİMEK ÇORBA</a>
                            </span>
                            <span class="yemek-menu-kalori">(170 kcal)</span>
                        </li>
                        <li>
                            <span class="yemek-menu-yemek">
                                <a>ETLİ MEVSİM TÜRLÜSÜ</a>
                            </span>
                            <span class="yemek-menu-kalori">(295 kcal)</span>
                        </li>
                    </ul>
                </div>
            </div>
        </body>
        </html>
        """
    
    @pytest.fixture
    def empty_html(self):
        """Menü olmayan HTML"""
        return """
        <html>
        <body>
            <div class="yemek-menu-col">
                <div class="panel-heading">
                    <h3 class="panel-title">
                        <span class="yemek-menu-ay">26 Kas. Cumartesi</span>
                    </h3>
                </div>
            </div>
        </body>
        </html>
        """
    
    def test_scraper_initialization(self, scraper):
        """Scraper doğru initialize edildi mi?"""
        assert scraper.url == "https://yemekhane.ogu.edu.tr/"
        assert 'User-Agent' in scraper.headers
    
    @patch('menu_scraper.requests.get')
    def test_fetch_page_success(self, mock_get, scraper):
        """Başarılı sayfa çekme testi"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"<html>Test</html>"
        mock_get.return_value = mock_response
        
        result = scraper.fetch_page()
        
        assert result == b"<html>Test</html>"
        mock_get.assert_called_once()
    
    @patch('menu_scraper.requests.get')
    def test_fetch_page_failure(self, mock_get, scraper):
        """Başarısız sayfa çekme testi (HTTP hatası)"""
        import requests
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")
        
        result = scraper.fetch_page()
        
        assert result is None
    
    def test_parse_menu_success(self, scraper, sample_html):
        """Başarılı menü parse testi"""
        result = scraper.parse_menu(sample_html)
        
        assert result is not None
        assert result['tarih'] == "24 Kas. Pazartesi"
        assert len(result['yemekler']) == 2
        assert result['yemekler'][0]['isim'] == "ERİŞTELİ YEŞİL MERCİMEK ÇORBA"
        assert result['yemekler'][0]['kalori'] == "(170 kcal)"
        assert result['menu_tipi'] == "Standart Menü"
    
    def test_parse_menu_empty(self, scraper, empty_html):
        """Boş menü parse testi (bugün class'ı yok)"""
        result = scraper.parse_menu(empty_html)
        
        assert result is None
    
    def test_parse_menu_invalid_html(self, scraper):
        """Geçersiz HTML testi"""
        invalid_html = "<html><body>Invalid content</body></html>"
        result = scraper.parse_menu(invalid_html)
        
        assert result is None
    
    @patch('builtins.open', new_callable=mock_open)
    def test_save_to_json_success(self, mock_file, scraper):
        """JSON kaydetme başarılı testi"""
        menu_data = {
            'tarih': '24 Kas. Pazartesi',
            'yemekler': [{'isim': 'Test', 'kalori': '100'}]
        }
        
        result = scraper.save_to_json(menu_data, 'test.json')
        
        assert result is True
        mock_file.assert_called_once_with('test.json', 'w', encoding='utf-8')
    
    @patch('builtins.open')
    def test_save_to_json_failure(self, mock_file, scraper):
        """JSON kaydetme başarısız testi"""
        mock_file.side_effect = Exception("Write error")
        menu_data = {'tarih': 'test'}
        
        result = scraper.save_to_json(menu_data, 'test.json')
        
        assert result is False


class TestMenuScraperIntegration:
    """Integration testleri"""
    
    @pytest.fixture
    def scraper(self):
        return MenuScraper()
    
    @pytest.fixture
    def sample_html(self):
        """Örnek HTML içeriği"""
        return """
        <html>
        <body>
            <div class="bugun yemek-menu-col">
                <div class="panel-heading">
                    <h3 class="panel-title">
                        <span class="yemek-menu-ay">24 Kas. Pazartesi</span>
                    </h3>
                </div>
                <div class="panel-body">
                    <ul class="list-unstyled yemek-menu-liste">
                        <li>
                            <span class="yemek-menu-yemek">
                                <a>ERİŞTELİ YEŞİL MERCİMEK ÇORBA</a>
                            </span>
                            <span class="yemek-menu-kalori">(170 kcal)</span>
                        </li>
                        <li>
                            <span class="yemek-menu-yemek">
                                <a>ETLİ MEVSİM TÜRLÜSÜ</a>
                            </span>
                            <span class="yemek-menu-kalori">(295 kcal)</span>
                        </li>
                    </ul>
                </div>
            </div>
        </body>
        </html>
        """
    
    @patch('menu_scraper.requests.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_full_workflow(self, mock_file, mock_get, scraper, sample_html):
        """Tüm workflow testi (fetch -> parse -> save)"""
        # Mock HTTP response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = sample_html.encode('utf-8')
        mock_get.return_value = mock_response
        
        # Menü çek
        menu_data = scraper.get_todays_menu()
        
        # Kontroller
        assert menu_data is not None
        assert 'tarih' in menu_data
        assert 'yemekler' in menu_data
        assert len(menu_data['yemekler']) > 0


# Parametrize edilmiş testler
class TestMenuScraperEdgeCases:
    """Edge case testleri"""
    
    @pytest.fixture
    def scraper(self):
        return MenuScraper()
    
    @pytest.mark.parametrize("html_content,expected_result", [
        # Boş yemek listesi
        ('<div class="bugun"><ul class="yemek-menu-liste"></ul></div>', []),
        # Tek yemek
        ('<div class="bugun"><ul class="yemek-menu-liste"><li><span class="yemek-menu-yemek"><a>Test</a></span></li></ul></div>', ['Test']),
    ])
    def test_various_menu_formats(self, scraper, html_content, expected_result):
        """Farklı menü formatları testi"""
        html = f"<html><body>{html_content}</body></html>"
        result = scraper.parse_menu(html)
        
        if expected_result:
            assert result is not None
            # İlk yemeğin ismini kontrol et
            if result['yemekler']:
                assert result['yemekler'][0]['isim'] in expected_result[0]


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
