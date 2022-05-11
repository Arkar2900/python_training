from click import option
from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return "Hello, this is the first flask program!"


if __name__ == '__main__':
    app.run(port=8080)
