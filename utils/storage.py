import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

class JSONStorage:
    """Simple JSON file-based storage system"""
    
    @staticmethod
    def read_json(file_path: str) -> Dict:
        """Read data from JSON file"""
        if not os.path.exists(file_path):
            return {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    
    @staticmethod
    def write_json(file_path: str, data: Dict) -> bool:
        """Write data to JSON file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error writing to {file_path}: {e}")
            return False
    
    @staticmethod
    def get_user(username: str, users_file: str) -> Optional[Dict]:
        """Get user data by username"""
        users = JSONStorage.read_json(users_file)
        return users.get(username)
    
    @staticmethod
    def save_user(username: str, user_data: Dict, users_file: str) -> bool:
        """Save or update user data"""
        users = JSONStorage.read_json(users_file)
        
        if username not in users:
            user_data['created_at'] = datetime.now().isoformat()
        
        user_data['updated_at'] = datetime.now().isoformat()
        users[username] = user_data
        
        return JSONStorage.write_json(users_file, users)
    
    @staticmethod
    def get_user_interviews(username: str, interviews_file: str) -> List[Dict]:
        """Get all interviews for a user"""
        interviews = JSONStorage.read_json(interviews_file)
        return interviews.get(username, [])
    
    @staticmethod
    def save_interview(username: str, interview_data: Dict, interviews_file: str) -> bool:
        """Save interview data for a user"""
        interviews = JSONStorage.read_json(interviews_file)
        
        if username not in interviews:
            interviews[username] = []
        
        interview_data['timestamp'] = datetime.now().isoformat()
        interviews[username].append(interview_data)
        
        return JSONStorage.write_json(interviews_file, interviews)
    
    @staticmethod
    def get_user_feedback(username: str, feedback_file: str) -> List[Dict]:
        """Get all feedback for a user"""
        feedback = JSONStorage.read_json(feedback_file)
        return feedback.get(username, [])
    
    @staticmethod
    def save_feedback(username: str, feedback_data: Dict, feedback_file: str) -> bool:
        """Save feedback data for a user"""
        feedback = JSONStorage.read_json(feedback_file)
        
        if username not in feedback:
            feedback[username] = []
        
        feedback_data['timestamp'] = datetime.now().isoformat()
        feedback[username].append(feedback_data)
        
        return JSONStorage.write_json(feedback_file, feedback)
    
    @staticmethod
    def update_user_skills(username: str, skills_data: Dict, users_file: str) -> bool:
        """Update user's skill data"""
        users = JSONStorage.read_json(users_file)
        
        if username not in users:
            return False
        
        users[username]['skills'] = skills_data
        users[username]['updated_at'] = datetime.now().isoformat()
        
        return JSONStorage.write_json(users_file, users)
