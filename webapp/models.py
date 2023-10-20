from webapp import db, login_manager
from datetime import datetime
from flask_login import UserMixin

date = datetime.utcnow()
months = ['0', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    adm_no = db.Column(db.String(), unique=True, nullable=False)
    std = db.Column(db.Integer(), nullable=False)
    date_joined = db.Column(db.String, nullable=False, default=str(months[date.month])+' '+str(date.day)+', '+str(date.year))
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.adm_no}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.String, nullable=False, default=str(months[date.month])+' '+str(date.day)+', '+str(date.year))
    content = db.Column(db.Text, nullable=False)
    post_std = db.Column(db.Integer(), nullable=False)
    subject = db.Column(db.String(), nullable=False)
    post_image = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    answers = db.relationship('Answer', backref='question', lazy=True)

    def __repr__(self):
        return f"Post('{self.question}', '{self.date_posted}')"

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    answer_image = db.Column(db.String(100))
    date_posted = db.Column(db.String, nullable=False, default=str(months[date.month])+' '+str(date.day)+', '+str(date.year))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f"Answer('{self.post_id}', '{self.date_added}')"