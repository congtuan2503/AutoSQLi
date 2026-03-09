"""
OWASP SQL Injection Scraper
Cào SQL Injection techniques từ OWASP resources
"""

from typing import List, Dict, Any
from .base import BaseScraper
import re
from html.parser import HTMLParser


class OWASPScraper(BaseScraper):
    """Scraper cho OWASP SQL Injection Cheat Sheet"""
    
    # OWASP cheat sheet thường được lưu ở GitHub
    OWASP_GITHUB_URL = "https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/SQL%20Injection"
    OWASP_CHEATSHEET_URL = "https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html"
    
    def get_source_name(self) -> str:
        return "OWASP"
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Cào OWASP SQL Injection techniques"""
        payloads = []
        
        # Cào từ PayloadsAllTheThings
        payloads.extend(self._scrape_payloads_all_things())
        
        # Cào basic techniques
        payloads.extend(self._get_basic_techniques())
        
        self.log_scrape(len(payloads))
        return payloads
    
    def _scrape_payloads_all_things(self) -> List[Dict[str, Any]]:
        """Cào từ PayloadsAllTheThings repo"""
        payloads = []
        
        try:
            # README từ SQL Injection folder
            url = self.OWASP_GITHUB_URL + "/README.md"
            content = self._make_request(url)
            
            if not content:
                return payloads
            
            # Extract payloads từ code blocks
            code_blocks = re.findall(r'```.*?\n(.*?)\n```', content, re.DOTALL)
            
            for block in code_blocks[:20]:  # Limit 20 blocks
                for line in block.split('\n'):
                    line = line.strip()
                    if line and ('SELECT' in line.upper() or 'UNION' in line.upper()):
                        payloads.append(self._parse_payload(line, "union_based"))
        
        except Exception as e:
            print(f"Lỗi cào OWASP PayloadsAllTheThings: {e}")
        
        return payloads
    
    def _get_basic_techniques(self) -> List[Dict[str, Any]]:
        """Basic SQL Injection techniques từ OWASP"""
        techniques = [
            {
                "name": "UNION-based SQLi",
                "payload": "' UNION SELECT NULL-- -",
                "category": "union_based",
                "description": "Sử dụng UNION để kết hợp kết quả từ SELECT",
                "source": self.get_source_name(),
                "verified": True
            },
            {
                "name": "Error-based SQLi",
                "payload": "' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT(0x3a,0x3a,(SELECT database()),0x3a,0x3a,FLOOR(RAND()*2))x FROM information_schema.tables GROUP BY x)y)-- -",
                "category": "error_based",
                "description": "Khiến database trả về error message chứa dữ liệu",
                "source": self.get_source_name(),
                "verified": True
            },
            {
                "name": "Time-based Blind SQLi",
                "payload": "' AND SLEEP(5)-- -",
                "category": "time_based",
                "description": "Sử dụng SLEEP() để phát hiện SQLi mù",
                "source": self.get_source_name(),
                "verified": True
            },
            {
                "name": "Boolean-based Blind SQLi",
                "payload": "' AND '1'='1",
                "category": "blind_based",
                "description": "Sử dụng true/false conditions để extract dữ liệu",
                "source": self.get_source_name(),
                "verified": True
            }
        ]
        
        return techniques
    
    def _scrape_cheatsheet(self) -> List[Dict[str, Any]]:
        """Cào từ OWASP Cheat Sheet (nếu có)"""
        payloads = []
        
        try:
            content = self._make_request(self.OWASP_CHEATSHEET_URL)
            
            if not content:
                return payloads
            
            # Extract code examples
            code_blocks = re.findall(r'<code>(.*?)</code>', content, re.DOTALL)
            
            for block in code_blocks[:10]:
                block = block.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
                if 'SELECT' in block.upper():
                    payloads.append(self._parse_payload(block, "reference"))
        
        except Exception as e:
            print(f"Lỗi cào OWASP Cheat Sheet: {e}")
        
        return payloads
