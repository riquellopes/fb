# coding: utf-8
import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'ldeyrweuy11yu2333uy3iu'
app.config['DATA_BASE_URI'] = 'sqlite:///fb.db'
db = SQLAlchemy(app)

@app.route("/<string:id>", methods=['GET'])
def get(id):
    return "1"


@app.route("/<string:id>", methods=['DELETE'])
def delete(id):
    return "2"


if __name__ == '__main__':
    app.run()
