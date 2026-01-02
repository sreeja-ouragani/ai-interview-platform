from flask import Blueprint, request, jsonify
from services.code_executor import CodeExecutor
from services.plagiarism_detector import PlagiarismDetector
import json
import os

coding_bp = Blueprint('coding', __name__, url_prefix='/api/coding')

# Load coding questions
def load_coding_questions():
    questions_file = 'data/questions_coding.json'
    if os.path.exists(questions_file):
        with open(questions_file, 'r') as f:
            return json.load(f)
    return []

@coding_bp.route('/problems', methods=['GET'])
def get_problems():
    """Get coding problems"""
    difficulty = request.args.get('difficulty', 'Medium')
    category = request.args.get('category', 'all')
    
    all_problems = load_coding_questions()
    
    # Filter
    filtered = [p for p in all_problems if p.get('difficulty') == difficulty]
    
    # Shuffle filtered list to randomize order
    import random
    random.shuffle(filtered)
    
    if category != 'all':
        filtered = [p for p in filtered if p.get('category') == category]
    
    # Remove hidden test cases
    problems_for_user = []
    for p in filtered:
        p_copy = p.copy()
        # Only show non-hidden test cases
        p_copy['test_cases'] = [tc for tc in p_copy.get('test_cases', []) if not tc.get('is_hidden', False)]
        problems_for_user.append(p_copy)
    
    return jsonify({
        'problems': problems_for_user,
        'total': len(problems_for_user)
    }), 200

@coding_bp.route('/execute', methods=['POST'])
def execute_code():
    """Execute code with test cases"""
    data = request.json
    code = data.get('code', '')
    language = data.get('language', 'python') or 'python'
    problem_id = data.get('problem_id')
    
    if not code:
        return jsonify({'error': 'Code is required'}), 400
    
    # Get problem with all test cases (including hidden)
    all_problems = load_coding_questions()
    problem = next((p for p in all_problems if p['id'] == problem_id), None)
    
    if not problem:
        return jsonify({'error': 'Problem not found'}), 404
    
    # Execute code
    executor = CodeExecutor()
    result = executor.execute_code(code, language, problem.get('test_cases', []))
    
    return jsonify({
        'result': result,
        'problem_title': problem.get('title', '')
    }), 200

@coding_bp.route('/submit', methods=['POST'])
def submit_solution():
    """Submit final solution with plagiarism check"""
    submissions_file = 'data/submissions.json'
    data = request.json
    username = data.get('username')
    problem_id = data.get('problem_id')
    code = data.get('code')
    language = data.get('language', 'python') or 'python'
    
    # Execute with all test cases
    all_problems = load_coding_questions()
    problem = next((p for p in all_problems if p['id'] == problem_id), None)
    
    if not problem:
        return jsonify({'error': 'Problem not found'}), 404
    
    executor = CodeExecutor()
    result = executor.execute_code(code, language, problem.get('test_cases', []))
    
    # Check for plagiarism using AI (Mistral)
    from services.mistral_service import MistralService
    mistral = MistralService()
    
    print("🔍 Running AI plagiarism detection...")
    plagiarism_result = mistral.detect_code_plagiarism(submitted_code=code)
    
    # Save submission
    submission = {
        'username': username,
        'problem_id': problem_id,
        'code': code,
        'language': language,
        'result': result,
        'plagiarism_check': plagiarism_result
    }
    
    # Store submission
    if os.path.exists(submissions_file):
        with open(submissions_file, 'r') as f:
            try:
                all_submissions = json.load(f)
            except:
                all_submissions = {}
    else:
        all_submissions = {}
    
    if username not in all_submissions:
        all_submissions[username] = []
    
    all_submissions[username].append(submission)
    
    with open(submissions_file, 'w') as f:
        json.dump(all_submissions, f, indent=2)
    
    return jsonify({
        'message': 'Solution submitted',
        'result': result,
        'plagiarism_check': plagiarism_result
    }), 200
