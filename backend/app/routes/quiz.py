import random
from flask import Blueprint, jsonify, request
from ..models.categories import Category, Subcategory, Subject, Unit
from ..models.question import Question

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Hello World"})

@quiz_bp.route('/categories/<int:index>', methods=['GET'])
def get_categories(index):
    """
    Returns a list of all the categories in the database

    """
    categories = Category.query.all()
    categories_data = [category.serialize() for category in categories]
    filtered_categories_data = [category_data for category_data in categories_data if category_data.get('nquestions', 0) > 0]
    category_list = [{'id': category.get('id'), 'name': category.get('name')}
                        for category in filtered_categories_data]
    return jsonify(category_list)


@quiz_bp.route('/subcategories/<int:category_id>', methods=['GET'])
def get_subcategories(category_id):
    """
    Returns a list of all the subcategories in the database
    under the specified category id

    """
    #subjects = Subject.query.filter_by(subcategory_id=subcategory_id).all()
    #subjects_data = [subject.serialize() for subject in subjects]
    #filtered_subjects_data = [subject_data for subject_data in subjects_data if subject_data.get('nquestions', 0) > 0]
    
    subcategories = Subcategory.query.filter_by(category_id=category_id).all()
    subcategories_data = [subcategory.serialize() for subcategory in subcategories]
    filtered_subcategories_data = [subcategory_data for subcategory_data in subcategories_data if subcategory_data.get('nquestions', 0) > 0]
    subcategory_list = [{'id': subcategory.get('id'), 'name': subcategory.get('name')}
                        for subcategory in filtered_subcategories_data]
    return jsonify(subcategory_list)


@quiz_bp.route('/subjects/<int:subcategory_id>', methods=['GET'])
def get_subjects(subcategory_id):
    """
    Returns a list of all the subjects in the database
    under the specified subcategory id

    """
    subjects = Subject.query.filter_by(subcategory_id=subcategory_id).all()
    subjects_data = [subject.serialize() for subject in subjects]
    filtered_subjects_data = [subject_data for subject_data in subjects_data if subject_data.get('nquestions', 0) > 0]
    subject_list = [{'id': subject.get('id'), 'name': subject.get('name')}
                    for subject in filtered_subjects_data]
    return jsonify(subject_list)


@quiz_bp.route('/units/<int:subject_id>', methods=['GET'])
def get_units(subject_id):
    """
    Returns a list of all the units in the database
    under the specified subject id

    """
    units = Unit.query.filter_by(subject_id=subject_id).all()
    units_data = [unit.serialize() for unit in units]
    filtered_units_data = [unit_data for unit_data in units_data if unit_data.get('nquestions', 0) > 0]
    unit_list = [{'id': unit.get('id'), 'name': unit.get('name')}
                        for unit in filtered_units_data]
    return jsonify(unit_list)

@quiz_bp.route('/tags/<int:unit_id>', methods=['GET'])
def get_tags(unit_id):
    """
    Returns a list of all the tags in the database
    under the specified unit id

    """
    
    unit = Unit.query.get(unit_id)
    tag_list = [{'id': 0, 'name': tag}
                 for tag in unit.tags]
    return jsonify(tag_list)

@quiz_bp.route('/subunits/<int:unit_id>', methods=['GET'])
def get_subunits(unit_id):
    """
    Returns a list of all the subunits in the database
    under the specified unit id

    """
    # Return unit as a subnit. This QBank does not have subunit
    # but has to be made to look so to conform with the AI categories 
    # at the frontend
    subunits = Unit.query.get(unit_id)
    subunits_list = [{'id': subunit.id, 'name': subunit.name}
                 for subunit in subunits]
    return jsonify(subunits_list)

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
    category_id = int(request.args.get('category_id', 0))
    subcategory_id = int(request.args.get('subcategory_id', 0))
    subject_id = int(request.args.get('subject_id', 0))
    unit_id = int(request.args.get('unit_id', 0))

    questions = None
    if category_id != 0:
        questions = Question.query.filter_by(category_id=category_id).all()
    elif subcategory_id != 0:
        questions = Question.query.filter_by(subcategory_id=subcategory_id).all()
    elif subject_id != 0:
        questions = Question.query.filter_by(subject_id=subject_id).all()
    elif unit_id != 0:
        questions = Question.query.filter_by(unit_id=unit_id).all()

    if questions is None:
        return jsonify({"message": "No questions found"}), 404

    random_questions = random.sample(questions, min(n, len(questions)))

    question_data_list = []
    for question in random_questions:
        question_data = {
            'id': question.id,
            'question': question.question_text,
            'option_a': question.option_a,
            'option_b': question.option_b,
            'option_c': question.option_c,
            'option_d': question.option_d,
            'option_e': question.option_e,
            'tags': question.tags,
            'answer': question.correct_options,
            'explanation': question.explanation
        }
        question_data_list.append(question_data)

    return jsonify(question_data_list)


@quiz_bp.route('/questions/level/<int:category_level>/category/<int:level_id>', methods=['GET'])
def get_quiz_questions(category_level, level_id):

    """
    Returns a speciifed number of questions that
    satisifes the paremeters. The category level
    can be 1 -> Category, 2 -> Subcategory, 3 ->
    Subject, 4 -> Unit. The actual id of the
    category will be used to retrieve the questions
    """
    
    n = int(request.args.get('n', 1))
    if category_level == 1:
        questions = Question.query.filter_by(category_id=level_id).all()
    elif category_level == 2:
        questions = Question.query.filter_by(subcategory_id=level_id).all()
    elif category_level == 3:
        questions = Question.query.filter_by(subject_id=level_id).all()
    elif category_level == 4:
        questions = Question.query.filter_by(unit_id=level_id).all()
    elif category_level == 5:
        questions = Question.query.filter_by(subunit_id=level_id).all()

    if not questions:
        return jsonify({"message": "No questions found"}), 404

    random_questions = random.sample(questions, min(n, len(questions)))

    question_data_list = []
    for question in random_questions:
        question_data = {
            'id': question.id,
            'question': question.question_text,
            'option_a': question.option_a,
            'option_b': question.option_b,
            'option_c': question.option_c,
            'option_d': question.option_d,
            'option_e': question.option_e,
            'tags': question.tags,
            'answer': "".join(question.correct_options),
            'explanation': question.explanation
        }
        question_data_list.append(question_data)

    return jsonify(question_data_list)


@quiz_bp.route('/question/<int:question_id>', methods = ['GET'])
def get_question_by_id(question_id):
    """
    """

    question = Question.query.get(question_id)
    if question:
        print(question.serialize())
        return jsonify(question.serialize())

@quiz_bp.route('/question/<int:question_id>/comments', methods=['GET'])
def get_comments(question_id):
    """
    Returns a list of all the comments
    related to the question with its id
    """

    try:
        question = Question.query.get(question_id)
        if question is None:
            return jsonify({'error': 'Question not found'}), 404

        comments = question.comments
        comments_list = []
        for comment in comments:
            comment_data = {
                "id": comment.id,
                "text": comment.text,
                "author": comment.user.username,
                "likes": comment.likes,
                "quotes": comment.quotes,
                "replies": len(comment.subcomments),
                "edited": comment.edited
            }
            comments_list.append(comment_data)

        return jsonify(comments_list), 200

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

    all_categories = Category.query.all()

    for category in all_categories:
        category.subcategories = get_subcategories(category.id)

    return jsonify([category.serialize() for category in all_categories])