"""
Payload Manager - Centralized payload and technique storage
Manages loading, updating, and access to SQL injection techniques
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


class PayloadManager:
    """Quản lý lưu trữ, cập nhật và truy cập payload"""
    
    def __init__(self):
        self.payload_file = Path(__file__).parent.parent / "data" / "payloads.json"
        self.backup_file = Path(__file__).parent.parent / "data" / "payloads.backup.json"
        self.payloads = self._load_payloads()
    
    def _load_payloads(self) -> Dict[str, Any]:
        """Load payloads từ JSON file"""
        if self.payload_file.exists():
            try:
                with open(self.payload_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Lỗi khi đọc payloads: {e}")
                return self._get_default_payloads()
        return self._get_default_payloads()
    
    def _get_default_payloads(self) -> Dict[str, Any]:
        """Payload mặc định ban đầu"""
        return {
            "metadata": {
                "version": "1.0",
                "updated": datetime.now().isoformat(),
                "sources": [],
                "total_payloads": 0
            },
            "union_based": {
                "numeric": [],
                "string": [],
                "double_quote": []
            },
            "error_based": [],
            "time_based": [],
            "blind_based": [],
            "waf_bypass": {
                "encoding": [],
                "comments": [],
                "case_variation": [],
                "whitespace": []
            },
            "version_fingerprint": [],
            "database_detection": []
        }
    
    def save_payloads(self):
        """Lưu payloads vào JSON file"""
        self.payload_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Backup cũ
        if self.payload_file.exists():
            import shutil
            shutil.copy2(self.payload_file, self.backup_file)
        
        # Cập nhật metadata
        self.payloads["metadata"]["updated"] = datetime.now().isoformat()
        self.payloads["metadata"]["total_payloads"] = self._count_payloads()
        
        with open(self.payload_file, 'w', encoding='utf-8') as f:
            json.dump(self.payloads, f, indent=2, ensure_ascii=False)
    
    def _count_payloads(self) -> int:
        """Đếm tổng số payloads"""
        count = 0
        for key, value in self.payloads.items():
            if key != "metadata":
                if isinstance(value, list):
                    count += len(value)
                elif isinstance(value, dict):
                    for subval in value.values():
                        if isinstance(subval, list):
                            count += len(subval)
        return count
    
    def add_payload(self, category: str, payload: Dict[str, Any], subcategory: Optional[str] = None):
        """Thêm một payload mới - Smart handling của nested categories"""
        import json
        
        # Nếu không specify subcategory, extract từ payload hoặc use default
        if not subcategory:
            subcategory = payload.get('subcategory', payload.get('type', 'general'))
        
        # Ensure category structure exists
        if category not in self.payloads:
            self.payloads[category] = []
        
        # Nếu current category là dict (có subcategories), add dưới subcategory
        if isinstance(self.payloads[category], dict):
            if subcategory not in self.payloads[category]:
                self.payloads[category][subcategory] = []
            
            # Check for duplicates
            payload_str = json.dumps(payload, sort_keys=True, default=str)
            existing_payloads = [json.dumps(p, sort_keys=True, default=str) for p in self.payloads[category][subcategory]]
            
            if payload_str not in existing_payloads:
                self.payloads[category][subcategory].append(payload)
                self.save_payloads()
        
        # Nếu category là list, add trực tiếp
        elif isinstance(self.payloads[category], list):
            # Check for duplicates
            payload_str = json.dumps(payload, sort_keys=True, default=str)
            existing_payloads = [json.dumps(p, sort_keys=True, default=str) for p in self.payloads[category]]
            
            if payload_str not in existing_payloads:
                self.payloads[category].append(payload)
                self.save_payloads()
    
    def add_payloads_batch(self, category: str, payloads: List[Dict], subcategory: Optional[str] = None):
        """Thêm nhiều payloads cùng lúc"""
        for payload in payloads:
            self.add_payload(category, payload, subcategory)
    
    def get_payloads(self, category: str, subcategory: Optional[str] = None) -> List[Dict]:
        """Lấy payloads theo category"""
        if category not in self.payloads:
            return []
        
        if subcategory:
            if isinstance(self.payloads[category], dict):
                return self.payloads[category].get(subcategory, [])
        else:
            if isinstance(self.payloads[category], list):
                return self.payloads[category]
        
        return []
    
    def get_all_waf_bypass(self) -> Dict[str, List]:
        """Lấy tất cả WAF bypass techniques"""
        return self.payloads.get("waf_bypass", {})
    
    def get_metadata(self) -> Dict:
        """Lấy metadata"""
        return self.payloads.get("metadata", {})
    
    def add_source(self, source_name: str):
        """Ghi lại nguồn dữ liệu"""
        if "metadata" not in self.payloads:
            self.payloads["metadata"] = {}
        
        sources = self.payloads["metadata"].get("sources", [])
        if source_name not in sources:
            sources.append(source_name)
        
        self.payloads["metadata"]["sources"] = sources
        self.save_payloads()
    
    def reset_to_default(self):
        """Reset về default payloads"""
        self.payloads = self._get_default_payloads()
        self.save_payloads()


# Global instance
payload_manager = PayloadManager()
