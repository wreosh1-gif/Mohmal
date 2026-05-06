from flask import Flask, render_template, request, send_file
import yt_dlp
import io
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download_internal')
def download_internal():
    video_url = request.args.get('url')
    if not video_url:
        return "الرابط مطلوب", 400
    try:
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            direct_link = info.get('url')
            response = requests.get(direct_link, stream=True)
            return send_file(
                io.BytesIO(response.content),
                mimetype='video/mp4',
                as_attachment=True,
                download_name='Mahmal_Video.mp4'
            )
    except Exception as e:
        return f"فشل التحميل: تأكد من الرابط. {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
