import random
import pandas as pd
from flask import Blueprint, render_template, jsonify, request
from models.questions import Category, Subcategory, Subject, MCQQuestion, Unit
from app import db

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/category', methods=['POST'])
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
        return jsonify({"info": "Category added successfully"})
    else:
        return jsonify({"info": "Category exists already"})


@admin_bp.route('/subcategory', methods=['POST'])
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
        return jsonify({"info": "Specified category does not exist"})
    
    subcategoryexists = Subcategory.query.filter_by(
        name=subcategory_name, category_id=category_id).first()
    if subcategoryexists is None:
        subcategory = Subcategory(
            name=subcategory_name, category_id=category_id
        )
        db.session.add(subcategory)
        db.session.commit()
        return jsonify({"info": "Subcategory added successfully"})
    else:
        return jsonify({"info": "SubCategory exists already", "id": subcategoryexists.id})

@admin_bp.route('/subject', methods=['POST'])
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
        return jsonify({"info": "Specified subcategory does not exist"})
    
    
    subjectexists = Subject.query.filter_by(
        name=subject_name, subcategory_id=subcategory_id).first()
    if subjectexists is None:
        subject = Subject(
            name=subject_name, subcategory_id=subcategory_id
        )
        db.session.add(subject)
        db.session.commit()
        return jsonify({"info": "Subject added successfully"})
    else:
        return jsonify({"info": "Subject exists already", "id": subjectexists.id})


@admin_bp.route('/unit', methods=['POST'])
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
        return jsonify({"info": "Specified subject does not exist"})
    
    
    unitexists = Unit.query.filter_by(
        name=unit_name, subject_id=subject_id).first()
    if unitexists is None:
        unit = Unit(
            name=unit_name, subject_id=subject_id
        )
        db.session.add(unit)
        db.session.commit()
        return jsonify({"info": "Unit added successfully"})
    else:
        return jsonify({"info": "Unit exists already", "id": unitexists.id})

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

    questionsCSV = data.get("questions")
    questions = questionsCSV.splitlines()
    
    if not questions:
        return jsonify({"error": "No questions data"}), 400
    try:
        # csv_data = pd.read_csv(pd.compat.StringIO(questionsCSV))
        # print(len(questions))
        # print(f"{unit_id}-{subject_id}-{subcategory_id}-{category_id}")
        for qrow in questions:
            # print(qrow)
            row = qrow.split("||")
            if len(row) < 9:
                print(row[1])
                continue
            print(row[0])
            question = MCQQuestion(
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
        db.session.commit()
        return jsonify({"message": "Questions data uploaded successfully"}), 201
    except Exception as e:
        return jsonify({"error": f"Error processing Questions data: {str(e)}"}), 500