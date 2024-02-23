from flask import Blueprint, render_template, jsonify, request
from ..models.categories import Category, Subcategory, Subject, Unit
from ..models.question import Question

from app import db

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/categories', methods=['POST'])
def new_category():
    """
    Creates a new category in the database if it doesn't currently exist
    """
    data = request.json
    if not data:
        return jsonify({"error": "JSON data is missing"}), 400

    category_name = data.get("category_name")
    if not category_name.strip():
        return jsonify({"error": "Category name is empty"}), 400

    existing_category = Category.query.filter_by(name=category_name).first()
    if existing_category:
        return jsonify({"info": "Category already exists", "id": existing_category.id}), 409

    new_category = Category(name=category_name)
    db.session.add(new_category)
    db.session.commit()

    return jsonify({"info": "Category added successfully", "id": new_category.id, "name": new_category.name}), 201



@admin_bp.route('/subcategories', methods=['POST'])
def new_subcategory():
    """
    Creates a new subcategory in the database under the specified category if it doesn't currently exist
    """
    data = request.json
    if not data:
        return jsonify({"error": "JSON data is missing"}), 400

    subcategory_name = data.get("subcategory_name")
    category_id = data.get("category_id")

    if not subcategory_name.strip():
        return jsonify({"error": "Subcategory name is empty"}), 400

    category_exists = Category.query.get(category_id)
    if not category_exists:
        return jsonify({"info": "Specified category does not exist"}), 404

    subcategory_exists = Subcategory.query.filter_by(name=subcategory_name, category_id=category_id).first()
    if subcategory_exists:
        return jsonify({"info": "Subcategory already exists", "id": subcategory_exists.id}), 409

    new_subcategory = Subcategory(name=subcategory_name, category_id=category_id)
    db.session.add(new_subcategory)
    db.session.commit()

    return jsonify({"id": new_subcategory.id, "name": new_subcategory.name}), 201


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

    subject_name = data.get("subject_name")
    subcategory_id = data.get("subcategory_id")

    if not subject_name.strip():
        return jsonify({"error": "Subject name is empty"}), 400

    subcategory_exists = Subcategory.query.get(subcategory_id)
    if not subcategory_exists:
        return jsonify({"info": "Specified subcategory does not exist"}), 404

    subject_exists = Subject.query.filter_by(name=subject_name, subcategory_id=subcategory_id).first()
    if subject_exists:
        return jsonify({"info": "Subject already exists", "id": subject_exists.id}), 409

    new_subject = Subject(name=subject_name, subcategory_id=subcategory_id)
    db.session.add(new_subject)
    db.session.commit()

    return jsonify({"id": new_subject.id, "name": new_subject.name}), 201



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

    unit_name = data.get("unit_name")
    subject_id = data.get("subject_id")

    if not unit_name.strip():
        return jsonify({"error": "Unit name is empty"}), 400

    subject_exists = Subject.query.get(subject_id)
    if not subject_exists:
        return jsonify({"info": "Specified subject does not exist"}), 404

    unit_exists = Unit.query.filter_by(name=unit_name, subject_id=subject_id).first()
    if unit_exists:
        return jsonify({"info": "Unit already exists", "id": unit_exists.id}), 409

    new_unit = Unit(name=unit_name, subject_id=subject_id)
    db.session.add(new_unit)
    db.session.commit()

    return jsonify({"id": new_unit.id, "name": new_unit.name}), 201


@admin_bp.route('/questions', methods=['POST'])
def upload_questions():
    data = request.json
    if not data:
        return jsonify({"error": "JSON data is missing"}), 400

    unit_id = data.get("unit_id")
    subject_id = data.get("subject_id")
    subcategory_id = data.get("subcategory_id")
    category_id = data.get("category_id")

    questions = data.get("questions")
    if not questions:
        return jsonify({"error": "No questions data"}), 400

    try:
        addition_counter = 0
        error_counter = 0
        
        for qrow in questions:
            row = qrow.split("||")
            if len(row) < 8:
                error_counter += 1
                continue
            
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
                correct_options=list(row[6]),
                explanation=row[7]
            )
            db.session.add(question)
            addition_counter += 1
        
        db.session.commit()
        return jsonify({
            "message": "Questions data uploaded successfully",
            "received": len(questions),
            "added": addition_counter,
            "error": error_counter
        }), 201

    except Exception as e:
        db.session.rollback()  # Rollback the transaction on error
        return jsonify({"error": f"Error processing questions data: {str(e)}"}), 500

    
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
    
@admin_bp.route('/upload-form', methods=['GET'])
def show_upload_form():
    categories = Category.query.all()
    categories_list = [{'id': category.id, 'name': category.name}
                     for category in categories]
    return render_template('upload-form.html', categories=categories_list)
