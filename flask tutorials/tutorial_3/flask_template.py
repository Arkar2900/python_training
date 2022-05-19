from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/hello/<int:score>')
def hello_name(score):
    return render_template('hello.html', marks=score)


@app.route('/result')
def result():
    result = {'phy': 50, 'che': 60, 'maths': 70}
    return render_template('result.html', result=result)


@app.route('/')
def index():
    message = None
    return render_template('index.html', message=message)


@app.route('/press', methods=['POST', 'GET'])
def press():
    message = None
    if request.method == 'POST':
        name = request.form['name']
        mail = request.form['mail']
        pw = request.form['pw']
        check_pw = request.form['check_pw']
        if not name or not mail or not pw or not check_pw:
            message = 'The input box should not be blank'
            return render_template('index.html', message=message)
        if pw != check_pw:
            message = 'The password and re-entered password should be same.\
Please enter agian!'
            return render_template('index.html', message=message)
        return 'You pressed the submit button. It is successfully submitted!'


if __name__ == '__main__':
    app.run(debug=True)
