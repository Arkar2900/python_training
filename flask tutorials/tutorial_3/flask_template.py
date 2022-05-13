from flask import Flask, render_template


app = Flask(__name__)


@app.route('/hello/<int:score>')
def hello_name(score):
    return render_template('hello.html', marks=score)


@app.route('/result')
def result():
    result = {'phy': 50, 'che': 60, 'maths': 70}
    return render_template('result.html', result=result)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/press", methods=['post'])
def press():
    return 'You pressed the submit button!'


if __name__ == '__main__':
    app.run(debug=True)
