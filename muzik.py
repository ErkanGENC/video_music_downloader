import os
import yt_dlp
from video import get_video_id, is_valid_youtube_url

def download_music(url, video_id, download_folder, format='mp3'):
    """Müzik indirme işlemini gerçekleştirir"""
    # Müzik klasörünü oluştur
    music_folder = os.path.join(download_folder, "muzik")
    if not os.path.exists(music_folder):
        os.makedirs(music_folder)
    
    # Dosya uzantısını belirle
    extension = format.lower()
    output_path = os.path.join(music_folder, f'audio_{video_id}.{extension}')
    
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': format,
                'preferredquality': '192' if format == 'mp3' else '256',
            }],
            'quiet': False,
            'no_warnings': False,
            'ignoreerrors': True,
            'no_color': True,
            'extract_flat': False,
            'force_generic_extractor': False,
            'socket_timeout': 30,
        }
        
        # Müziği indir
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                # Önce video bilgilerini al
                info = ydl.extract_info(url, download=False)
                if info is None:
                    raise Exception("Video bilgileri alınamadı")
                    
                # Sonra müziği indir
                ydl.download([url])
                
                # Dosya kontrollerini yap
                if not os.path.exists(output_path):
                    raise Exception("İndirilen dosya bulunamadı")
                if os.path.getsize(output_path) == 0:
                    raise Exception("İndirilen dosya boş")
                    
                return output_path
                
            except yt_dlp.utils.DownloadError as e:
                raise Exception(f"Müzik indirilemedi: {str(e)}")
            except Exception as e:
                raise Exception(f"Beklenmeyen hata: {str(e)}")
            
    except Exception as e:
        if os.path.exists(output_path):
            try:
                os.remove(output_path)
            except:
                pass
        raise Exception(f"İndirme hatası: {str(e)}") 