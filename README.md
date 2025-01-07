# Video ve Müzik İndirme Uygulaması

Bu proje, YouTube'dan video ve müzik indirmenizi sağlayan bir web uygulamasıdır.

## Özellikler

- YouTube videolarını MP4 formatında indirme
- YouTube videolarını MP3 formatında indirme
- Kullanıcı dostu web arayüzü
- Hızlı indirme işlemi

## Kurulum

1. Projeyi klonlayın:
```bash
git clone https://github.com/kullaniciadi/video_music_downloader.git
cd video_music_downloader
```

2. Gerekli Python paketlerini yükleyin:
```bash
pip install -r requirements.txt
```

## Kullanım

1. Uygulamayı başlatın:
```bash
python app.py
```

2. Web tarayıcınızda `http://localhost:5000` adresine gidin
3. YouTube video URL'sini girin
4. İndirmek istediğiniz formatı seçin (MP3 veya MP4)
5. İndirme butonuna tıklayın

## Klasör Yapısı

- `/static` - CSS, JavaScript ve diğer statik dosyalar
- `/templates` - HTML şablonları
- `/downloads` - İndirilen dosyaların geçici depolama alanı
- `/indirilenler` - İndirilen dosyaların kalıcı depolama alanı

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakın.
