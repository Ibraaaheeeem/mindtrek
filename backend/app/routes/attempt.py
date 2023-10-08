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
    total_duration = data.get('total_duration') # Duration of mock exam
    date_taken = data.get('date_taken') # Mock exam schedule
    date_object = None
    if date_taken:
        date_object = datetime.strptime(date_taken, '%d-%m-%Y %H:%M:%S')
    current_timestamp = datetime.now() # date object for immediate mock exam
    total_possible_score = 0 # Initial value

    if not current_user or not mock_subjects or not total_duration:
        print(current_user)
        print(mock_subjects)
        return jsonify({'msg': 'Incomplete data. All data are required.'}), 400
    
    # Create a new mock exam
    attempt = Attempt(
        user_id = current_user.id,
        duration = total_duration,
        date_taken = date_object if date_taken else current_timestamp
    )

    
    quiz_data = []
    # Add subjetcs to mock exam
    for subject in mock_subjects:
        
        if subject['level'] == 1:
            level = Category.query.filter_by(name=subject['name']).first()
            print(level.name)
            questions = Question.query.filter_by(category_id=level.id).all()
            quiz_questions = random.sample(questions, min(subject['num_questions'], len(questions)))
            quiz_data_ids = {"subject": subject['name'], "subjectId": level.id, "level": subject['level'], "ids": [question.id for question in quiz_questions]}
            quiz_data.append(quiz_data_ids)

        elif subject['level'] == 2:
            level = Subcategory.query.filter_by(name=subject['name']).first()
            questions = Question.query.filter_by(subcategory_id=level.id).all()
            quiz_questions = random.sample(questions, min(subject['num_questions'], len(questions)))
            print(len(quiz_questions))
            quiz_data_ids = {"subject": subject['name'], "subjectId": level.id, "level": subject['level'], "ids": [question.id for question in quiz_questions]}
            quiz_data.append(quiz_data_ids)

        elif subject['level'] == 3:
            level = Subject.query.filter_by(name=subject['name']).first()
            questions = Question.query.filter_by(subject_id=level.id).all()
            quiz_questions = random.sample(questions, min(subject['num_questions'], len(questions)))
            print(len(quiz_questions))
            quiz_data_ids = {"subject": subject['name'], "subjectId": level.id, "level": subject['level'], "ids": [question.id for question in quiz_questions]}
            quiz_data.append(quiz_data_ids)

        elif subject['level'] == 4:
            level = Unit.query.filter_by(name=subject['name']).first()
            questions = Question.query.filter_by(unit_id=level.id).all()
            quiz_questions = random.sample(questions, min(subject['num_questions'], len(questions)))
            print(len(quiz_questions))
            quiz_data_ids = {"subject": subject['name'], "subjectId": subject['id'], "level": subject['level'],"ids": [question.id for question in quiz_questions]}
            quiz_data.append(quiz_data_ids)

        mock_subject = MockSubject(
            name = subject['name'],
            num_questions = min(len(questions), subject['num_questions']),
            score = 0
        )
        total_possible_score += mock_subject.num_questions
        attempt.add_mock_subject(mock_subject)
    
    # Add sum total of questions as highest possible score
    attempt.total_possible_score = total_possible_score
    
    db.session.add(attempt)
    db.session.commit()


    return jsonify({'msg': 'Mock created', 'quiz_data': quiz_data, "mock_id": attempt.id, "duration": total_duration}), 201

@attempt_bp.route('/mock/<int:attempt_id>', methods=['PATCH'])
def edit_attempt(attempt_id):
    """
    Edits an existing mock exam.
    """
    user_verified = get_jwt_identity()
    if user_verified is None:
        return jsonify({'message': 'Invalid user'}), 400
    current_user = User.query.filter_by(username=user_verified).first()

    attempt = Attempt.query.get(attempt_id)
    if attempt is None:
        return jsonify({'message': 'Invalid mock id'}), 400
    
    # Retrieved passed data from frontend
    data = request.get_json()
    
    mock_subjects = data.get('mock_subjects')  # List of mock subjects
    total_duration = data.get('duration')
    date_taken = data.get('date_taken')
    date_object = datetime.strptime(date_taken, '%d-%m-%Y %H:%M:%S')
    current_timestamp = datetime.now()
    total_possible_score = 0
    
    if not current_user or not mock_subjects or not total_duration or not date_taken:
        return jsonify({'message': 'Incomplete data. All information are required.'}), 400

    # Edit values for mock exam
    attempt.duration = total_duration
    attempt.date_taken = date_object if date_taken else current_timestamp
    attempt.subjects_taken = [] # Initialise mock subjects
    attempt.total_score = 0

    # Add subjects to mock
    for subject in mock_subjects:
        mock_subject = MockSubject(
            name = subject['name'],
            num_questions = subject['num_questions'],
            score = 0
        )
        total_possible_score += mock_subject.num_questions
        attempt.add_mock_subject(mock_subject)
    
    # Set addition of num_questions as new highest possible score
    attempt.total_possible_score = total_possible_score
    
    db.session.add(attempt)
    db.session.commit()
    return jsonify({'message': 'Mock exam edited successfully.'}), 201

