from flask import Blueprint, request, jsonify
from services.mcq_evaluator import MCQEvaluator
import json
import os
import random

mcq_bp = Blueprint('mcq', __name__, url_prefix='/api/mcq')

# Load MCQ questions from JSON file
def load_questions():
    questions_file = 'data/questions_mcq.json'
    if os.path.exists(questions_file):
        with open(questions_file, 'r') as f:
            return json.load(f)
    return []

@mcq_bp.route('/questions', methods=['GET'])
def get_questions():
    """Get MCQ questions based on difficulty and category"""
    difficulty = request.args.get('difficulty', 'Medium')
    category = request.args.get('category', 'all')
    count = int(request.args.get('count', 10))
    
    all_questions = load_questions()
    
    # Filter by difficulty
    if difficulty != 'all':
        filtered = [q for q in all_questions if q.get('difficulty') == difficulty]
    else:
        filtered = all_questions
    
    # Filter by category if specified
    if category != 'all':
        filtered = [q for q in filtered if q.get('category') == category]
    
    # Limit count and randomize
    try:
        if len(filtered) < count:
            selected = filtered
        else:
            selected = random.sample(filtered, count)
    except Exception:
        selected = filtered[:count]
    
    # Remove correct answers before sending
    questions_for_user = []
    for q in selected:
        q_copy = q.copy()
        # Keep correct_answer on server side only
        questions_for_user.append({
            'id': q_copy['id'],
            'question': q_copy['question'],
            'options': q_copy['options'],
            'category': q_copy.get('category', ''),
            'difficulty': q_copy.get('difficulty', '')
        })
    
    return jsonify({
        'questions': questions_for_user,
        'total': len(selected)
    }), 200

@mcq_bp.route('/evaluate', methods=['POST'])
def evaluate_answers():
    """Evaluate MCQ answers"""
    data = request.json
    user_answers = data.get('answers', {})  # {question_id: answer}
    
    all_questions = load_questions()
    
    # Get questions that were answered
    answered_questions = [q for q in all_questions if q['id'] in user_answers]
    
    # Evaluate
    result = MCQEvaluator.evaluate_mcq_set(answered_questions, user_answers)
    
    # Get performance analysis
    analysis = MCQEvaluator.get_performance_analysis(result)
    
    return jsonify({
        'evaluation': result,
        'analysis': analysis
    }), 200
