"""
PortSwigger Web Security Academy Scraper
Cào SQL Injection lessons và labs từ PortSwigger
"""

from typing import List, Dict, Any
from .base import TechniqueScraper
import re


class PortSwiggerScraper(TechniqueScraper):
    """Scraper cho PortSwigger Web Security Academy"""
    
    PORTSWIGGER_BASE = "https://portswigger.net/web-security"
    
    SQL_INJECTION_TOPICS = [
        ("sql-injection", "SQL Injection basics"),
        ("blind-sql-injection", "Blind SQL Injection"),
        ("time-delay-based-blind-sql-injection", "Time-delay Blind SQLi"),
    ]
    
    def get_source_name(self) -> str:
        return "PortSwigger"
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Cào từ PortSwigger Web Security Academy"""
        techniques = []
        
        # Thêm known techniques từ PortSwigger
        techniques.extend(self._get_portswigger_techniques())
        
        self.log_scrape(len(techniques))
        return techniques
    
    def _get_portswigger_techniques(self) -> List[Dict[str, Any]]:
        """Lấy techniques được biết từ PortSwigger"""
        techniques = [
            {
                "name": "UNION-based SQL Injection",
                "description": "Sử dụng UNION keyword để kết hợp results từ multiple SELECT statements",
                "type": "union_based",
                "steps": [
                    "1. Tìm số lượng columns dalam original query",
                    "2. Tìm columns có kiểu string",
                    "3. Sử dụng UNION SELECT để extract dữ liệu"
                ],
                "example": "' UNION SELECT NULL,NULL,NULL--",
                "source": self.get_source_name(),
                "url": f"{self.PORTSWIGGER_BASE}/sql-injection"
            },
            {
                "name": "Error-based SQL Injection",
                "description": "Lợi dụng error messages từ database để extract dữ liệu",
                "type": "error_based",
                "steps": [
                    "1. Trigger error bằng cách sửa syntax",
                    "2. Quan sát error message",
                    "3. Inject code vào error message để extract dữ liệu"
                ],
                "example": "' AND extractvalue(rand(),concat(0x3a,(select database())))--",
                "source": self.get_source_name(),
                "url": f"{self.PORTSWIGGER_BASE}/sql-injection"
            },
            {
                "name": "Time-based Blind SQL Injection",
                "description": "Sử dụng time delay để phát hiện và extract dữ liệu",
                "type": "time_based",
                "steps": [
                    "1. Inject time delay function",
                    "2. Đo lường response time",
                    "3. Extract dữ liệu bằng conditional delays"
                ],
                "example": "' AND (SELECT SLEEP(5))",
                "source": self.get_source_name(),
                "url": f"{self.PORTSWIGGER_BASE}/blind-sql-injection"
            },
            {
                "name": "Boolean-based Blind SQL Injection",
                "description": "Sử dụng boolean conditions để extract dữ liệu từ mù SQLi",
                "type": "boolean_blind",
                "steps": [
                    "1. Inject boolean conditions",
                    "2. Quan sát responses (true or false)",
                    "3. Extract character-by-character"
                ],
                "example": "' AND '1'='1",
                "source": self.get_source_name(),
                "url": f"{self.PORTSWIGGER_BASE}/blind-sql-injection"
            }
        ]
        
        return techniques
    
    def _scrape_lab_solutions(self) -> List[Dict[str, Any]]:
        """Cào lab solutions từ PortSwigger (nếu public)"""
        techniques = []
        
        try:
            # PortSwigger thường có public learning materials
            for topic, description in self.SQL_INJECTION_TOPICS:
                url = f"{self.PORTSWIGGER_BASE}/{topic}"
                
                content = self._make_request(url)
                
                if content:
                    # Extract examples từ content
                    examples = re.findall(r"<code[^>]*>(.*?)</code>", content, re.DOTALL)
                    
                    for example in examples[:5]:
                        example = example.replace('<br>', '\n').replace('&lt;', '<').replace('&gt;', '>')
                        if any(keyword in example.upper() for keyword in ['SELECT', 'UNION', 'SLEEP']):
                            techniques.append(self.parse_technique(
                                f"PortSwigger: {topic.replace('-', ' ')}",
                                example,
                                "example"
                            ))
        
        except Exception as e:
            print(f"Lỗi cào PortSwigger labs: {e}")
        
        return techniques
