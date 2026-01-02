from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
from services.resume_parser import ResumeParser
from services.mistral_service import MistralService
from utils.storage import JSONStorage
from config import Config

resume_bp = Blueprint('resume', __name__, url_prefix='/api/resume')

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@resume_bp.route('/upload/<username>', methods=['POST'])
def upload_resume(username):
    """Upload and analyze resume"""
    user = JSONStorage.get_user(username, Config.USERS_FILE)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: PDF, DOCX, TXT'}), 400
    
    # Save file
    filename = secure_filename(f"{username}_{file.filename}")
    filepath = os.path.join(Config.RESUMES_DIR, filename)
    file.save(filepath)
    
    # Parse resume
    resume_text = ResumeParser.parse_resume(filepath)
    
    if not resume_text:
        return jsonify({'error': 'Failed to parse resume'}), 500
    
    # Extract skills using Mistral AI
    mistral = MistralService()
    skills_data = mistral.extract_skills_from_resume(resume_text)
    
    # Update user skills
    user['skills'] = skills_data
    user['resume_filename'] = filename
    user['resume_text'] = resume_text[:500]  # Store first 500 chars
    
    JSONStorage.save_user(username, user, Config.USERS_FILE)
    
    return jsonify({
        'message': 'Resume uploaded and analyzed successfully',
        'skills': skills_data,
        'filename': filename
    }), 200

@resume_bp.route('/match/<username>', methods=['POST'])
def match_job(username):
    """Match resume to job description"""
    user = JSONStorage.get_user(username, Config.USERS_FILE)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if 'skills' not in user or not user['skills']:
        return jsonify({'error': 'Please upload resume first'}), 400
    
    data = request.json
    job_description = data.get('job_description', '')
    
    if not job_description:
        return jsonify({'error': 'Job description is required'}), 400
    
    # Match using Mistral AI
    mistral = MistralService()
    match_result = mistral.match_resume_to_job(user['skills'], job_description)
    
    # Save match result
    user['last_job_match'] = match_result
    JSONStorage.save_user(username, user, Config.USERS_FILE)
    
    return jsonify({
        'message': 'Job matching completed',
        'match_result': match_result
    }), 200
