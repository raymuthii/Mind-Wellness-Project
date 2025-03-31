# app/routes/story.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.SuccessStory import Story
from schemas.story import StorySchema
from app import db

story_bp = Blueprint('story', __name__)
story_schema = StorySchema()
stories_schema = StorySchema(many=True)

@story_bp.route('/', methods=['GET'])
def get_stories():
    """Get all published stories"""
    try:
        stories = Story.query.filter_by(
            status='published'
        ).order_by(Story.created_at.desc()).all()
        return jsonify(stories_schema.dump(stories)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@story_bp.route('/<int:id>', methods=['GET'])
def get_story(id):
    """Get a specific story"""
    try:
        story = Story.query.get_or_404(id)
        story.increment_view()  # Increment view count
        db.session.commit()
        return jsonify(story_schema.dump(story)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@story_bp.route('/', methods=['POST'])
@jwt_required()
def create_story():
    """Create a new story"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        # Add author_id to data
        data['author_id'] = user_id
        
        # Validate and deserialize input
        story = story_schema.load(data)
        db.session.add(story)
        db.session.commit()
        
        return jsonify({
            'message': 'Story created successfully',
            'story': story_schema.dump(story)
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@story_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_story(id):
    """Update a story"""
    try:
        story = Story.query.get_or_404(id)
        user_id = get_jwt_identity()
        
        # Check if user is the author
        if story.author_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
            
        data = request.get_json()
        
        # Update story fields
        for key, value in data.items():
            setattr(story, key, value)
            
        db.session.commit()
        return jsonify({
            'message': 'Story updated successfully',
            'story': story_schema.dump(story)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@story_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_story(id):
    """Delete a story"""
    try:
        story = Story.query.get_or_404(id)
        user_id = get_jwt_identity()
        
        # Check if user is the author
        if story.author_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
            
        db.session.delete(story)
        db.session.commit()
        return jsonify({'message': 'Story deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@story_bp.route('/charity/<int:charity_id>', methods=['GET'])
def get_charity_stories(charity_id):
    """Get all stories for a specific charity"""
    try:
        stories = Story.query.filter_by(
            charity_id=charity_id,
            status='published'
        ).order_by(Story.created_at.desc()).all()
        return jsonify(stories_schema.dump(stories)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@story_bp.route('/<int:id>/like', methods=['POST'])
@jwt_required()
def like_story(id):
    """Like/unlike a story"""
    try:
        story = Story.query.get_or_404(id)
        story.increment_likes()
        db.session.commit()
        return jsonify({
            'message': 'Story liked successfully',
            'likes': story.likes
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@story_bp.route('/<int:id>/share', methods=['POST'])
@jwt_required()
def share_story(id):
    """Record a story share"""
    try:
        story = Story.query.get_or_404(id)
        story.increment_shares()
        db.session.commit()
        return jsonify({
            'message': 'Story share recorded successfully',
            'shares': story.shares
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@story_bp.route('/featured', methods=['GET'])
def get_featured_stories():
    """Get featured stories"""
    try:
        stories = Story.query.filter_by(
            featured=True,
            status='published'
        ).order_by(Story.created_at.desc()).all()
        return jsonify(stories_schema.dump(stories)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
