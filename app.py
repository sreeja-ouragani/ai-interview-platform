from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
import os
from utils.storage import JSONStorage

# Import routes
from routes.user_routes import user_bp
from routes.resume_routes import resume_bp
from routes.interview_routes import interview_bp
from routes.mcq_routes import mcq_bp
from routes.coding_routes import coding_bp
from routes.recruiter_routes import recruiter_bp

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS for frontend
    CORS(app)
    
    # Initialize app directories
    Config.init_app()
    
    # Register blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(interview_bp)
    app.register_blueprint(mcq_bp)
    app.register_blueprint(coding_bp)
    app.register_blueprint(recruiter_bp)
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'AI Interview Platform API is running'
        }), 200
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def root():
        return jsonify({
            'message': 'Welcome to AI Interview Preparation Platform API',
            'version': '1.0.0',
            'endpoints': {
                'user': '/api/user',
                'resume': '/api/resume',
                'interview': '/api/interview',
                'mcq': '/api/mcq',
                'coding': '/api/coding'
            }
        }), 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    print("=" * 60)
    print("🚀 AI Interview Preparation Platform")
    print("=" * 60)
    print(f"Server running on http://{Config.HOST}:{Config.PORT}")
    print(f"API Documentation: http://{Config.HOST}:{Config.PORT}/")
    print("=" * 60)
    
    # Check if Mistral API key is configured
    if not Config.MISTRAL_API_KEY:
        print("⚠️  WARNING: MISTRAL_API_KEY not configured!")
        print("   Please add your Mistral API key to .env file")
        print("=" * 60)
    
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
