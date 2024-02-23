import random
from flask import Blueprint, request, jsonify
from ..models.social import Attempt, User, MockSubject
from ..models.question import Question
from ..models.categories import Category, Subcategory, Subject, Unit
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db


# Create a Blueprint for the mock exam endpoints
attempt_bp = Blueprint('attempt', __name__)

def jwt_required_for_all_routes():
    @attempt_bp.before_request
    @jwt_required()
    def before_request():
        pass

jwt_required_for_all_routes()

@attempt_bp.route('/mock', methods=['POST'])
def create_attempt():
    """
    Creates a new mock exam.
    """

    # Verify and retrieve user using passed jwt
    user_verified = get_jwt_identity()
    if user_verified is None:
        return jsonify({'message': 'Invalid user'}), 400

    current_user = User.query.filter_by(email=user_verified).first()

    # Receive passed parameters
    data = request.get_json()

    mock_subjects = data.get('mock_subjects')  # List of mock subjects
    total_duration = data.get('total_duration')  # Duration of mock exam
    date_taken = data.get('date_taken')  # Mock exam schedule
    date_object = datetime.strptime(date_taken, '%d-%m-%Y %H:%M:%S') if date_taken else datetime.now()

    if not current_user or not mock_subjects or not total_duration:
        return jsonify({'msg': 'Incomplete data. All data are required.'}), 400

    attempt = Attempt(
        user_id=current_user.id,
        duration=total_duration,
        date_taken=date_object
    )

    quiz_data = []

    for subject in mock_subjects:
        level = None
        if subject['level'] == 1:
            level = Category.query.filter_by(name=subject['name']).first()
        elif subject['level'] == 2:
            level = Subcategory.query.filter_by(name=subject['name']).first()
        elif subject['level'] == 3:
            level = Subject.query.filter_by(name=subject['name']).first()
        elif subject['level'] == 4:
            level = Unit.query.filter_by(name=subject['name']).first()

        if not level:
            return jsonify({'msg': f'Level {subject["level"]} subject not found: {subject["name"]}'}), 404

        questions = Question.query.filter_by(**{level.__class__.__name__.lower() + '_id': level.id}).all()
        quiz_questions = random.sample(questions, min(subject['num_questions'], len(questions)))

        quiz_data_ids = {
            "subject": subject['name'],
            "subjectId": level.id,
            "level": subject['level'],
            "ids": [question.id for question in quiz_questions]
        }
        quiz_data.append(quiz_data_ids)

        mock_subject = MockSubject(
            name=subject['name'],
            num_questions=min(len(questions), subject['num_questions']),
            score=0
        )
        attempt.add_mock_subject(mock_subject)

    attempt.total_possible_score = sum(mock_subject.num_questions for mock_subject in attempt.subjects_taken)

    db.session.add(attempt)
    db.session.commit()

    return jsonify({'msg': 'Mock created', 'quiz_data': quiz_data, "mock_id": attempt.id, "duration": total_duration, "question_source": "QBANK", 'questions': []}), 201

