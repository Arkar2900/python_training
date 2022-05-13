from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)


@app.route('/hello')
def hello_world():
    return 'hello world'


app.add_url_rule('/hello_world', 'hi', hello_world)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin/<name>')
def hello_admin(name):
    return 'Hello Admin,  %s' % name


@app.route('/guest/<name>')
def hello_guest(name):
    return '%s is unauthorized user.' % name


@app.route('/login', methods=['POST', 'GET'])
def login():
    admin = "MTH"
    user = request.form['nm'].upper()
    if user == admin:
        return redirect(url_for('hello_admin', name=user))
    else:
        return redirect(url_for('hello_guest', name=user))


if __name__ == '__main__':
    app.run(debug=True)
