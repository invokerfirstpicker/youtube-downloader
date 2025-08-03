import os
import yt_dlp
from pathlib import Path
from typing import Dict, List, Optional
import shutil
import subprocess
import sys
import platform


class YouTubeDownloader:
    
    def __init__(self, output_dir: str = "downloads", quality: str = "best", force_convert: bool = False):
        os.environ['PYTHONIOENCODING'] = 'utf-8'
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.quality = quality
        self.force_convert = force_convert
        self._check_ffmpeg()
    
    def _check_ffmpeg(self):
        if not shutil.which('ffmpeg'):
            print("🔧 ffmpeg not found. Installing automatically...")
            self._install_ffmpeg()
    
    def _install_ffmpeg(self):
        try:
            if platform.system() == "Windows":
                print("📦 Installing ffmpeg via winget...")
                result = subprocess.run(
                    ["winget", "install", "ffmpeg", "--accept-source-agreements", "--accept-package-agreements"],
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='ignore',
                    timeout=300
                )
                if result.returncode == 0:
                    print("✅ ffmpeg installed successfully!")
                    self._add_ffmpeg_to_path()
                else:
                    print("⚠️  Could not install ffmpeg automatically. Please install manually.")
                    print("   Download from: https://ffmpeg.org/download.html")
            else:
                print("⚠️  Auto-install only supported on Windows. Please install ffmpeg manually.")
        except Exception as e:
            print(f"⚠️  Error installing ffmpeg: {e}")
            print("   Please install manually from: https://ffmpeg.org/download.html")
    
    def _add_ffmpeg_to_path(self):
        if platform.system() == "Windows":
            possible_paths = [
                os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-7.1.1-full_build\bin"),
                os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-7.0.2-full_build\bin"),
                os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-*-full_build\bin")
            ]
            
            for path in possible_paths:
                if os.path.exists(path.replace("*", "7.1.1")):
                    os.environ["PATH"] = os.environ["PATH"] + ";" + path.replace("*", "7.1.1")
                    self.ffmpeg_path = os.path.join(path.replace("*", "7.1.1"), "ffmpeg.exe")
                    return
                elif os.path.exists(path.replace("*", "7.0.2")):
                    os.environ["PATH"] = os.environ["PATH"] + ";" + path.replace("*", "7.0.2")
                    self.ffmpeg_path = os.path.join(path.replace("*", "7.0.2"), "ffmpeg.exe")
                    return
            
            winget_packages = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages")
            if os.path.exists(winget_packages):
                for item in os.listdir(winget_packages):
                    if "FFmpeg" in item:
                        ffmpeg_dir = os.path.join(winget_packages, item)
                        for subdir in os.listdir(ffmpeg_dir):
                            if "ffmpeg-" in subdir and "full_build" in subdir:
                                bin_path = os.path.join(ffmpeg_dir, subdir, "bin")
                                if os.path.exists(bin_path):
                                    os.environ["PATH"] = os.environ["PATH"] + ";" + bin_path
                                    self.ffmpeg_path = os.path.join(bin_path, "ffmpeg.exe")
                                    return
        
    def get_ydl_opts(self) -> Dict:
        quality_formats = {
            'best': 'bestvideo[vcodec!*=av01][ext=mp4]+bestaudio[acodec!*=opus]/bestvideo[vcodec!*=av01]+bestaudio[acodec!*=opus]/best[ext=mp4]/best',
            'ultra': 'bestvideo[height>=2160][vcodec!*=av01]+bestaudio[acodec!*=opus]/bestvideo[height>=1440][vcodec!*=av01]+bestaudio[acodec!*=opus]/bestvideo+bestaudio/best',
            '4k': 'bestvideo[height>=2160][vcodec!*=av01][ext=mp4]+bestaudio[acodec!*=opus]/bestvideo[height>=2160][vcodec!*=av01]+bestaudio[acodec!*=opus]/best[height>=2160]',
            '1440p': 'bestvideo[height>=1440][height<=2160][vcodec!*=av01][ext=mp4]+bestaudio[acodec!*=opus]/bestvideo[height>=1440][height<=2160][vcodec!*=av01]+bestaudio[acodec!*=opus]/best[height>=1440][height<=2160]',
            '1080p': 'bestvideo[height>=1080][height<=1440][vcodec!*=av01][ext=mp4]+bestaudio[acodec!*=opus]/bestvideo[height>=1080][height<=1440][vcodec!*=av01]+bestaudio[acodec!*=opus]/best[height>=1080][height<=1440]',
            '720p': 'bestvideo[height>=720][height<=1080][vcodec!*=av01][ext=mp4]+bestaudio[acodec!*=opus]/bestvideo[height>=720][height<=1080][vcodec!*=av01]+bestaudio[acodec!*=opus]/best[height>=720][height<=1080]',
            '480p': 'bestvideo[height>=480][height<=720][vcodec!*=av01][ext=mp4]+bestaudio[acodec!*=opus]/bestvideo[height>=480][height<=720][vcodec!*=av01]+bestaudio[acodec!*=opus]/best[height>=480][height<=720]',
            '360p': 'bestvideo[height>=360][height<=480][vcodec!*=av01][ext=mp4]+bestaudio[acodec!*=opus]/bestvideo[height>=360][height<=480][vcodec!*=av01]+bestaudio[acodec!*=opus]/best[height>=360][height<=480]',
            'worst': 'worst[ext=mp4]/worst',
            'audio': 'bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio'
        }
        
        format_selector = quality_formats.get(self.quality, self.quality)
        
        opts = {
            'format': format_selector,
            'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
            'restrictfilenames': True,
            'noplaylist': False,
            'ignoreerrors': True,
            'writesubtitles': False,
            'writeautomaticsub': False,
            'subtitleslangs': ['en', 'ru'],
            'merge_output_format': 'mp4',
            'prefer_ffmpeg': True,
            'keepvideo': False,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
        }
        
        if self.quality == 'audio':
            opts.update({
                'extractaudio': True,
                'audioformat': 'mp3',
                'audioquality': '0',
                'audio_quality': 0,
                'format': 'bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio'
            })
        else:
            opts.update({
                'extractaudio': False,
                'writeinfojson': False,
                'writethumbnail': False,
                'embedsubs': False,
                'embedthumbnail': False,
                'addmetadata': True,
            })
        
        return opts
    
    def _merge_video_audio(self, video_file: str, audio_file: str, output_file: str) -> bool:
        ffmpeg_cmd = shutil.which('ffmpeg')
        if not ffmpeg_cmd and hasattr(self, 'ffmpeg_path'):
            ffmpeg_cmd = self.ffmpeg_path
        
        if not ffmpeg_cmd:
            print("❌ ffmpeg not available for merging")
            return False
        
        try:
            cmd = [
                ffmpeg_cmd,
                '-i', video_file,
                '-i', audio_file,
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-ac', '2',
                '-ar', '48000',
                '-ab', '192k',
                '-preset', 'fast',
                '-crf', '23',
                '-movflags', '+faststart',
                '-f', 'mp4',
                '-y',
                output_file
            ]
            
            print(f"🔧 Converting and merging to compatible MP4...")
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            
            if result.returncode == 0:
                print(f"✅ Successfully converted to: {output_file}")
                os.remove(video_file)
                os.remove(audio_file)
                print(f"🗑️  Cleaned up temporary files")
                return True
            else:
                print(f"❌ Error converting files: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error during conversion: {e}")
            return False
    
    def _convert_to_compatible_mp4(self, input_file: str, output_file: str) -> bool:
        ffmpeg_cmd = shutil.which('ffmpeg')
        if not ffmpeg_cmd and hasattr(self, 'ffmpeg_path'):
            ffmpeg_cmd = self.ffmpeg_path
        
        if not ffmpeg_cmd:
            print("❌ ffmpeg not available for conversion")
            return False
        
        try:
            cmd = [
                ffmpeg_cmd,
                '-i', input_file,
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-ac', '2',
                '-ar', '48000',
                '-ab', '192k',
                '-profile:v', 'main',
                '-level', '3.1',
                '-preset', 'fast',
                '-crf', '23',
                '-pix_fmt', 'yuv420p',
                '-movflags', '+faststart',
                '-f', 'mp4',
                '-strict', 'experimental',
                '-avoid_negative_ts', 'make_zero',
                '-y',
                output_file
            ]

            print(f"🔄 Converting to Windows Media Player compatible format...")
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=1800)
            
            if result.returncode == 0:
                print(f"✅ Successfully converted to: {output_file}")
                if input_file != output_file and os.path.exists(output_file):
                    os.remove(input_file)
                    print(f"🗑️  Replaced original file")
                return True
            else:
                print(f"❌ Error converting file: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"❌ Conversion timeout - file too large")
            return False
        except Exception as e:
            print(f"❌ Error during conversion: {e}")
            return False
    
    def _check_codec_compatibility(self, file_path: str) -> bool:
        ffprobe_cmd = shutil.which('ffprobe')
        if not ffprobe_cmd and hasattr(self, 'ffmpeg_path'):
            ffprobe_path = self.ffmpeg_path.replace('ffmpeg.exe', 'ffprobe.exe')
            if os.path.exists(ffprobe_path):
                ffprobe_cmd = ffprobe_path
        
        if not ffprobe_cmd:
            return False
        
        try:
            cmd = [
                ffprobe_cmd,
                '-v', 'quiet',
                '-show_entries', 'stream=codec_name',
                '-of', 'csv=p=0',
                file_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            if result.returncode == 0:
                codecs = result.stdout.strip().split('\n')
                problematic_codecs = ['av01', 'vp9', 'opus', 'vorbis']
                for codec in codecs:
                    if any(prob in codec.lower() for prob in problematic_codecs):
                        print(f"⚠️  Detected problematic codec: {codec}")
                        return False
                return True
            
        except Exception:
            pass
        
        return False
    
    def list_formats(self, url: str) -> bool:
        try:
            ydl_opts = {
                'listformats': True,
                'quiet': False,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info(url, download=False)
                return True
        except Exception as e:
            print(f"✗ Error getting formats for {url}: {str(e)}")
            return False
    
    def download_video(self, url: str) -> bool:
        try:
            opts = self.get_ydl_opts()
            
            if self.quality in ['best', 'ultra']:
                print(f"🔍 Searching for highest quality format...")
                try:
                    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                        info = ydl.extract_info(url, download=False)
                        formats = info.get('formats', [])
                        if formats:
                            best_height = max(f.get('height', 0) for f in formats if f.get('height'))
                            print(f"📺 Best available quality: {best_height}p")
                except:
                    pass
            
            with yt_dlp.YoutubeDL(opts) as ydl:
                print(f"⬇️ Downloading: {url}")
                print(f"🎯 Quality setting: {self.quality}")
                
                info = ydl.extract_info(url, download=False)
                video_title = info.get('title', 'video').replace('/', '_').replace('\\', '_')
                
                ydl.download([url])
                
                video_files = list(self.output_dir.glob(f"{video_title}.f*.mp4"))
                audio_files = list(self.output_dir.glob(f"{video_title}.f*.webm")) + list(self.output_dir.glob(f"{video_title}.f*.m4a"))
                
                if len(video_files) == 1 and len(audio_files) == 1:
                    video_file = str(video_files[0])
                    audio_file = str(audio_files[0])
                    final_output = str(self.output_dir / f"{video_title}_4K.mp4")
                    
                    if self._merge_video_audio(video_file, audio_file, final_output):
                        print(f"🎉 Video downloaded and merged in maximum quality!")
                        return True
                else:
                    existing_files = list(self.output_dir.glob(f"{video_title}.*"))
                    if existing_files:
                        converted = False
                        for file_path in existing_files:
                            if file_path.suffix.lower() in ['.mp4', '.mkv', '.webm', '.avi', '.mov']:
                                print(f"🔍 Checking codec compatibility...")
                                if not self._check_codec_compatibility(str(file_path)) or self.force_convert:
                                    compatible_output = str(self.output_dir / f"{video_title}_WMP_compatible.mp4")
                                    print(f"🔄 Converting AV1/Opus to H.264/AAC for Windows compatibility...")
                                    if self._convert_to_compatible_mp4(str(file_path), compatible_output):
                                        print(f"🎉 Video converted to Windows-compatible format with audio!")
                                        converted = True
                                        break
                                    else:
                                        print(f"⚠️  Conversion failed, keeping original file")
                                else:
                                    print(f"✅ Codecs are already compatible!")
                        
                        if not converted:
                            print(f"✅ Video downloaded successfully!")
                        else:
                            return True
                    
                print(f"✅ Successfully downloaded video from: {url}")
                return True
        except Exception as e:
            print(f"❌ Error downloading {url}: {str(e)}")
            return False
    
    def download_from_list(self, file_path: str) -> Dict[str, int]:
        stats = {'successful': 0, 'failed': 0, 'total': 0}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            stats['total'] = len(urls)
            print(f"Found {stats['total']} URLs in {file_path}")
            
            for i, url in enumerate(urls, 1):
                print(f"\n[{i}/{stats['total']}] Processing: {url}")
                
                if self.download_video(url):
                    stats['successful'] += 1
                else:
                    stats['failed'] += 1
                    
        except FileNotFoundError:
            print(f"✗ Error: File '{file_path}' not found")
        except Exception as e:
            print(f"✗ Error reading file: {str(e)}")
        
        return stats
    
    def get_video_info(self, url: str) -> Optional[Dict]:
        try:
            ydl_opts = {'quiet': True, 'no_warnings': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'view_count': info.get('view_count', 0)
                }
        except Exception:
            return None