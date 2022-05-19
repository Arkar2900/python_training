from flask import Flask, render_template, request
import time
from datetime import datetime
import os


app = Flask(__name__)


@app.route('/')
def student():
    return render_template('student.html')


@app.route('/result', methods=['POST'])
def result():
    message = None
    if request.method == 'POST':
        physics = request.form.get('physics')
        chemistry = request.form.get('chemistry')
        mathematics = request.form.get('mathematics')
        startdate = datetime.strptime(request.form['startdate'], '%Y-%m-%d')
        if(not physics.isdigit() or not chemistry.isdigit()
           or not mathematics.isdigit()):
            message = 'The marks should be integer number'
            return render_template('student.html', message=message)
        result = request.form
        return render_template('result.html', result=result, startdate=startdate)


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        my_file = request.files['file']
        timestr = time.strftime('%Y%m%d')
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
