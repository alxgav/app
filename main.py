import os

import services
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from flask import Flask, request
from flask import render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Create a directory to store the uploaded files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Allow only text files


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# this endpoint will handle the file upload and not use in this project
@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        files = request.files.getlist('file')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File uploaded successfully'

@app.route("/")
def hello_world():
    stations = services.get_stations()
    final_response = services.get_final_data()
    data = {
        "stations": stations,
        "final_response": final_response}
    return render_template('index.html', data=data)
