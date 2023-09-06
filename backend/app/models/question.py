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

    def __repr__(self):
        return f'<Question {self.question_text}>'