from app import db
from datetime import datetime

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
    password = db.Column(db.String(120), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen_date = db.Column(db.DateTime, default=datetime.utcnow)

    attempts = db.relationship('Attempt', back_populates='user')
    attempts = db.relationship('Comment', back_populates='user')

    def __repr__(self):
        return f'<User {self.username}>'

class MockSubject(db.Model):
    __tablename__ = 'mock_subjects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    num_questions = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<MockSubject {self.name}>'
    
class Attempt(db.Model):
    __tablename__ = 'exam_attempts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration of the exam in minutes
    date_taken = db.Column(db.DateTime, default=datetime.utcnow)
    total_score = db.Column(db.Float, default=0.0)
    total_possible_score = db.Column(db.Float, default=0.0)

    # Define a many-to-many relationship between Attempt and MockSubject
    subjects_taken = db.relationship('MockSubject', secondary='exam_subjects',
                                     back_populates='attempts_taken')

class ExamSubjects(db.Model):
    __tablename__ = 'exam_subjects'

    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('exam_attempts.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('mock_subjects.id'), nullable=False)
    score = db.Column(db.Float, default=0.0)

    # Define many to many relationships
    attempt = db.relationship('Attempt', back_populates='exam_subjects')
    subject = db.relationship('MockSubject', back_populates='exam_subjects')
    