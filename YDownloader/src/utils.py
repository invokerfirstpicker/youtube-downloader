import re
from typing import Dict
from colorama import Fore, Style


def validate_url(url: str) -> bool:
    youtube_patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=[\w-]+',
        r'(?:https?://)?(?:www\.)?youtu\.be/[\w-]+',
        r'(?:https?://)?(?:www\.)?youtube\.com/playlist\?list=[\w-]+',
        r'(?:https?://)?(?:www\.)?youtube\.com/channel/[\w-]+',
        r'(?:https?://)?(?:www\.)?youtube\.com/@[\w-]+',
    ]
    
    for pattern in youtube_patterns:
        if re.match(pattern, url):
            return True
    return False


def print_banner():
    banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════╗
║                 YDownloader                  ║
║            YouTube Video Downloader         ║
║                  Version 1.0.0              ║
╚══════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)


def print_stats(stats: Dict[str, int]):
    print(f"\n{Fore.CYAN}═══ Download Statistics ═══")
    print(f"{Fore.GREEN}✓ Successful: {stats['successful']}")
    print(f"{Fore.RED}✗ Failed: {stats['failed']}")
    print(f"{Fore.CYAN}Total: {stats['total']}")
    
    if stats['total'] > 0:
        success_rate = (stats['successful'] / stats['total']) * 100
        print(f"{Fore.YELLOW}Success rate: {success_rate:.1f}%")


def format_duration(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}m {secs}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours}h {minutes}m {secs}s"


def format_file_size(bytes_size: int) -> str:
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    size = float(bytes_size)
    unit_index = 0
    
    while size >= 1024.0 and unit_index < len(units) - 1:
        size /= 1024.0
        unit_index += 1
    
    return f"{size:.1f} {units[unit_index]}"


def create_safe_filename(filename: str) -> str:
    invalid_chars = r'<>:"/\\|?*'
    safe_filename = filename
    
    for char in invalid_chars:
        safe_filename = safe_filename.replace(char, '_')
    
    safe_filename = safe_filename.strip()[:200]
    
    return safe_filename or 'untitled'