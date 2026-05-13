import os
import uuid
from flask import Flask, request, jsonify, render_template
from rembg import remove
from PIL import Image
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 МБ макс. размер

UPLOAD_DIR = os.path.join('static', 'uploads')
PROCESSED_DIR = os.path.join('static', 'processed')
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'error': 'Файл не отправлен'}), 400

    file = request.files['image']
    if not file or file.filename == '':
        return jsonify({'error': 'Файл пустой'}), 400

    try:
        # Сохраняем оригинал
        ext = os.path.splitext(file.filename)[1]
        orig_id = uuid.uuid4().hex
        orig_path = os.path.join(UPLOAD_DIR, f"{orig_id}{ext}")
        file.save(orig_path)

        # Удаляем фон
        with open(orig_path, 'rb') as f:
            input_data = f.read()
        output_data = remove(input_data)

        # Сохраняем PNG с прозрачностью
        proc_path = os.path.join(PROCESSED_DIR, f"{orig_id}.png")
        with open(proc_path, 'wb') as f:
            f.write(output_data)

        app.logger.info(f"Обработано: {orig_path} -> {proc_path}")
        return jsonify({'url': f"/static/processed/{orig_id}.png"})

    except Exception as e:
        app.logger.error(f"Ошибка обработки: {e}")
        return jsonify({'error': 'Ошибка обработки изображения'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
