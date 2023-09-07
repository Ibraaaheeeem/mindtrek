from app import db
from datetime import datetime

exam_subjects = db.Table('exam_subjects',
    db.Column('attempt_id', db.Integer, db.ForeignKey('exam_attempts.id'), primary_key=True),
    db.Column('subject_id', db.Integer, db.ForeignKey('mock_subjects.id'), primary_key=True),
    db.Column('score', db.Float, default=0.0)
)

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(2000), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    question = db.relationship('Question', backref='comments')
    user = db.relationship('User', backref='user')

    def __repr__(self):
        return f'<Comment {self.id}>'

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen_date = db.Column(db.DateTime, default=datetime.utcnow)
    attempts = db.relationship('Attempt', back_populates='user')
    comments = db.relationship('Comment', back_populates='user')

    def __repr__(self):
        return f'<User {self.username}>'

class MockSubject(db.Model):
    __tablename__ = 'mock_subjects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    num_questions = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Float, nullable=False)
    
    attempts_taken = db.relationship('Attempt', secondary='exam_subjects',
                                     back_populates='subjects_taken')
    
    def __repr__(self):
        return f'<MockSubject {self.name}>'
    
class Attempt(db.Model):
    __tablename__ = 'exam_attempts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration of the exam in minutes
    date_taken = db.Column(db.DateTime, default=datetime.utcnow)
    total_score = db.Column(db.Float, default=0.0)
    total_possible_score = db.Column(db.Float, default=0.0)
    
    user = db.relationship('User', back_populates='attempts')
    # Define a many-to-many relationship between Attempt and MockSubject
    subjects_taken = db.relationship('MockSubject', secondary='exam_subjects',
                                     back_populates='attempts_taken')