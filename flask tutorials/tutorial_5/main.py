from flask import Flask, render_template, request, redirect, url_for, session, make_response


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
    error1 = None
    error2 = None
    if not request.form['pass'] or not request.form['email']:
        error1 = 'The input box should not be blank!\n \
Please insert your credentials.'
        return render_template("login.html", error1=error1, error2=error2)
    if (
      request.method == 'POST' and request.form['pass'] == 'admin' and
      request.form['email'] == 'admin'
    ):
        session['logged_in'] = True
        return render_template("success.html")
    error2 = 'Invalid credential'
    return render_template("login.html", error1=error1, error2=error2)


@app.route('/success')
def success():
    return "You have logged in successfully!"


@app.route("/cookie_test/", methods=["GET"])
def index():
    response = make_response("Here, take some cookie!")
    response.headers["Set-Cookie"] = "myfirstcookie=somecookievalue"
    return response


if __name__ == '__main__':
    app.run(debug=True)
