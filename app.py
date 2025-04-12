from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from pdf2image import convert_from_bytes
import os
from io import BytesIO

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'pdf_file' not in request.files:
        return '파일이 업로드되지 않았습니다.', 400

    file = request.files['pdf_file']
    if file.filename == '':
        return '파일명이 없습니다.', 400

    filename = secure_filename(file.filename)
    pdf_bytes = file.read()

    try:
        # PDF 페이지들을 이미지로 변환 (기본은 첫 페이지만)
        images = convert_from_bytes(pdf_bytes)
        if not images:
            return '이미지 변환 실패', 500

        # 첫 번째 페이지만 JPG로 변환 (필요 시 반복 가능)
        img_io = BytesIO()
        images[0].save(img_io, 'JPEG', quality=100)
        img_io.seek(0)

        return send_file(
            img_io,
            mimetype='image/jpeg',
            as_attachment=True,
            download_name='converted.jpg'
        )
    except Exception as e:
        return f'변환 중 오류 발생: {str(e)}', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