@attempt_bp.route('/ai/mock', methods=['POST'])
def create_attempt_ai():
    """
    Creates a new mock exam under ai mode.
    """

    # Verify and retrieve user using passed jwt
    user_verified = get_jwt_identity()
    if user_verified is None:
        return jsonify({'message': 'Invalid user'}), 400

    current_user = User.query.filter_by(email=user_verified).first()

    # Receive passed parameters
    data = request.get_json()

    mock_subjects = data.get('mock_subjects')  # List of mock subjects
    total_duration = data.get('total_duration')  # Duration of mock exam
    date_taken = data.get('date_taken')  # Mock exam schedule
    date_object = None

    if date_taken:
        date_object = datetime.strptime(date_taken, '%d-%m-%Y %H:%M:%S')

    current_timestamp = datetime.now()  # Date object for immediate mock exam
    total_possible_score = 0  # Initial value

    if not current_user or not mock_subjects or not total_duration:
        return jsonify({'msg': 'Incomplete data. All data are required.'}), 400

    # Create a new mock exam
    attempt = Attempt(
        user_id=current_user.id,
        duration=total_duration,
        date_taken=date_object if date_taken else current_timestamp
    )

    quiz_data = []

    # Add subjects to mock exam
    for subject in mock_subjects:
        mock_subject = MockSubject(
            name=subject['name'],
            num_questions=subject['num_questions'],
            score=0
        )
        total_possible_score += subject['num_questions']
        attempt.add_mock_subject(mock_subject)

        
    # Add total possible score to the attempt
    attempt.total_possible_score = total_possible_score

    db.session.add(attempt)
    db.session.commit()

    return jsonify({
        'msg': 'AI Mock created',
        'quiz_data': quiz_data,
        "mock_id": attempt.id,
        "duration": total_duration,
        "question_source": "QBANK"
    }), 201



@attempt_bp.route('/mock/<int:attempt_id>', methods=['PATCH'])
def edit_attempt(attempt_id):
    """
    Edits an existing mock exam.
    """
    user_verified = get_jwt_identity()
    if user_verified is None:
        return jsonify({'message': 'Invalid user'}), 400

    # Ensure that the user is retrieved using the correct attribute (e.g., email or username)
    current_user = User.query.filter_by(username=user_verified).first()

    attempt = Attempt.query.get(attempt_id)
    if attempt is None:
        return jsonify({'message': 'Invalid mock id'}), 400

    data = request.get_json()

    # Extract necessary data from the request
    mock_subjects = data.get('mock_subjects')
    total_duration = data.get('duration')
    date_taken = data.get('date_taken')

    # Validate the incoming data
    if not current_user or not mock_subjects or not total_duration or not date_taken:
        return jsonify({'message': 'Incomplete data. All information are required.'}), 400

    try:
        # Convert date_taken to a datetime object
        date_object = datetime.strptime(date_taken, '%d-%m-%Y %H:%M:%S')
    except ValueError:
        return jsonify({'message': 'Invalid date format for date_taken.'}), 400

    current_timestamp = datetime.now()
    total_possible_score = 0

    # Update the attempt details
    attempt.duration = total_duration
    attempt.date_taken = date_object if date_taken else current_timestamp
    attempt.subjects_taken = []  # Clear previous subjects
    attempt.total_score = 0

    # Add subjects to the attempt
    for subject in mock_subjects:
        mock_subject = MockSubject(
            name=subject['name'],
            num_questions=subject['num_questions'],
            score=0
        )
        total_possible_score += mock_subject.num_questions
        attempt.add_mock_subject(mock_subject)

    # Set the total possible score
    attempt.total_possible_score = total_possible_score

    # Commit changes to the database
    db.session.add(attempt)
    db.session.commit()

    return jsonify({'message': 'Mock exam edited successfully.'}), 201

@attempt_bp.route('/mocks', methods=['GET'])
def get_attempts():
    """
    Get a list of all mock exams.
    """

    # Verify and retrieve user
    user_identity = get_jwt_identity()
    if user_identity is None:
        return jsonify({'message': 'Unauthorized access'}), 401

    user = User.query.filter_by(username=user_identity).first()
    if user is None:
        return jsonify({'message': 'User not found'}), 404

    attempts = Attempt.query.filter_by(user_id=user.id).all()
    attempts_list = []

    for attempt in attempts:
        subjects = []
        for subject in attempt.subjects_taken:
            subject_data = {
                'name': subject.name,
                'num_questions': subject.num_questions,
                'score': subject.score
            }
            subjects.append(subject_data)

        attempt_data = {
            'attempt_id': attempt.id,
            'duration': attempt.duration,
            'date_taken': attempt.date_taken.strftime('%d-%m-%Y %H:%M:%S') if attempt.date_taken else None,
            'total_possible_score': attempt.total_possible_score,
            'total_score': attempt.total_score,
            'subjects_taken': subjects
        }
        attempts_list.append(attempt_data)

    return jsonify(attempts_list)


