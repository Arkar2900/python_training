from flask import Flask, render_template, request
from werkzeug.utils import secure_filename


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
        f = request.files['file']
        f.save(secure_filename(f.filename))
        st1 = 'file uploaded successfully'
        print(f.filename)
        return st1


if __name__ == '__main__':
    app.run(debug=True)