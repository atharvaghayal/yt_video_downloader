from flask import Flask, render_template, request, send_file
import os
import yt_dlp
import uuid
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    if 'url' in request.form:
        url = request.form['url']
        output_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.mp4")

        ydl_opts = {
            'format': 'mp4',
            'outtmpl': output_path,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        return send_file(output_path, as_attachment=True)

    elif 'myfile' in request.files:
        file = request.files['myfile']
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        output_path = os.path.join(UPLOAD_FOLDER, f"compressed_{file.filename}")

        file.save(input_path)

        subprocess.run([
            'ffmpeg', '-i', input_path,
            '-vcodec', 'libx264', '-crf', '28', output_path
        ])

        return send_file(output_path, as_attachment=True)

    return "No input received!"

if __name__ == '__main__':
    app.run(debug=True)