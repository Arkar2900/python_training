from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import time
import os


app = Flask(__name__)


@app.route('/')
def student():
    return render_template('student.html')


@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        result = request.form
        return render_template("result.html", result=result)


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        my_file = request.files['file']
        timestr = time.strftime("%Y%m%d")
        print(timestr)
        path = os.getcwd()
        folder_name = r'\my_folder'
        folder_time = r'\{}'.format(timestr)
        if not os.path.exists(path + folder_name):
            os.mkdir(path + folder_name)
        folder_to_save_files = path + folder_name + folder_time
        if not os.path.exists(folder_to_save_files):
            os.mkdir(folder_to_save_files)
        my_file.save(os.path.join(folder_to_save_files, my_file.filename))
        print(os.path.join(folder_to_save_files, my_file.filename))
        return 'file uploaded successfully'


if __name__ == '__main__':
    app.run(debug=True)