@attempt_bp.route('/mock/<int:attempt_id>', methods=['GET'])
def get_attempt(attempt_id):
    """
    Get details of a specific mock exam by ID.
    """
    # Retrieve and verify user
    user_verified = get_jwt_identity()
    if user_verified is None:
        return jsonify({'message': 'Unauthorized access'}), 401

    user = User.query.filter_by(username=user_verified).first()
    if user is None:
        return jsonify({'message': 'User not found'}), 404

    attempt = Attempt.query.filter_by(user_id=user.id, id=attempt_id).first()
    if attempt is None:
        return jsonify({'message': 'Mock exam not found.'}), 404

    subjects = []
    for subject in attempt.subjects_taken:
        subject_data = {
            'name': subject.name,
            'num_questions': subject.num_questions,
            'score': subject.score
        }
        subjects.append(subject_data)

    attempt_data = {
        'attempt_id': attempt.id,
        'duration': attempt.duration,
        'date_taken': attempt.date_taken.strftime('%d-%m-%Y %H:%M:%S') if attempt.date_taken else None,
        'total_possible_score': attempt.total_possible_score,
        'total_score': attempt.total_score,
        'subjects_taken': subjects
    }

    return jsonify(attempt_data)


@attempt_bp.route('/mock/<int:attempt_id>', methods=['DELETE'])
def delete_attempt(attempt_id):
    """
    Delete a specific mock exam by ID.
    """
    # Retrieve and verify user
    user_verified = get_jwt_identity()
    if user_verified is None:
        return jsonify({'message': 'Unauthorized access'}), 401

    user = User.query.filter_by(username=user_verified).first()
    if user is None:
        return jsonify({'message': 'User not found'}), 404

    attempt = Attempt.query.filter_by(user_id=user.id, id=attempt_id).first()
    if attempt is None:
        return jsonify({'message': 'Mock exam not found.'}), 404

    try:
        db.session.delete(attempt)
        db.session.commit()
        return jsonify({'message': 'Mock exam removed'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to delete mock exam: {str(e)}'}), 500


@attempt_bp.route('/mock/scores/<int:attempt_id>', methods=['PATCH'])
def update_scores(attempt_id):

    """
    Edit the scores of MockSubjects
    """

    # Verify and retrieve user
    user_verified = get_jwt_identity()
    if user_verified is not None:
        user = User.query.filter_by(username=user_verified).first()
    else:
        return jsonify({'error': 'Unauthorized access'}), 401

    # Extract passed data
    data = request.get_json()
    scored_mock_subjects = data.get('scored_mock_subjects')

    attempt = Attempt.query.get(attempt_id)
    if attempt is None:
        return jsonify({'error': 'Attempt not found.'}), 404

    try:
        attempt_total_score = 0

        # Update scores for each scored subject
        for scored_subject in scored_mock_subjects:
            subject_name = scored_subject.get('name')
            subject_score = scored_subject.get('score')

            # Find the subject in subjects_taken in the attempt by name
            subject = next((s for s in attempt.subjects_taken if s.name == subject_name), None)

            if subject is not None:
                # Update the subject's score
                subject.score = subject_score
                attempt_total_score += subject_score

        # Update the total score of the attempt
        attempt.total_score = attempt_total_score
        db.session.commit()

        # Return the updated attempt data
        attempt_data = {
            'attempt_id': attempt.id,
            'duration': attempt.duration,
            'date_taken': attempt.date_taken.strftime('%d-%m-%Y %H:%M:%S'),
            'total_possible_score': attempt.total_possible_score,
            'total_score': attempt.total_score,
            'subjects_taken': [{"name": subject.name, "num_questions": subject.num_questions, "score": subject.score} for subject in attempt.subjects_taken]
        }
        return jsonify(attempt_data)

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500