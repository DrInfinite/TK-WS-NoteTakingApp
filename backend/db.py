from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import UUIDType

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db = SQLAlchemy(app)


# The User class is a model that represents a user. It has an id, name, password, and a relationship
# to the Notebook class
class User(db.Model):
    id = db.Column(UUIDType(binary=False), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    notebooks = db.relationship('Notebook', backref='user', lazy=True)

    def __repr__(self):
        return f"User(id='{self.id}', name='{self.name}', '{self.password}')"


# The Notebook class is a database model that has a one-to-many relationship with the Note class.
class Notebook(db.Model):
    id = db.Column(UUIDType(binary=False), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    pages = db.relationship('Note', backref='notebook', lazy=True)

    def __repr__(self):
        return f"Notebook(id='{self.id}', title='{self.title}', user_id='{self.user_id}')"


# The Page class is a model that represents a page in a notebook. It has an id, title, content, and a
# relationship to the Notebook class.
# The Page class inherits from the db.Model class.
class Page(db.Model):
    id = db.Column(UUIDType(binary=False), primary_key=True)
    notebook_id = db.Column(db.Integer, db.ForeignKey(
        'notebook.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Page(id='{self.id}', title='{self.title}', notebook_id='{self.notebook_id}', content='{self.content}')"


app.app_context().push()

db.create_all()
