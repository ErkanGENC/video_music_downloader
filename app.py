from flask import Flask, render_template, request, send_file, Response
import os
from video import download_video, is_valid_youtube_url, get_video_id
from muzik import download_music

app = Flask(__name__)

DOWNLOAD_FOLDER = "indirilenler"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def handle_download():
    try:
        url = request.form['url']
        quality = request.form['quality']
        
        if not is_valid_youtube_url(url):
            return render_template('index.html', message="Lütfen geçerli bir YouTube URL'si girin.")
        
        video_id = get_video_id(url)
        if not video_id:
            return render_template('index.html', message="Video ID'si alinamadi.")

        # Video dosyasını indir
        output_path = download_video(url, quality, video_id, DOWNLOAD_FOLDER)
        
        if not os.path.exists(output_path):
            return render_template('index.html', message="İndirme işlemi başarisiz oldu.")

        # Dosyayı gönder
        filename = f"video_{video_id}.mp4"
        response = send_file(
            output_path,
            as_attachment=True,
            download_name=filename,
            mimetype='video/mp4'
        )
        
        # İndirme tamamlandıktan sonra dosyayı sil
        @response.call_on_close
        def cleanup():
            if os.path.exists(output_path):
                try:
                    os.remove(output_path)
                except:
                    pass
                    
        return response

    except Exception as e:
        error_message = str(e)
        if "format" in error_message.lower():
            error_message = "Bu video için seçilen çözünürlük mevcut değil. Daha düşük bir çözünürlük seçin."
        elif "unavailable" in error_message.lower():
            error_message = "Bu video mevcut değil veya erişilemez durumda."
        elif "private" in error_message.lower():
            error_message = "Bu video özel veya gizli."
        elif "copyright" in error_message.lower():
            error_message = "Bu video telif hakki nedeniyle indirilemez."
        elif "age" in error_message.lower():
            error_message = "Bu video yaş sinirlamali içerik nedeniyle indirilemez."
        return render_template('index.html', message=f"Hata oluştu: {error_message}")

@app.route('/download_music', methods=['POST'])
def handle_music_download():
    try:
        url = request.form['url']
        format = request.form.get('format', 'mp3')  # Varsayılan olarak mp3
        
        if not is_valid_youtube_url(url):
            return render_template('index.html', message="Lütfen geçerli bir YouTube URL'si girin.")
        
        video_id = get_video_id(url)
        if not video_id:
            return render_template('index.html', message="Video ID'si alınamadı.")

        # Müzik dosyasını indir
        output_path = download_music(url, video_id, DOWNLOAD_FOLDER, format)
        
        if not os.path.exists(output_path):
            return render_template('index.html', message="İndirme işlemi başarısız oldu.")

        # Dosyayı gönder
        filename = f"audio_{video_id}.{format}"
        response = send_file(
            output_path,
            as_attachment=True,
            download_name=filename,
            mimetype=f'audio/{format}'
        )
        
        # İndirme tamamlandıktan sonra dosyayı sil
        @response.call_on_close
        def cleanup():
            if os.path.exists(output_path):
                try:
                    os.remove(output_path)
                except:
                    pass
                    
        return response

    except Exception as e:
        error_message = str(e)
        if "unavailable" in error_message.lower():
            error_message = "Bu video mevcut değil veya erişilemez durumda."
        elif "private" in error_message.lower():
            error_message = "Bu video özel veya gizli."
        elif "copyright" in error_message.lower():
            error_message = "Bu video telif hakkı nedeniyle indirilemez."
        elif "age" in error_message.lower():
            error_message = "Bu video yaş sınırlamalı içerik nedeniyle indirilemez."
        return render_template('index.html', message=f"Hata oluştu: {error_message}")

if __name__ == '__main__':
    app.run(debug=True) 