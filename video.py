import os
from urllib.parse import parse_qs, urlparse
import yt_dlp

def get_video_id(url):
    """YouTube URL'sinden video ID'sini çıkarır"""
    try:
        parsed_url = urlparse(url)
        if parsed_url.hostname == 'youtu.be':
            video_id = parsed_url.path[1:]
        elif parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
            if parsed_url.path == '/watch':
                video_id = parse_qs(parsed_url.query)['v'][0]
            elif parsed_url.path[:7] == '/embed/':
                video_id = parsed_url.path.split('/')[2]
            elif parsed_url.path[:3] == '/v/':
                video_id = parsed_url.path.split('/')[2]
            else:
                return None
        else:
            return None
            
        # Video ID'sinin uzunluğunu kontrol et (YouTube ID'leri 11 karakter olmalıdır)
        if video_id and len(video_id) == 11:
            return video_id
        return None
    except:
        return None

def is_valid_youtube_url(url):
    """YouTube URL'sinin geçerli olup olmadığını kontrol eder"""
    try:
        # URL formatını kontrol et
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            return False
            
        # Hostname kontrolü
        if parsed_url.hostname not in ('youtube.com', 'www.youtube.com', 'youtu.be', 'm.youtube.com'):
            return False
            
        # Video ID'sini al ve kontrol et
        video_id = get_video_id(url)
        if not video_id or len(video_id) != 11:
            return False
            
        return True
    except:
        return False

def download_video(url, quality, video_id, download_folder):
    """Video indirme işlemini gerçekleştirir"""
    # Video klasörünü oluştur
    video_folder = os.path.join(download_folder, "video")
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)
        
    output_path = os.path.join(video_folder, f'video_{video_id}.mp4')
    
    try:
        # Kaliteye göre format seçimi
        quality = int(quality)
        if quality >= 2160:
            format_spec = 'bestvideo[height<=2160]+bestaudio/best'
        elif quality >= 1440:
            format_spec = 'bestvideo[height<=1440]+bestaudio/best'
        elif quality >= 1080:
            format_spec = 'bestvideo[height<=1080]+bestaudio/best'
        elif quality >= 720:
            format_spec = 'bestvideo[height<=720]+bestaudio/best'
        elif quality >= 480:
            format_spec = 'bestvideo[height<=480]+bestaudio/best'
        else:
            format_spec = 'best[height<=360]/best'

        ydl_opts = {
            'format': format_spec,
            'outtmpl': output_path,
            'merge_output_format': 'mp4',
            'quiet': False,  # Hata ayıklama için çıktıları göster
            'no_warnings': False,  # Uyarıları göster
            'ignoreerrors': True,
            'no_color': True,
            'extract_flat': False,
            'force_generic_extractor': False,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'socket_timeout': 30,
        }
        
        # Videoyu indir
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                # Önce video bilgilerini al
                info = ydl.extract_info(url, download=False)
                if info is None:
                    raise Exception("Video bilgileri alınamadı")
                    
                # Sonra videoyu indir
                ydl.download([url])
                
                # Dosya kontrollerini yap
                if not os.path.exists(output_path):
                    raise Exception("İndirilen dosya bulunamadı")
                if os.path.getsize(output_path) == 0:
                    raise Exception("İndirilen dosya boş")
                    
                return output_path
                
            except yt_dlp.utils.DownloadError as e:
                raise Exception(f"Video indirilemedi: {str(e)}")
            except Exception as e:
                raise Exception(f"Beklenmeyen hata: {str(e)}")
            
    except Exception as e:
        if os.path.exists(output_path):
            try:
                os.remove(output_path)
            except:
                pass
        raise Exception(f"İndirme hatası: {str(e)}") 