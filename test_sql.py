from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

class pref_sequence_data(db.Model):
    __tablename__ = 'pref_sequence_data'
    id = db.Column(db.Integer(), primary_key=True)
    sequency = db.Column(db.ARRAY(db.Integer))

data = pref_sequence_data(sequency=[1,2,3,42,3,423])
db.create_all()
db.session.add(data)

