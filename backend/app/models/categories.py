from app import db 
from sqlalchemy.dialects.postgresql import ARRAY


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    subcategories = db.relationship('Subcategory', backref='category', lazy=True, cascade='all, delete-orphan')

    def serialize(self):
        
        return {
            'id': self.id,
            'name': self.name,
            'subcategories': [subcategory.serialize() for subcategory in self.subcategories],
            'nquestions': len(self.questions)
        }

    def __repr__(self):
        return f'<Category {self.name}>'

    @property
    def questions(self):
        from ..models import Question
        return db.session.query(Question).join(Subcategory).filter(Subcategory.category_id == self.id).all()


class Subcategory(db.Model):
    __tablename__ = 'subcategories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    subjects = db.relationship('Subject', backref='subcategory', lazy=True, cascade='all, delete-orphan')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'subjects': [subject.serialize() for subject in self.subjects],
            'nquestions': len(self.questions)
        }

    def __repr__(self):
        return f'<Subcategory {self.name}>'

    @property
    def questions(self):
        from ..models import Question
        return db.session.query(Question).filter_by(subcategory_id=self.id).all()


class Subject(db.Model):
    __tablename__ = 'subjects'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategories.id'), nullable=False)
    units = db.relationship('Unit', backref='subject', lazy=True, cascade='all, delete-orphan')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'units': [unit.serialize() for unit in self.units],
            'nquestions': len(self.questions)
        }

    def __repr__(self):
        return f'<Subject {self.name}>'

    @property
    def questions(self):
        from ..models import Question
        return db.session.query(Question).filter_by(subject_id=self.id).all()


class Unit(db.Model):
    __tablename__ = 'units'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    questions = db.relationship('Question', backref='unit', lazy=True, cascade='all, delete-orphan')
    tags = db.Column(ARRAY(db.String))
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'tags': self.tags,
            'nquestions': len(self.questions)
        }
    
    def __repr__(self):
        return f'<Unit {self.name}>'

    @property
    def questions(self):
        from ..models import Question
        return db.session.query(Question).filter_by(unit_id=self.id).all()
