from website import db
class Person(db.Model):
    __tablename__ = 'people'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False) # POSTGRE: db.Column(String(255))
    age = db.Column(db.Integer)
    job = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Person with name {self.name} and age {self.age}'
    
    def get_id(self):
        return self.pid