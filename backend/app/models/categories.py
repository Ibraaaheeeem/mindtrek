from app import db 
from sqlalchemy.dialects.postgresql import ARRAY

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    subcategories = db.relationship('Subcategory', backref='category', lazy=True, cascade='all, delete-orphan')

    def serialize(self):
        from ..models import Question
        questions = Question.query.filter_by(category_id=self.id).all()
        count = 0
        for question in questions:
            count += 1
        
        return {
            'id': self.id,
            'name': self.name,
            'subcategories': [subcategory.serialize() for subcategory in self.subcategories],
            'nquestions': len(questions)
        }

    def __repr__(self):
        return f'<Category {self.name}>'


class Subcategory(db.Model):
    __tablename__ = 'subcategories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    subjects = db.relationship('Subject', backref='subcategory', lazy=True, cascade='all, delete-orphan')

    def serialize(self):
        from ..models import Question
        questions = Question.query.filter_by(subcategory_id=self.id).all()
        count = 0
        for question in questions:
            count += 1
        
        return {
            'id': self.id,
            'name': self.name,
            'subjects': [subject.serialize() for subject in self.subjects],
            'nquestions': len(questions)
        }

    def __repr__(self):
        return f'<Subcategory {self.name}>'

class Subject(db.Model):
    __tablename__ = 'subjects'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategories.id'), nullable=False)
    units = db.relationship('Unit', backref='subject', lazy=True, cascade='all, delete-orphan')

    def serialize(self):
        from ..models import Question
        questions = Question.query.filter_by(subject_id=self.id).all()
        count = 0
        for question in questions:
            count += 1
        return {
            'id': self.id,
            'name': self.name,
            'units': [unit.serialize() for unit in self.units],
            'nquestions': len(questions)
        }

    def __repr__(self):
        return f'<Subject {self.name}>'

class Unit(db.Model):
    __tablename__ = 'units'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    questions = db.relationship('Question', backref='unit', lazy=True, cascade='all, delete-orphan')
    tags = db.Column(ARRAY(db.String))
    
    def serialize(self):
        from ..models import Question
        questions = Question.query.filter_by(unit_id=self.id).all()
        count = 0
        for question in questions:
            count += 1
        
        
        return {
            'id': self.id,
            'name': self.name,
            'tags': self.tags,
            'nquestions': len(questions)
        }
    
    def __repr__(self):
        return f'<Unit {self.name}>'