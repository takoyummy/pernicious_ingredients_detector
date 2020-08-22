import collections
import os
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import time

client = MongoClient('localhost', 27017)
db = client.dbproject

UPLOAD_FOLDER = './static'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

path = ""
path_name = ""
result = ""


# HTML 화면 보여주기
@app.route('/')
def homework():
    return render_template('test4.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            global path_name
            path_name = filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            global path
            path = './static/' + path_name
            # return redirect(url_for('upload_file',
            #                         filename=filename))
            return render_template('test5.html')


def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    from google.cloud.vision import types
    import io
    import os

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./OCRAPI-b76498b09587.json"

    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')
    global result
    result = ""

    for text in texts:
        result += text.description

    all_hazard = list(db.project.find({}))
    array = []

    img_path = '../static/' + path_name
    dic_path = {'path': img_path}
    array.append(dic_path)

    for hazard in all_hazard:
        name = hazard['name']
        desc = hazard['desc']
        dic = {'name': name, 'desc': desc}
        if name in result:
            array.append(dic)
    print('최종 결과는')


    return array

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


@app.route('/result', methods=['GET'])
def view_orders():
    print('get실행')
    arrays = detect_text(path)
    print(arrays)
    return jsonify({'result': 'success', 'hazard': arrays})




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
