from website import db
class Person(db.Model):
    __tablename__ = 'people'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False) # POSTGRE: db.Column(String(255))
    age = db.Column(db.Integer)
    job = db.Column(db.String)
    # ForeignKey to User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    # One-to-One relationship with User
    user = db.relationship('User', back_populates='person', uselist=False, lazy=True)
    # One-to-Many relationship with Todo
    todos = db.relationship('Todo', backref='person', lazy=True)

    def __repr__(self):
        return f'Person with name {self.name} and age {self.age}'
    
    def get_id(self):
        return self.id