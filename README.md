# YDownloader
An open source script written in Python for downloading videos from Youtube
# YDownloader

Simple YouTube video downloader

## What it does

Downloads videos from YouTube. Can download one video or a whole list. Choose quality from best to worst or specific resolution.

## How to use

Clone this repo:
```bash
git clone https://github.com/yourusername/YDownloader.git
cd YDownloader
pip install -r requirements.txt
```

Download single video:
```bash
python main.py -u "https://youtube.com/watch?v=VIDEO_ID"
```

Download from list:
```bash
python main.py -l video_list.txt
```

Choose quality:
```bash
python main.py -u "URL" -q 720p
```

Custom folder:
```bash
python main.py -u "URL" -o ./videos/
```

Just get info:
```bash
python main.py -u "URL" --info
```

## Options

- `-u` - single video URL
- `-l` - text file with URLs (one per line)
- `-q` - quality: best, worst, 1080p, 720p, 480p, 360p, audio
- `-o` - output folder
- `--info` - show video info without downloading

## Quality

- `best` - highest quality (default)
- `worst` - lowest quality
- `1080p`, `720p`, `480p`, `360p` - specific resolution
- `audio` - audio only (mp3)

## Files

- `main.py` - run this
- `src/` - code
- `requirements.txt` - what to install
- `example_urls.txt` - example list

## Dependencies

- yt-dlp
- colorama
- tqdm

Educational use only. Respect YouTube ToS.

---

# На русском

Простой загрузчик видео с YouTube

## Что делает

Качает видео с ютуба. Можно одно видео или список. Выбираешь качество от лучшего до худшего или конкретное разрешение.

## Как использовать

Склонируй:
```bash
git clone https://github.com/yourusername/YDownloader.git
cd YDownloader
pip install -r requirements.txt
```

Скачать одно видео:
```bash
python main.py -u "https://youtube.com/watch?v=VIDEO_ID"
```

Скачать из списка:
```bash
python main.py -l video_list.txt
```

Выбрать качество:
```bash
python main.py -u "URL" -q 720p
```

Своя папка:
```bash
python main.py -u "URL" -o ./видео/
```

Только инфо:
```bash
python main.py -u "URL" --info
```

## Опции

- `-u` - URL одного видео
- `-l` - текстовик со ссылками (по одной на строку)
- `-q` - качество: best, worst, 1080p, 720p, 480p, 360p, audio
- `-o` - папка для сохранения
- `--info` - показать инфо без скачивания

## Качество

- `best` - лучшее качество (по умолчанию)
- `worst` - худшее качество
- `1080p`, `720p`, `480p`, `360p` - конкретное разрешение
- `audio` - только звук (mp3)

## Файлы

- `main.py` - запускаешь это
- `src/` - код
- `requirements.txt` - что устанавливать
- `example_urls.txt` - пример списка

## Зависимости

- yt-dlp
- colorama
- tqdm

Только для образовтельных целей. Соблюдайте правила YouTube.
