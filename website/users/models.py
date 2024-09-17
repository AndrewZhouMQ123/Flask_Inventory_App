# create db tables first and connect app to database
# or create db tables using sqlalchemy and flask migrate
# running the query script on the db in terminal: sqlite3 instance/testdb.db < prova.sql
from flask_login import UserMixin

from website import db
    
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)
    phone = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    description = db.Column(db.String)
    # One-to-One relationship with Person
    person = db.relationship('Person', back_populates='user', uselist=False, lazy=True)


    def __repr__(self):
        return f'<User: {self.username}, Role: {self.role}>'
    
    def get_id(self):
        return self.id