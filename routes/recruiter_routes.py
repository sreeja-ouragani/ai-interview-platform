from flask import Blueprint, request, jsonify
from utils.storage import JSONStorage
from services.mistral_service import MistralService
from config import Config
import uuid

recruiter_bp = Blueprint('recruiter', __name__, url_prefix='/api/recruiter')

@recruiter_bp.route('/register', methods=['POST'])
def register_recruiter():
    """Register recruiter/institute account"""
    data = request.json
    company_name = data.get('company_name', '').strip()
    email = data.get('email', '').strip()
    
    if not company_name or not email:
        return jsonify({'error': 'Company name and email are required'}), 400
    
    # Use company_name as unique identifier
    recruiter_data = {
        'company_name': company_name,
        'email': email,
        'contact_person': data.get('contact_person', ''),
        'phone': data.get('phone', ''),
        'subscription_tier': data.get('subscription_tier', 'Free'),
        'batches': []
    }
    
    # Save to recruiters.json
    recruiters_file = Config.DATA_DIR + '/recruiters.json'
    recruiters = JSONStorage.read_json(recruiters_file)
    recruiters[company_name] = recruiter_data
    JSONStorage.write_json(recruiters_file, recruiters)
    
    return jsonify({
        'message': 'Recruiter registered successfully',
        'recruiter': recruiter_data
    }), 201

@recruiter_bp.route('/batch/create', methods=['POST'])
def create_batch():
    """Create interview batch"""
    data = request.json
    company_name = data.get('company_name')
    batch_name = data.get('batch_name')
    
    if not company_name or not batch_name:
        return jsonify({'error': 'Company name and batch name are required'}), 400
    
    recruiters_file = Config.DATA_DIR + '/recruiters.json'
    recruiters = JSONStorage.read_json(recruiters_file)
    
    if company_name not in recruiters:
        return jsonify({'error': 'Recruiter not found'}), 404
    
    batch = {
        'batch_id': str(uuid.uuid4()),
        'batch_name': batch_name,
        'job_description': data.get('job_description', ''),
        'required_skills': data.get('required_skills', []),
        'start_date': data.get('start_date', ''),
        'end_date': data.get('end_date', ''),
        'shortlist_threshold': data.get('shortlist_threshold', 70),
        'candidates': [],
        'status': 'Active'
    }
    
    recruiters[company_name]['batches'].append(batch)
    JSONStorage.write_json(recruiters_file, recruiters)
    
    return jsonify({
        'message': 'Batch created successfully',
        'batch': batch
    }), 201

@recruiter_bp.route('/batch/<batch_id>/candidates', methods=['GET'])
def get_batch_candidates(batch_id):
    """Get all candidates in a batch"""
    company_name = request.args.get('company_name')
    
    if not company_name:
        return jsonify({'error': 'Company name is required'}), 400
    
    recruiters_file = Config.DATA_DIR + '/recruiters.json'
    recruiters = JSONStorage.read_json(recruiters_file)
    
    if company_name not in recruiters:
        return jsonify({'error': 'Recruiter not found'}), 404
    
    # Find batch
    batch = None
    for b in recruiters[company_name]['batches']:
        if b['batch_id'] == batch_id:
            batch = b
            break
    
    if not batch:
        return jsonify({'error': 'Batch not found'}), 404
    
    # Get interview data for candidates
    interviews_file = Config.INTERVIEWS_FILE
    all_interviews = JSONStorage.read_json(interviews_file)
    
    candidates_data = []
    for candidate in batch['candidates']:
        username = candidate['username']
        interviews = all_interviews.get(username, [])
        
        # Calculate average score
        total_score = sum([i.get('overall_score', 0) for i in interviews])
        avg_score = total_score / len(interviews) if interviews else 0
        
        candidates_data.append({
            'username': username,
            'interview_count': len(interviews),
            'average_score': round(avg_score, 2),
            'status': candidate.get('status', 'Pending')
        })
    
    return jsonify({
        'batch': batch,
        'candidates': candidates_data
    }), 200

