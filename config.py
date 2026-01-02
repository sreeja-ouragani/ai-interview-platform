import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Mistral AI Configuration
    MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
    print(f"🔧 Config loaded MISTRAL_API_KEY: '{MISTRAL_API_KEY}' (Length: {len(MISTRAL_API_KEY) if MISTRAL_API_KEY else 0})")

    
    # Judge0 Configuration
    JUDGE0_API_KEY = os.getenv('JUDGE0_API_KEY')
    JUDGE0_API_URL = os.getenv('JUDGE0_API_URL', 'https://judge0-ce.p.rapidapi.com')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    # Server Configuration
    HOST = os.getenv('HOST', '127.0.0.1')
    PORT = int(os.getenv('PORT', 5000))
    
    # Data Storage Configuration
    DATA_DIR = 'data'
    USERS_FILE = os.path.join(DATA_DIR, 'users.json')
    INTERVIEWS_FILE = os.path.join(DATA_DIR, 'interviews.json')
    FEEDBACK_FILE = os.path.join(DATA_DIR, 'feedback.json')
    RESUMES_DIR = os.path.join(DATA_DIR, 'resumes')
    
    # Interview Configuration
    INTERVIEW_ROUNDS = ['HR', 'Technical', 'Coding', 'Managerial']
    DIFFICULTY_LEVELS = ['Easy', 'Medium', 'Hard']
    
    # Mistral Model Configuration
    MISTRAL_MODEL = 'mistral-large-latest'  # or 'mistral-medium', 'mistral-small'
    
    @staticmethod
    def init_app():
        """Initialize application directories"""
        os.makedirs(Config.DATA_DIR, exist_ok=True)
        os.makedirs(Config.RESUMES_DIR, exist_ok=True)
        
        # Create empty JSON files if they don't exist
        for file_path in [Config.USERS_FILE, Config.INTERVIEWS_FILE, Config.FEEDBACK_FILE]:
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    import json
                    json.dump({}, f)
