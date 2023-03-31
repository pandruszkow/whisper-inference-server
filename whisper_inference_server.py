import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename

from persistent_transcriber import PersistentTranscriber

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'

transcriber = PersistentTranscriber()


@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/reload', methods=['POST'])
def reload_model():
    global transcriber
    model_name = request.get_json().get('model_name', 'medium')
    transcriber = PersistentTranscriber(model_name)
    return jsonify({'message': f'Model {model_name} loaded'}), 200


@app.route('/recognise', methods=['POST'])
def recognise():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    transcription = transcriber.transcribe_file(filepath)
    os.remove(filepath)
    return jsonify({'transcription': transcription}), 200


if __name__ == '__main__':
    os.makedirs(name=app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run()
