from website import db

class Todo(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    done = db.Column(db.Boolean, nullable=False, default=False)
    due_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"<TODO {self.title}, Done: {self.done}"
    
    def get_id(self):
        return self.id
    
    def set_done(self, done):
        self.done = done

    def set_duedate(self, duedate):
        self.due_date = duedate

    def set_title(self, title):
        self.title = title
    
    def set_description(self, description):
        self.description = description

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'done': self.done,
            'due_date': self.due_date.strftime('%Y-%m-%dT%H:%M'),
            'user_id': self.user_id,
        }