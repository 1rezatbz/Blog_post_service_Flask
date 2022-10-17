from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '539d4d8ff1d0bbe8ce8eb190c5624d14'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db.db'
db = SQLAlchemy(app)


from src import routes



