import random
import pandas as pd
from flask import Blueprint, render_template, jsonify, request
from ..models.categories import Category, Subcategory, Subject, Unit
from ..models.question import Question

from app import db

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/categories', methods=['POST'])
def new_category():
    """
    Creates a new category in database
    if it doesn't currently exist
    """
    data = request.json
    if not data:
        return jsonify({"error": "JSON data is missing"}), 400
    print('inside')
    category_name = data.get("category_name")
    print(category_name)
    categoryexists = Category.query.filter_by(name=category_name).first()
    if categoryexists is None:
        category = Category(name=category_name)
        db.session.add(category)
        db.session.commit()
        return jsonify({"info": "Category added successfully", "id": category.id, "name":category.name}), 201
    else:
        return jsonify({"info": "Category exists already", "id": categoryexists.id}), 409


@admin_bp.route('/subcategories', methods=['POST'])
def new_subcategory():
    """
    Creates a new subcategory in database
    under the specified category
    if it doesn't currently exist
    """
    
    data = request.json
    if not data:
        return jsonify({"error": "JSON data is missing"}), 400
    print('inside')
    subcategory_name = data.get("subcategory_name")
    
    category_id = data.get("category_id")
    categoryexists = Category.query.filter_by(id=category_id).first()
    if categoryexists == None:
        return jsonify({"info": "Specified category does not exist"}),404
    
    subcategoryexists = Subcategory.query.filter_by(
        name=subcategory_name, category_id=category_id).first()
    if subcategoryexists is None:
        subcategory = Subcategory(
            name=subcategory_name, category_id=category_id
        )
        db.session.add(subcategory)
        db.session.commit()
        return jsonify({"id": subcategory.id, "name":subcategory.name}), 201
    else:
        return jsonify({"info": "SubCategory exists already", "id": subcategoryexists.id}), 409

@admin_bp.route('/subjects', methods=['POST'])
def new_subject():
    """
    Creates a new subject in database
    under the specified subcategory
    if it doesn't currently exist
    """
    
    data = request.json
    if not data:
        return jsonify({"error": "JSON data is missing"}), 400
    print('inside')

    subject_name = data.get("subject_name")
    subcategory_id = data.get("subcategory_id")

    subcategoryexists = Subcategory.query.filter_by(id=subcategory_id).first()
    if subcategoryexists == None:
        return jsonify({"info": "Specified subcategory does not exist"}), 404
    
    
    subjectexists = Subject.query.filter_by(
        name=subject_name, subcategory_id=subcategory_id).first()
    if subjectexists is None:
        subject = Subject(
            name=subject_name, subcategory_id=subcategory_id
        )
        db.session.add(subject)
        db.session.commit()
        return jsonify({"id": subject.id, "name": subject.name}), 201
    else:
        return jsonify({"info": "Subject exists already", "id": subjectexists.id}), 409


@admin_bp.route('/units', methods=['POST'])
def new_unit():
    """
    Creates a new unit in database
    under the specified subject
    if it doesn't currently exist
    """
    
    data = request.json
    if not data:
        return jsonify({"error": "JSON data is missing"}), 400
    print('inside')
    unit_name = data.get("unit_name")
    subject_id = data.get("subject_id")
    subjectexists = Subject.query.filter_by(id=subject_id).first()
    if subjectexists == None:
        return jsonify({"info": "Specified subject does not exist"}), 404
    unitexists = Unit.query.filter_by(
        name=unit_name, subject_id=subject_id).first()
    if unitexists is None:
        unit = Unit(
            name=unit_name, subject_id=subject_id
        )
        db.session.add(unit)
        db.session.commit()
        return jsonify({"id": unit.id, "name": unit.name}), 201
    else:
        return jsonify({"info": "Unit exists already", "id": unitexists.id}), 409

@admin_bp.route('/questions', methods=['POST'])
def upload_questions():
    data = request.json
    if not data:
        return jsonify({"error": "JSON data is missing"}), 400
    print('inside')
    unit_id = data.get("unit_id")
    subject_id = data.get("subject_id")
    subcategory_id = data.get("subcategory_id")
    category_id = data.get("category_id")

    questions = data.get("questions").splitlines()
    addition_counter = 0
    error_counter = 0
    if not questions:
        return jsonify({"error": "No questions data"}), 400
    try:
        
        for qrow in questions:
            row = qrow.split("||")
            if len(row) < 9:
                error_counter += 1
                continue
            print(row[0])
            question = Question(
                unit_id=unit_id,
                subject_id=subject_id,
                subcategory_id=subcategory_id,
                category_id=category_id,
                tags=row[0].split(","),
                question_text=row[1],
                option_a=row[2],
                option_b=row[3],
                option_c=row[4],
                option_d=row[5],
                option_e=row[6],
                correct_options=list(row[7]),
                explanation=row[8]
            )
            db.session.add(question)
            addition_counter += 1
        db.session.commit()
        return jsonify({"message": "Questions data uploaded successfully","received": len(questions), "added": addition_counter, "error": error_counter}), 201
    except Exception as e:
        return jsonify({"error": f"Error processing Questions data: {str(e)}"}), 500
    
@admin_bp.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = Category.query.get(category_id)
    if category:
        db.session.delete(category)
        db.session.commit()
        return jsonify({"message": "Category ${category.name} deleted successfully"}), 204
    else:
        return jsonify({"message": "Category ${category.name} not found"}), 404

@admin_bp.route('/subcategory/<int:subcategory_id>', methods=['DELETE'])
def delete_subcategory(subcategory_id):
    subcategory = Subcategory.query.get(subcategory_id)
    if subcategory:
        db.session.delete(subcategory)
        db.session.commit()
        return jsonify({"message": "Subcategory ${subcategory.name} deleted successfully"}), 204
    else:
        return jsonify({"message": "Subcategory ${subcategory.name} not found"}), 404

@admin_bp.route('/subject/<int:subject_id>', methods=['DELETE'])
def delete_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if subject:
        db.session.delete(subject)
        db.session.commit()
        return jsonify({"message": "Subject ${subject.name} deleted successfully"}), 204
    else:
        return jsonify({"message": "Subject ${subject.name} not found"}), 404

@admin_bp.route('/unit/<int:unit_id>', methods=['DELETE'])
def delete_unit(unit_id):
    unit = Unit.query.get(unit_id)
    if unit:
        db.session.delete(unit)
        db.session.commit()
        return jsonify({"message": "Unit ${unit.name} deleted successfully"}), 204
    else:
        return jsonify({"message": "Unit ${unit.name} not found"}), 404

@admin_bp.route('/question/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    question = Question.query.get(question_id)
    if question:
        db.session.delete(question_id)
        db.session.commit()
        return jsonify({"message": "Question ${question_id} deleted successfully"}), 204
    else:
        return jsonify({"message": "Question ${question_id} not found"}), 404