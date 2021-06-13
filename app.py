import os
import tempfile

from PIL import Image

from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

from embedder import ClipEmbedder


app = Flask(__name__)


clip_embedder = ClipEmbedder()


@app.route('/')
def index():
    return '''
    <!doctype html>
    <title>CLIP Embedder</title>
    <h1>Embed an image</h1>
    <form action=/embed/image method=post enctype=multipart/form-data>
      <input type=file name=image>
      <input type=submit value=Embed>
    </form>
    <h1>Embed text</h1>
    <form action=/embed/text method=post>
        <input type=text name=text>
        <input type=submit value=Embed>
    </form>
    '''


@app.route('/embed/image', methods=['POST'])
def embed_image():
    # check if the post request has the file part
    if 'image' not in request.files:
        return {
            'status': 'error',
            'error': 'No image part',
        }
    image_file = request.files['image']

    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if image_file.filename == '':
        return {
            'status': 'error',
            'error': 'No image selected',
        }

    filename = secure_filename(image_file.filename)
    _, path = tempfile.mkstemp()
    image_file.save(path)
    image = Image.open(path).convert('RGB')
    embedding = clip_embedder.embed_image(image)
    os.remove(path)
    return {
        'status': 'ok',
        'embedding': embedding.tolist(),
    }


@app.route('/embed/text', methods=['POST'])
def embed_text():
    if 'text' in request.form:
        text = request.form['text']
    else:
        text = request.data.decode('utf-8')

    text = text.strip()

    if text == '':
        return {
            'status': 'error',
            'error': 'Text is empty',
        }

    embedding = clip_embedder.embed_text(text)
    return {
        'status': 'ok',
        'embedding': embedding.tolist(),
    }


if __name__ == '__main__':
    import bjoern
    bjoern.run(app, '0.0.0.0', 8000)

