from flask import Blueprint, request, jsonify, g
from ..models.social import User, Comment, Subcomment
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db

comment_bp = Blueprint('discussions', __name__)

def jwt_required_for_all_routes():
    @comment_bp.before_request
    @jwt_required()
    def before_request():
        username = get_jwt_identity()
        if username is None:
            return jsonify({'error': 'Missing or invalid username'}), 401

        current_user = User.query.filter_by(username=username).first()
        g.user = current_user

jwt_required_for_all_routes()

@comment_bp.route('/comments', methods=['POST'])
def create_comment():
    try:
        data = request.get_json()
        text = data.get('text')
        timestamp = data.get('timestamp')
        date_object = datetime.strptime(timestamp, '%d-%m-%Y %H:%M:%S') if timestamp else datetime.now()

        comment = Comment(
            text=text,
            question_id=data.get('question_id'),
            user_id=g.user.id,
            timestamp=date_object
        )
        db.session.add(comment)
        db.session.commit()
        return jsonify({'message': 'Comment created successfully', 'comment_id': comment.id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@comment_bp.route('/comment/<int:comment_id>', methods=['PATCH'])
def edit_comment(comment_id):
    try:
        data = request.get_json()
        text = data.get('text')
        timestamp = data.get('timestamp')
        date_object = datetime.strptime(timestamp, '%d-%m-%Y %H:%M:%S') if timestamp else datetime.now()

        comment = Comment.query.get(comment_id)
        comment.text = text
        comment.timestamp = date_object
        db.session.commit()
        return jsonify({'message': 'Comment edited successfully', 'comment_id': comment_id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@comment_bp.route('/comment/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    try:
        comment = Comment.query.get(comment_id)
        db.session.delete(comment)
        db.session.commit()
        return jsonify({'message': 'Comment deleted successfully', 'comment_id': comment_id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@comment_bp.route('/subcomments', methods=['POST'])
def create_subcomment():
    try:
        data = request.get_json()
        text = data.get('text')
        comment_id = data.get('comment_id')
        timestamp = data.get('timestamp')
        date_object = datetime.strptime(timestamp, '%d-%m-%Y %H:%M:%S') if timestamp else datetime.now()

        comment = Comment.query.get(comment_id)
        if comment is None:
            return jsonify({'error': 'Parent comment does not exist'}), 404

        subcomment = Subcomment(
            text=text,
            comment_id=comment.id,
            user_id=g.user.id,
            timestamp=date_object
        )
        db.session.add(subcomment)
        db.session.commit()
        return jsonify({'message': 'Subcomment created successfully', 'subcomment_id': subcomment.id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@comment_bp.route('/subcomment/<int:subcomment_id>', methods=['PATCH'])
def edit_subcomment(subcomment_id):
    try:
        data = request.get_json()
        text = data.get('text')
        timestamp = data.get('timestamp')
        date_object = datetime.strptime(timestamp, '%d-%m-%Y %H:%M:%S') if timestamp else datetime.now()

        subcomment = Subcomment.query.get(subcomment_id)
        if subcomment is None:
            return jsonify({'error': 'Subcomment does not exist'}), 404

        subcomment.text = text
        subcomment.timestamp = date_object
        db.session.commit()
        return jsonify({'message': 'Subcomment edited successfully', 'subcomment_id': subcomment.id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@comment_bp.route('/subcomment/<int:subcomment_id>', methods=['DELETE'])
def delete_subcomment(subcomment_id):
    try:
        subcomment = Subcomment.query.get(subcomment_id)
        db.session.delete(subcomment)
        db.session.commit()
        return jsonify({'message': 'Subcomment deleted successfully', 'comment_id': subcomment_id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
