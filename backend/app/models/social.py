from app import db
from datetime import datetime


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(2000), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey(
        'questions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    likes = db.Column(db.Integer, default=0)
    quotes = db.Column(db.Integer, default=0)
    replies = db.Column(db.Integer, default=0)
    edited = db.Column(db.Boolean, default=False)
    question = db.relationship('Question', back_populates='comments')
    user = db.relationship('User', back_populates='comments')
    subcomments = db.relationship(
        'Subcomment', back_populates='comment', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Comment {self.id}>'


class Subcomment(db.Model):
    __tablename__ = 'subcomments'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(2000), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey(
        'comments.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    edited = db.Column(db.Boolean, default=False)
    comment = db.relationship('Comment', back_populates='subcomments')

    def __repr__(self):
        return f'<Subcomment {self.id}>'


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen_date = db.Column(db.DateTime, default=datetime.utcnow)
    attempts = db.relationship(
        'Attempt', back_populates='user', cascade='all, delete-orphan')
    comments = db.relationship('Comment', back_populates='user')

    def __repr__(self):
        return f'<User {self.username}>'


class MockSubject(db.Model):
    __tablename__ = 'mock_subjects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    num_questions = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, default=0)
    attempts_taken = db.relationship('Attempt', secondary='exam_subjects',
                                     back_populates='subjects_taken')

    def __repr__(self):
        return f'<MockSubject {self.name}>'


class Attempt(db.Model):
    __tablename__ = 'attempts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Duration of the exam in minutes
    duration = db.Column(db.Integer, nullable=False)
    date_taken = db.Column(db.DateTime, default=datetime.utcnow)
    total_score = db.Column(db.Integer, default=0)
    total_possible_score = db.Column(db.Integer, default=0)

    user = db.relationship('User', back_populates='attempts')
    # Define a many-to-many relationship between Attempt and MockSubject
    subjects_taken = db.relationship('MockSubject', secondary='exam_subjects',
                                     single_parent=True, cascade='all, delete-orphan',
                                     back_populates='attempts_taken')

    def add_mock_subject(self, mock_subject):
        """
        Add a MockSubject to the subjects_taken relationship.
        """
        self.subjects_taken.append(mock_subject)


exam_subjects = db.Table('exam_subjects',
                         db.Column('attempt_id', db.Integer, db.ForeignKey(
                             'attempts.id'), primary_key=True),
                         db.Column('subject_id', db.Integer, db.ForeignKey(
                             'mock_subjects.id'), primary_key=True),
                         db.Column('score', db.Integer, default=0)
                         )