@recruiter_bp.route('/batch/<batch_id>/add-candidate', methods=['POST'])
def add_candidate_to_batch(batch_id):
    """Add candidate to batch"""
    data = request.json
    company_name = data.get('company_name')
    username = data.get('username')
    
    if not company_name or not username:
        return jsonify({'error': 'Company name and username are required'}), 400
    
    recruiters_file = Config.DATA_DIR + '/recruiters.json'
    recruiters = JSONStorage.read_json(recruiters_file)
    
    if company_name not in recruiters:
        return jsonify({'error': 'Recruiter not found'}), 404
    
    # Find and update batch
    batch_found = False
    for batch in recruiters[company_name]['batches']:
        if batch['batch_id'] == batch_id:
            batch['candidates'].append({
                'username': username,
                'added_date': data.get('added_date', ''),
                'status': 'Pending'
            })
            batch_found = True
            break
    
    if not batch_found:
        return jsonify({'error': 'Batch not found'}), 404
    
    JSONStorage.write_json(recruiters_file, recruiters)
    
    return jsonify({'message': 'Candidate added to batch'}), 200

@recruiter_bp.route('/batch/<batch_id>/auto-shortlist', methods=['POST'])
def auto_shortlist(batch_id):
    """Auto-shortlist candidates based on threshold"""
    data = request.json
    company_name = data.get('company_name')
    
    if not company_name:
        return jsonify({'error': 'Company name is required'}), 400
    
    recruiters_file = Config.DATA_DIR + '/recruiters.json'
    recruiters = JSONStorage.read_json(recruiters_file)
    
    if company_name not in recruiters:
        return jsonify({'error': 'Recruiter not found'}), 404
    
    # Find batch
    batch = None
    for b in recruiters[company_name]['batches']:
        if b['batch_id'] == batch_id:
            batch = b
            break
    
    if not batch:
        return jsonify({'error': 'Batch not found'}), 404
    
    threshold = batch.get('shortlist_threshold', 70)
    
    # Get interview scores
    interviews_file = Config.INTERVIEWS_FILE
    all_interviews = JSONStorage.read_json(interviews_file)
    
    shortlisted = []
    rejected = []
    
    for candidate in batch['candidates']:
        username = candidate['username']
        interviews = all_interviews.get(username, [])
        
        if interviews:
            # Get latest interview score
            latest_score = interviews[-1].get('overall_score', 0)
            
            if latest_score >= threshold:
                candidate['status'] = 'Shortlisted'
                shortlisted.append(username)
            else:
                candidate['status'] = 'Rejected'
                rejected.append(username)
        else:
            candidate['status'] = 'Pending'
    
    JSONStorage.write_json(recruiters_file, recruiters)
    
    return jsonify({
        'message': 'Auto-shortlisting completed',
        'threshold': threshold,
        'shortlisted': shortlisted,
        'rejected': rejected
    }), 200

@recruiter_bp.route('/candidate/<username>/report', methods=['GET'])
def get_candidate_report(username):
    """Get detailed skill report for candidate"""
    user = JSONStorage.get_user(username, Config.USERS_FILE)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get interviews
    interviews = JSONStorage.get_user_interviews(username, Config.INTERVIEWS_FILE)
    
    # Get feedback
    feedback = JSONStorage.get_user_feedback(username, Config.FEEDBACK_FILE)
    
    # Calculate stats
    total_interviews = len(interviews)
    avg_score = sum([i.get('overall_score', 0) for i in interviews]) / total_interviews if total_interviews > 0 else 0
    
    report = {
        'username': username,
        'profile': user,
        'statistics': {
            'total_interviews': total_interviews,
            'average_score': round(avg_score, 2),
            'skills': user.get('skills', {}),
            'experience_level': user.get('experience_level', 'Not specified'),
            'target_role': user.get('target_role', 'Not specified')
        },
        'interview_history': interviews,
        'latest_feedback': feedback[-1] if feedback else None
    }
    
    return jsonify(report), 200

@recruiter_bp.route('/dashboard/<company_name>', methods=['GET'])
def get_dashboard(company_name):
    """Get recruiter dashboard data"""
    recruiters_file = Config.DATA_DIR + '/recruiters.json'
    recruiters = JSONStorage.read_json(recruiters_file)
    
    if company_name not in recruiters:
        return jsonify({'error': 'Recruiter not found'}), 404
    
    recruiter = recruiters[company_name]
    
    # Calculate stats
    total_batches = len(recruiter['batches'])
    total_candidates = sum([len(b['candidates']) for b in recruiter['batches']])
    
    active_batches = [b for b in recruiter['batches'] if b['status'] == 'Active']
    
    dashboard = {
        'company_name': company_name,
        'total_batches': total_batches,
        'active_batches': len(active_batches),
        'total_candidates': total_candidates,
        'batches': recruiter['batches'],
        'subscription_tier': recruiter.get('subscription_tier', 'Free')
    }
    
    return jsonify(dashboard), 200
