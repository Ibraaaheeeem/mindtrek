from app import db
from sqlalchemy.dialects.postgresql import ARRAY


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_text = db.Column(db.String(1024), nullable=False)
    
    # Foreign keys referencing other tables
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategories.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    # Option fields
    option_a = db.Column(db.String(512))
    option_b = db.Column(db.String(512))
    option_c = db.Column(db.String(512))
    option_d = db.Column(db.String(512))
    option_e = db.Column(db.String(512))

    # Tags and correct options stored as PostgreSQL arrays
    tags = db.Column(ARRAY(db.String(124)))
    correct_options = db.Column(ARRAY(db.CHAR), nullable=False)
    explanation = db.Column(db.String(1024))

    # Relationship with Comment model
    comments = db.relationship('Comment', back_populates='question', cascade='all, delete-orphan')

    # Method to serialize the object into a dictionary
    def serialize(self):
        return {
            'id': self.id,
            'question': self.question_text,
            'option_a': self.option_a,
            'option_b': self.option_b,
            'option_c': self.option_c,
            'option_d': self.option_d,
            'option_e': self.option_e,
            'answer': "".join(self.correct_options),
            'explanation': self.explanation

        }
    
    # String representation of the object
    def __repr__(self):
        return f'<Question {self.question_text}>'