@attempt_bp.route('/mocks', methods=['GET'])
def get_attempts():
    """
    Get a list of all mock exams.
    """

    # Verify and retrieve user
    user_verified = get_jwt_identity()
    if user_verified is not None:
        user = User.query.filter_by(username=user_verified).first()

    # Retrieve user's attempts
    attempts = Attempt.query.filter_by(user_id=user.id).all()
    attempts_list = []
        
    for attempt in attempts:
        subjects = [{"name":subject.name, "num_questions": subject.num_questions, "score": subject.score} for subject in attempt.subjects_taken]
        
        # Create a dictionary with attempt details and associated subjects
        attempt_data = {
            'attempt_id': attempt.id,
            'duration': attempt.duration,
            'date_taken': attempt.date_taken.strftime('%d-%m-%Y %H:%M:%S'),
            'total_possible_score': attempt.total_possible_score,
            'total_score': attempt.total_score,
            'subjects_taken': subjects
        }
        
        # Add attempt to list and return
        attempts_list.append(attempt_data)
    return jsonify(attempts_list)

@attempt_bp.route('/mock/<int:attempt_id>', methods=['GET'])
def get_attempt(attempt_id):
    """
    Get details of a specific mock exam by ID.
    """
    # Retrieve and verify user
    user_verified = get_jwt_identity()
    if user_verified is not None:
        user = User.query.filter_by(username=user_verified).first()
    attempts = Attempt.query.filter_by(user_id=user.id).all()

    # Search for the attempt with the specified ID in attempts list of user
    # and return
    for attempt in attempts:
        if attempt.id == attempt_id:
            subjects = [{"name":subject.name, "num_questions": subject.num_questions, "score": subject.score} for subject in attempt.subjects_taken]
            attempt_data = {
                'attempt_id': attempt.id,
                'duration': attempt.duration,
                'date_taken': attempt.date_taken.strftime('%d-%m-%Y %H:%M:%S'),
                'total_possible_score': attempt.total_possible_score,
                'total_score': attempt.total_score,
                'subjects_taken': subjects
            }
            return jsonify(attempt_data)

    # If the mock exam with the given ID is not found, return a 404 response
    return jsonify({'message': 'Mock exam not found.'}), 404

@attempt_bp.route('/mock/<int:attempt_id>', methods=['DELETE'])
def delete_attempt(attempt_id):
    """
    Delete a specific mock exam by ID.
    """
    # Retrieve and verify user
    user_verified = get_jwt_identity()
    if user_verified is not None:
        user = User.query.filter_by(username=user_verified).first()
    
    attempts = Attempt.query.filter_by(user_id=user.id).all()

    # Search for the attempt with the specified ID in the attempts list
    # and return
    for attempt in attempts:
        if attempt.id == attempt_id:
            db.session.delete(attempt)
            db.session.commit()
            return jsonify({'message': 'Mock exam removed'})

    # If the mock exam with the given ID is not found, return a 404 response
    return jsonify({'message': 'Mock exam not found.'}), 404

@attempt_bp.route('/mock/scores/<int:attempt_id>', methods=['PATCH'])
def update_scores(attempt_id):

    """
    Edit the scores of MockSubjects
    """

    # Verify and retrieve user
    user_verified = get_jwt_identity()
    if user_verified is not None:
        user = User.query.filter_by(username=user_verified).first()
    
    # Extract passed data
    data = request.get_json()
    scored_mock_subjects = data.get('scored_mock_subjects')
        
    attempt = Attempt.query.get(attempt_id)
    if attempt is None:
        return jsonify({'error': 'Attempt not found.'}), 404


    try:
        attempt_total_score = 0 # initial value
        
        for scored_subject in scored_mock_subjects:
            subject_name = scored_subject.get('name')
            subject_score = scored_subject.get('score')
            
            # Find the subject in subjects_taken in the attempt by name
            subject = next((s for s in attempt.subjects_taken if s.name == subject_name), None)

            if subject is not None:
                # Update the subject's score
                subject.score = subject_score
                attempt_total_score += subject_score
        attempt.total_score = attempt_total_score
        db.session.commit()

        # Find and return the updated attempt
        updated_attempt = Attempt.query.get(attempt_id)
        attempt_data = {
                'attempt_id': updated_attempt.id,
                'duration': updated_attempt.duration,
                'date_taken': updated_attempt.date_taken.strftime('%d-%m-%Y %H:%M:%S'),
                'total_possible_score': attempt.total_possible_score,
                'total_score': attempt.total_score,
                'subjects_taken':[{"name": subject.name, "num_questions": subject.num_questions, "score": subject.score} for subject in updated_attempt.subjects_taken]
            }
        return jsonify(attempt_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500