import requests
import random
from typing import Optional, Dict, Any
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Requester:
    """HTTP request handler with random User-Agent rotation and error handling."""
    
    DEFAULT_TIMEOUT = 10
    DEFAULT_USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59"
    ]

    def __init__(self, timeout: int = DEFAULT_TIMEOUT, user_agents: Optional[list] = None):
        """Initialize Requester with optional custom timeout and user agents."""
        if timeout <= 0:
            raise ValueError(f"Timeout must be positive, got {timeout}")
        self.timeout = timeout
        self.user_agents = user_agents or self.DEFAULT_USER_AGENTS

    def _get_random_headers(self) -> Dict[str, str]:
        """Generate headers with random User-Agent."""
        ua = random.choice(self.user_agents)
        return {
            "User-Agent": ua,
            "Accept": "*/*",
            "Connection": "keep-alive"
        }
    
    def request(self, url: str, method: str = "GET", data: Optional[Dict[str, Any]] = None) -> Optional[requests.Response]:
        """
        Send HTTP request with error handling.
        
        Args:
            url: Target URL
            method: HTTP method (GET or POST)
            data: Data for POST request
            
        Returns:
            Response object or None if request fails
        """
        if not url or not isinstance(url, str):
            raise ValueError("URL must be a non-empty string")
        
        if method.upper() not in ["GET", "POST"]:
            raise ValueError(f"Method {method} not supported. Use GET or POST.")
        
        headers = self._get_random_headers()
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=self.timeout, verify=False)
            else:  # POST
                response = requests.post(url, headers=headers, data=data, timeout=self.timeout, verify=False)
            
            return response
        
        except requests.exceptions.Timeout:
            print(f"[!] Timeout error: {url} took too long to respond.")
            return None
        except requests.exceptions.ConnectionError:
            print(f"[!] Connection error: Failed to connect to {url}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"[!] Request error: {str(e)}")
            return None
        except Exception as e:
            print(f"[!] Unexpected error: {str(e)}")
            return None