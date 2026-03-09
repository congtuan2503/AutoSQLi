"""
Base Scraper Class - Lớp cơ sở cho tất cả scrapers
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import requests
from datetime import datetime


class BaseScraper(ABC):
    """Lớp cơ sở cho tất cả scrapers"""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    @abstractmethod
    def scrape(self) -> List[Dict[str, Any]]:
        """
        Cào dữ liệu từ nguồn
        Returns: List of payloads/techniques
        """
        pass
    
    @abstractmethod
    def get_source_name(self) -> str:
        """Returns: Tên nguồn dữ liệu"""
        pass
    
    def _make_request(self, url: str) -> str:
        """Thực hiện HTTP request"""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Lỗi khi cào {url}: {e}")
            return ""
    
    def _parse_payload(self, payload_str: str, category: str = "unknown") -> Dict[str, Any]:
        """Parse một payload thành Dict"""
        return {
            "payload": payload_str.strip(),
            "category": category,
            "source": self.get_source_name(),
            "discovered_at": datetime.now().isoformat(),
            "verified": False
        }
    
    def log_scrape(self, count: int):
        """Log thông tin scraping"""
        print(f"[{self.get_source_name()}] Cào được {count} payloads/techniques", flush=True)


class TechniqueScraper(BaseScraper):
    """Scraper cho techniques và bypass methods"""
    
    def parse_technique(self, name: str, description: str, technique_type: str) -> Dict[str, Any]:
        """Parse một technique"""
        return {
            "name": name,
            "description": description,
            "type": technique_type,
            "source": self.get_source_name(),
            "discovered_at": datetime.now().isoformat()
        }
