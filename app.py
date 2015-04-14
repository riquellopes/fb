# coding: utf-8
import requests
import json
from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['GRAPH_FB'] = "http://graph.facebook.com/{}"
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'ldeyrweuy11yu2333uy3iu'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fb.db'
app.config['SQLALCHEMY_ECHO'] = False
db = SQLAlchemy(app)


class Person(db.Model):
    __tablename__ = 'person'
    username = db.Column(db.String(100))
    facebookId = db.Column('facebookId', db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    gender = db.Column(db.String(60))

    @property
    def serialize(self):
        return {
            'username': self.username,
            'facebookid': self.facebookId,
            'name': self.name,
            'gender': self.gender
        }


@app.route("/person/", methods=['POST'])
def post():
    response = requests.get(app.config['GRAPH_FB'].format(request.form.get('facebookid')))
    json = response.json()
    p = Person(**{
        'username': json['username'],
        'facebookId': json['id'],
        'name': json['name'],
        'gender': json['gender']
    })
    db.session.add(p)
    db.session.commit()
    return "", 201


@app.route("/person/<string:id>", methods=['DELETE'])
def delete(id):
    Person.query.get(id).query.delete()
    db.session.commit()
    return "", 204


@app.route("/person/", methods=['GET'])
def get():
    limit = request.args.get('limit', None)
    p = Person.query.filter()
    if limit is not None:
        p = p.limit(limit)
    return Response(json.dumps([i.serialize for i in p], indent=2), mimetype='application/json')
if __name__ == '__main__':
    db.create_all()
    app.run()
