from pathlib import Path
import yt_dlp


def download_youtube_audio(video_url, output_dir):

    output_template = str(Path(output_dir) / 'audio.%(ext)s')
    options = {
        'format': 'bestaudio/best',
        'outtmpl': output_template,
        'quiet': True,
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(options) as yt_downloader:
        yt_downloader.download([video_url])
    return str(Path(output_dir) / 'audio.mp3')


def extract_video_info(video_url):

    options = {
        'quiet': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(options) as yt_downloader:
        info = yt_downloader.extract_info(video_url, download=False)
        return {
            'title': info.get('title'),
            'duration': info.get('duration'),
            'description': info.get('description')
        }