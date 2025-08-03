import argparse
import sys
from pathlib import Path
from colorama import init, Fore, Style

from .downloader import YouTubeDownloader
from .utils import validate_url, print_banner, print_stats

init(autoreset=True)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='YDownloader - YouTube Video Downloader',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s -u "https://youtube.com/watch?v=dQw4w9WgXcQ" -q ultra
  %(prog)s -u "https://youtube.com/watch?v=dQw4w9WgXcQ" -q 4k  
  %(prog)s -l video_list.txt -q best
  %(prog)s -u "https://youtube.com/watch?v=dQw4w9WgXcQ" --list-formats
  %(prog)s -u "https://youtube.com/watch?v=dQw4w9WgXcQ" -q 1080p -o ./my_videos/
  %(prog)s --convert video.mp4
  
Quality options:
  ultra - Maximum available quality (4K/1440p/1080p with best audio)
  4k    - 4K (2160p) quality
  1440p - 1440p quality  
  best  - Best quality with video+audio merge
  1080p - 1080p quality
  720p  - 720p quality
        '''
    )
    
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        '-u', '--url',
        type=str,
        help='Single YouTube video URL to download'
    )
    group.add_argument(
        '-l', '--list',
        type=str,
        help='Path to text file containing YouTube URLs (one per line)'
    )
    
    parser.add_argument(
        '-q', '--quality',
        type=str,
        default='best',
        choices=['best', 'ultra', '4k', '1440p', '1080p', '720p', '480p', '360p', 'worst', 'audio'],
        help='Video quality to download (default: best)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='downloads',
        help='Output directory for downloaded videos (default: downloads)'
    )
    
    parser.add_argument(
        '--info',
        action='store_true',
        help='Show video information without downloading'
    )
    
    parser.add_argument(
        '--list-formats',
        action='store_true',
        help='List all available video formats without downloading'
    )
    
    parser.add_argument(
        '--convert',
        type=str,
        help='Convert existing video file to Windows Media Player compatible MP4 format'
    )
    
    parser.add_argument(
        '--force-convert',
        action='store_true',
        help='Force convert all downloaded videos to compatible format'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='YDownloader 1.0.0'
    )
    
    return parser


def handle_single_url(downloader: YouTubeDownloader, url: str, info_only: bool = False, list_formats: bool = False) -> bool:
    if not validate_url(url):
        print(f"{Fore.RED}✗ Invalid YouTube URL: {url}")
        return False
    
    if list_formats:
        print(f"{Fore.CYAN}Listing available formats...")
        return downloader.list_formats(url)
    
    if info_only:
        print(f"{Fore.CYAN}Getting video information...")
        info = downloader.get_video_info(url)
        if info:
            print(f"{Fore.GREEN}Title: {info['title']}")
            print(f"{Fore.GREEN}Uploader: {info['uploader']}")
            print(f"{Fore.GREEN}Duration: {info['duration']} seconds")
            print(f"{Fore.GREEN}Views: {info['view_count']:,}")
            return True
        else:
            print(f"{Fore.RED}✗ Could not get video information")
            return False
    else:
        return downloader.download_video(url)


def handle_url_list(downloader: YouTubeDownloader, file_path: str, info_only: bool = False) -> bool:
    if not Path(file_path).exists():
        print(f"{Fore.RED}✗ File not found: {file_path}")
        return False
    
    if info_only:
        print(f"{Fore.RED}✗ Info mode not supported for URL lists")
        return False
    
    stats = downloader.download_from_list(file_path)
    print_stats(stats)
    
    return stats['successful'] > 0


def main():
    print_banner()
    
    parser = create_parser()
    args = parser.parse_args()
    
    if hasattr(args, 'convert') and args.convert:
        if not Path(args.convert).exists():
            print(f"{Fore.RED}✗ File not found: {args.convert}")
            sys.exit(1)
        
        downloader = YouTubeDownloader(output_dir="./", quality="best")
        input_file = args.convert
        output_file = str(Path(input_file).with_stem(Path(input_file).stem + "_compatible"))
        
        if downloader._convert_to_compatible_mp4(input_file, output_file):
            print(f"{Fore.GREEN}✓ Conversion completed successfully!")
            sys.exit(0)
        else:
            print(f"{Fore.RED}✗ Conversion failed")
            sys.exit(1)
    
    if not args.url and not args.list:
        print(f"{Fore.RED}✗ Either --url or --list is required")
        parser.print_help()
        sys.exit(1)
    
    if args.list and not Path(args.list).exists():
        print(f"{Fore.RED}✗ List file not found: {args.list}")
        sys.exit(1)
    
    output_path = Path(args.output)
    try:
        output_path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"{Fore.RED}✗ Could not create output directory: {e}")
        sys.exit(1)
    
    print(f"{Fore.CYAN}Initializing downloader...")
    print(f"{Fore.CYAN}Quality: {args.quality}")
    print(f"{Fore.CYAN}Output directory: {output_path.absolute()}")
    print()
    
    downloader = YouTubeDownloader(
        output_dir=str(output_path),
        quality=args.quality,
        force_convert=getattr(args, 'force_convert', False)
    )
    
    success = False
    
    try:
        if args.url:
            success = handle_single_url(downloader, args.url, args.info, getattr(args, 'list_formats', False))
        elif args.list:
            if getattr(args, 'list_formats', False):
                print(f"{Fore.RED}✗ Format listing not supported for URL lists")
                sys.exit(1)
            success = handle_url_list(downloader, args.list, args.info)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠ Download interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"{Fore.RED}✗ Unexpected error: {e}")
        sys.exit(1)
    
    if success:
        print(f"\n{Fore.GREEN}✓ Operation completed successfully!")
        sys.exit(0)
    else:
        print(f"\n{Fore.RED}✗ Operation failed")
        sys.exit(1)