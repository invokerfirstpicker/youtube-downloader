#!/usr/bin/env python3

import subprocess
import sys
import os
import platform

def install_requirements():
    print("📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Python dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Failed to install Python dependencies")
        return False
    return True

def install_ffmpeg():
    print("🔧 Installing ffmpeg...")
    try:
        if platform.system() == "Windows":
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
                return True
            else:
                print("⚠️  Could not install ffmpeg via winget")
                return False

        elif platform.system() == "Darwin":
            result = subprocess.run(["brew", "install", "ffmpeg"], capture_output=True, text=True, encoding='utf-8', errors='ignore')
            if result.returncode == 0:
                print("✅ ffmpeg installed successfully!")
                return True
            else:
                print("⚠️  Could not install ffmpeg via brew")
                return False

        elif platform.system() == "Linux":
            distro_commands = [
                ["apt", "update", "&&", "apt", "install", "-y", "ffmpeg"],
                ["yum", "install", "-y", "ffmpeg"],
                ["pacman", "-S", "--noconfirm", "ffmpeg"]
            ]
            for cmd in distro_commands:
                try:
                    # Для команды вроде "apt update && apt install" нужно использовать shell=True
                    result = subprocess.run(" ".join(cmd), shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
                    if result.returncode == 0:
                        print("✅ ffmpeg installed successfully!")
                        return True
                except Exception as e:
                    print(f"⚠️  Failed command: {' '.join(cmd)} | Error: {e}")
                    continue
            print("⚠️  Could not install ffmpeg automatically on Linux")
            return False

        else:
            print(f"❌ Unsupported OS: {platform.system()}")
            return False

    except Exception as e:
        print(f"❌ Error installing ffmpeg: {e}")
        return False

def main():
    print("🚀 YDownloader Setup")
    print("=" * 40)
    
    success = True
    
    if not install_requirements():
        success = False
    
    if not install_ffmpeg():
        success = False
        print("🔗 Please install ffmpeg manually:")
        print("   Windows: https://ffmpeg.org/download.html")
        print("   macOS: brew install ffmpeg")
        print("   Linux: sudo apt install ffmpeg")
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 Setup completed successfully!")
        print("🚀 Run: python main.py -u 'YOUR_URL' -q ultra")
    else:
        print("⚠️  Setup completed with warnings")
        print("📖 Check the messages above for manual installation steps")

if __name__ == "__main__":
    main()