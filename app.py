from flask import Flask, render_template, url_for
from werkzeug.utils import redirect

from Test import ml

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/load")
def load():
    ml()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
