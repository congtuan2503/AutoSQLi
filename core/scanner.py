import urllib.parse
from typing import Tuple, Optional, List
from core.requester import Requester


class Scanner:
    """SQLi vulnerability scanner using error-based and boolean-based detection."""
    
    DEFAULT_ERROR_SIGNATURES = [
        "You have an error in your SQL syntax",
        "Warning: mysql_",
        "unrecognized token:",
        "Microsoft OLE DB Provider for SQL Server",
        "ORA-00933: SQL command not properly ended",
        "SQL syntax error",
        "mysql_fetch",
        "pg_exec",
        "OLE DB"
    ]
    
    DEFAULT_DIFF_THRESHOLD = 50  # Max allowed difference between original and true responses
    BOOLEAN_DIFF_THRESHOLD = 150  # Min difference between true and false responses

    def __init__(self, url: str, error_signatures: Optional[List[str]] = None):
        """Initialize scanner with target URL."""
        if not url or not isinstance(url, str):
            raise ValueError("URL must be a non-empty string")
        self.url = url
        self.requester = Requester()
        self.error_signatures = error_signatures or self.DEFAULT_ERROR_SIGNATURES

    def _is_error_based(self, html: Optional[str]) -> bool:
        """Check if HTML contains SQL error signatures."""
        if not html:
            return False
        html_lower = html.lower()
        return any(sig.lower() in html_lower for sig in self.error_signatures)

    def check_vulnerability(self) -> Tuple[bool, str]:
        """
        Check for SQLi vulnerability using multiple techniques.
        
        Returns:
            (is_vulnerable, vulnerability_type)
        """
        # Get baseline response
        original_res = self.requester.request(self.url)
        if not original_res:
            return False, "Connection Error"
        
        original_len = len(original_res.text)

        # TEST 1: Error-based SQLi
        if self._test_error_based():
            return True, "Error-based SQLi Found!"

        # TEST 2: Boolean-based SQLi
        is_vuln, msg = self._test_boolean_based(original_len)
        if is_vuln:
            return True, msg

        return False, "Not Vulnerable"

    def _test_error_based(self) -> bool:
        """Test for error-based SQL injection."""
        payload = "'"
        try:
            res_error = self.requester.request(self.url + payload)
            return res_error and self._is_error_based(res_error.text)
        except Exception:
            return False

    def _test_boolean_based(self, original_len: int) -> Tuple[bool, str]:
        """Test for boolean-based SQL injection."""
        payload_true = "%20AND%201=1"
        payload_false = "%20AND%201=2"
        
        try:
            res_true = self.requester.request(self.url + payload_true)
            res_false = self.requester.request(self.url + payload_false)

            if not res_true or not res_false:
                return False, "Failed to test boolean-based"

            len_true = len(res_true.text)
            len_false = len(res_false.text)

            diff_orig_true = abs(original_len - len_true)
            diff_true_false = abs(len_true - len_false)

            # Vulnerable if:
            # 1. True response similar to original (accounting for dynamic content)
            # 2. False response significantly different from true
            if diff_orig_true < self.DEFAULT_DIFF_THRESHOLD and diff_true_false > self.BOOLEAN_DIFF_THRESHOLD:
                return True, "Boolean-based SQLi Found!"
            
            return False, ""
        except Exception:
            return False, ""