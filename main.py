# Здесь происходит определение ответов различных запросов Фласком.

from flask import Flask
from flask import render_template
import models

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")
