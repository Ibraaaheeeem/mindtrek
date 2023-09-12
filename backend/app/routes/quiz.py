import random
import pandas as pd
from flask import Blueprint, jsonify, request
from app import db, jwt
from ..models.social import User
from ..models.categories import Category, Subcategory, Subject, Unit
from ..models.question import Question

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/categories', methods=['GET'])
def get_categories():
    """
    Returns a list of all the categories in the database

    """
    categories = Category.query.all()
    category_list = [{'id': category.id, 'name': category.name}
                     for category in categories]
    return jsonify(category_list)


@quiz_bp.route('/subcategories/<int:category_id>', methods=['GET'])
def get_subcategories(category_id):
    """
    Returns a list of all the subcategories in the database
    under the specified category id

    """
    subcategories = Subcategory.query.filter_by(category_id=category_id).all()
    subcategory_list = [{'id': subcategory.id, 'name': subcategory.name}
                        for subcategory in subcategories]
    return jsonify(subcategory_list)


@quiz_bp.route('/subjects/<int:subcategory_id>', methods=['GET'])
def get_subjects(subcategory_id):
    """
    Returns a list of all the subjects in the database
    under the specified subcategory id

    """
    subjects = Subject.query.filter_by(subcategory_id=subcategory_id).all()
    subject_list = [{'id': subject.id, 'name': subject.name}
                    for subject in subjects]
    return jsonify(subject_list)


@quiz_bp.route('/units/<int:subject_id>', methods=['GET'])
def get_units(subject_id):
    """
    Returns a list of all the units in the database
    under the specified subject id

    """
    units = Unit.query.filter_by(subject_id=subject_id).all()
    unit_list = [{'id': unit.id, 'name': unit.name}
                 for unit in units]
    print(unit_list)
    return jsonify(unit_list)


@quiz_bp.route('/questions/category/<int:category_id>/subcategory/<int:subcategory_id>/subject/<int:subject_id>/unit/<int:unit_id>', methods=['GET'])
def get_questions(category_id, subcategory_id, subject_id, unit_id):
    """
    Returns a speciifed number of questions that
    satisifes the paremeters. The highest category
    level will be used in selecting the questions.
    When questions of higher specificity are needed,
    the lower heirarchy should be utilised
    """
    n = int(request.args.get('n', 1))
    questions = None
    if category_id != 0:
        questions = Question.query.filter_by(category_id=category_id).all()
    elif subcategory_id != 0:
        questions = Question.query.filter_by(
            subcategory_id=subcategory_id).all()
    elif subject_id != 0:
        questions = Question.query.filter_by(subject_id=subject_id).all()
    elif unit_id != 0:
        questions = Question.query.filter_by(unit_id=unit_id).all()

    if questions == None:
        return jsonify({"message": "No questions found"})
    random_questions = random.sample(questions, min(n, len(questions)))

    question_data_list = []
    for question in random_questions:
        question_data = {
            'id': question.id,
            'question_text': question.question_text,
            'option_a': question.option_a,
            'option_b': question.option_b,
            'option_c': question.option_c,
            'option_d': question.option_d,
            'option_e': question.option_e,
            'tags': question.tags,
            'correct_options': question.correct_options,
            'explanation': question.explanation
        }
        question_data_list.append(question_data)
    return jsonify(question_data_list)

@quiz_bp.route('/question/<int:question_id>/comments', methods=['GET'])
def get_comments(question_id):
    """
    Returns a list of all the comments
    related to the question with its id
    """
    try:
        question = Question.query.get(question_id)
        comments = question.comments
        comments_list = [{"id": comment.id,
                          "text": comment.text,
                          "author": comment.user.username,
                          "likes": comment.likes,
                          "quotes": comment.quotes,
                          "replies": len(comment.subcomments),
                          "edited": comment.edited
                          } for comment in comments]
        return jsonify(comments_list), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_hierarchy(node):
    if node is None:
        return []
    hierarchy = {
        'name': node.name,
        'subcategories': [get_hierarchy(subcat) for subcat in node.subcategories],
        'subjects': [get_hierarchy(subject) for subject in node.subjects],
        'units': [unit.name for unit in node.units]
    }
    return hierarchy

@quiz_bp.route('/get_all_categories', methods=['GET'])
def get_all_categories():
    all_categories = Category.query.all()
    
    def get_subcategories(category_id):
        subcategories = Subcategory.query.filter_by(category_id=category_id).all()
        for subcategory in subcategories:
            subcategory.subjects = get_subjects(subcategory.id)
        return subcategories
    
    def get_subjects(subcategory_id):
        subjects = Subject.query.filter_by(subcategory_id=subcategory_id).all()
        for subject in subjects:
            subject.units = get_units(subject.id)
        return subjects
    
    def get_units(subject_id):
        return Unit.query.filter_by(subject_id=subject_id).all()
    
    for category in all_categories:
        category.subcategories = get_subcategories(category.id)
    
    return jsonify([category.serialize() for category in all_categories])
