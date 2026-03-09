"""
GitHub Security Tools Scraper
Cào SQL Injection tools và exploits từ GitHub
"""

from typing import List, Dict, Any
from .base import BaseScraper
import json
import re


class GitHubScraper(BaseScraper):
    """Scraper cho GitHub Security Tools"""
    
    # Tìm kiếm repositories liên quan đến SQL Injection
    GITHUB_API_SEARCH = "https://api.github.com/search/repositories"
    
    SEARCH_QUERIES = [
        "sql injection",
        "sqli payload",
        "sql exploit",
        "database attack"
    ]
    
    def get_source_name(self) -> str:
        return "GitHub"
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Cào từ GitHub repositories"""
        payloads = []
        
        for query in self.SEARCH_QUERIES[:2]:  # Limit 2 searches
            payloads.extend(self._search_repositories(query))
        
        self.log_scrape(len(payloads))
        return payloads
    
    def _search_repositories(self, query: str) -> List[Dict[str, Any]]:
        """Tìm kiếm repositories trên GitHub"""
        payloads = []
        
        try:
            params = {
                "q": f"{query} language:python stars:>10",
                "sort": "stars",
                "order": "desc",
                "per_page": 5
            }
            
            response = self.session.get(
                self.GITHUB_API_SEARCH,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            
            for repo in data.get('items', [])[:5]:
                payloads.append({
                    "payload": f"GitHub: {repo['full_name']}",
                    "url": repo['html_url'],
                    "description": repo.get('description', ''),
                    "stars": repo.get('stargazers_count', 0),
                    "language": repo.get('language', 'Unknown'),
                    "category": "reference_tool",
                    "source": self.get_source_name(),
                    "verified": False
                })
        
        except Exception as e:
            print(f"Lỗi cào GitHub với query '{query}': {e}")
        
        return payloads
    
    def _extract_payloads_from_repo(self, repo_url: str) -> List[Dict[str, Any]]:
        """Extract payloads từ một repo"""
        payloads = []
        
        try:
            # Tìm raw files
            raw_url = repo_url.replace("github.com", "raw.githubusercontent.com").rstrip('/') + "/main"
            
            # Tìm Python files
            python_files = [
                f"{raw_url}/payloads.py",
                f"{raw_url}/payloads.json",
                f"{raw_url}/exploits.py"
            ]
            
            for file_url in python_files:
                content = self._make_request(file_url)
                if content:
                    payloads.extend(self._parse_python_payloads(content))
        
        except Exception as e:
            print(f"Lỗi extract từ repo {repo_url}: {e}")
        
        return payloads
    
    def _parse_python_payloads(self, content: str) -> List[Dict[str, Any]]:
        """Parse payloads từ Python code"""
        payloads = []
        
        try:
            # Tìm strings chứa payload patterns
            patterns = re.findall(r"['\"]([^'\"]*(?:UNION|SELECT|FROM|WHERE)[^'\"]*)['\"]", content, re.IGNORECASE)
            
            for pattern in patterns[:10]:
                payloads.append(self._parse_payload(pattern, "extracted"))
        
        except Exception as e:
            print(f"Lỗi parse Python payloads: {e}")
        
        return payloads
