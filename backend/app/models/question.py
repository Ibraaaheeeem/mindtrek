from app import db
from sqlalchemy.dialects.postgresql import ARRAY


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_text = db.Column(db.String(1024), nullable=False)
    
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategories.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    option_a = db.Column(db.String(512))
    option_b = db.Column(db.String(512))
    option_c = db.Column(db.String(512))
    option_d = db.Column(db.String(512))
    option_e = db.Column(db.String(512))

    tags = db.Column(ARRAY(db.String(124)))
    correct_options = db.Column(ARRAY(db.CHAR), nullable=False)
    explanation = db.Column(db.String(1024))

    comments = db.relationship('Comment', back_populates='question', cascade='all, delete-orphan')


    def serialize(self):
        return {
            'id': self.id,
            'question_text': self.question_text,
            'option_a': self.option_a,
            'option_b': self.option_b,
            'option_c': self.option_c,
            'option_d': self.option_d,
            'option_e': self.option_e,
            'correct_options': self.correct_options,
            'explanation': self.explanation

        }
    
    def __repr__(self):
        return f'<Question {self.question_text}>'