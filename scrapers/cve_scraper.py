"""
CVE Database Scraper
Cào SQL Injection vulnerabilities từ CVE databases
"""

from typing import List, Dict, Any
from .base import BaseScraper
import json
import re
from datetime import datetime, timedelta


class CVEScraper(BaseScraper):
    """Scraper cho CVE databases (NVD, ExploitDB)"""
    
    NVD_API = "https://services.nvd.nist.gov/rest/json/cves/1.0"
    
    def get_source_name(self) -> str:
        return "CVE Database"
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Cào SQL Injection CVEs"""
        cves = []
        
        # Cào từ NVD (National Vulnerability Database)
        cves.extend(self._scrape_nvd())
        
        # Thêm known SQLi CVEs
        cves.extend(self._get_known_sqli_cves())
        
        self.log_scrape(len(cves))
        return cves
    
    def _scrape_nvd(self) -> List[Dict[str, Any]]:
        """Cào từ NVD API"""
        cves = []
        
        try:
            # NVD API có rate limiting, nên limit requests
            params = {
                "keyword": "SQL Injection",
                "resultsPerPage": 10
            }
            
            url = f"{self.NVD_API}?keyword={params['keyword']}&resultsPerPage={params['resultsPerPage']}"
            
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            
            for result in data.get('result', {}).get('CVE_Items', [])[:10]:
                cve_id = result.get('cve', {}).get('CVE_data_meta', {}).get('ID')
                description = result.get('cve', {}).get('description', {}).get('description_data', [{}])[0].get('value', '')
                
                if cve_id:
                    cves.append({
                        "cve_id": cve_id,
                        "description": description,
                        "type": "sql_injection",
                        "source": self.get_source_name(),
                        "url": f"https://nvd.nist.gov/vuln/detail/{cve_id}",
                        "discovered_at": datetime.now().isoformat()
                    })
        
        except Exception as e:
            print(f"Lỗi cào NVD: {e}")
        
        return cves
    
    def _get_known_sqli_cves(self) -> List[Dict[str, Any]]:
        """Thêm known SQL Injection CVEs"""
        cves = [
            {
                "cve_id": "CVE-2021-22911",
                "title": "Joomla SQL Injection",
                "description": "SQL Injection vulnerability in Joomla",
                "type": "sql_injection",
                "source": self.get_source_name(),
                "url": "https://nvd.nist.gov/vuln/detail/CVE-2021-22911",
                "severity": "High"
            },
            {
                "cve_id": "CVE-2021-41773",
                "title": "Apache Log4j RCE",
                "description": "While not pure SQLi, demonstrates modern exploitation",
                "type": "reference",
                "source": self.get_source_name(),
                "url": "https://nvd.nist.gov/vuln/detail/CVE-2021-41773",
                "severity": "Critical"
            }
        ]
        
        return cves
    
    def _scrape_exploitdb(self) -> List[Dict[str, Any]]:
        """Cào từ ExploitDB (nếu có API)"""
        exploits = []
        
        try:
            # ExploitDB API
            url = "https://www.exploit-db.com/api/search?q=sql+injection&type=webapps"
            
            content = self._make_request(url)
            
            if content:
                try:
                    data = json.loads(content)
                    
                    for result in data.get('results', [])[:10]:
                        exploits.append({
                            "exploit_id": result.get('edb_id'),
                            "title": result.get('title'),
                            "type": "exploit",
                            "source": self.get_source_name(),
                            "url": f"https://www.exploit-db.com/exploits/{result.get('edb_id')}"
                        })
                except json.JSONDecodeError:
                    pass
        
        except Exception as e:
            print(f"Lỗi cào ExploitDB: {e}")
        
        return exploits
