from flask import Flask, render_template, request, redirect, url_for, session


# Initializing the Flask application
app = Flask(__name__)
app.secret_key = "sdfasdfasdfas111"


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/logout')
def logout():
    session['logged_in'] = None
    return redirect(url_for('home'))


@app.route('/validate', methods=['POST'])
def validate():
    if (
      request.method == 'POST' and request.form['pass'] == 'admin' and
      request.form['email'] == 'admin'
    ):
        session['logged_in'] = True
        return render_template("success.html")
    return redirect(url_for("login"))


@app.route('/success')
def success():
    return "You have logged in successfully!"


if __name__ == '__main__':
    app.run(debug=True)
