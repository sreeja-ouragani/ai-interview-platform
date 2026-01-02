# AI Interview Preparation Platform

A comprehensive AI-powered interview preparation platform built with Python Flask and Mistral AI.

## Features

### ✅ AI-Powered Features (Using Mistral AI)
1. **Resume Analysis** - Extract skills from resume automatically
2. **Job Matching** - Match resume to job descriptions with gap analysis
3. **HR Interview** - AI-powered conversational HR interview
4. **Personalized Feedback** - Detailed feedback with improvement suggestions

### ✅ Non-AI Features (Deterministic)
1. **MCQ Evaluation** - Technical multiple-choice questions with auto-grading
2. **Code Execution** - Run code with test cases using Judge0 API
3. **Performance Tracking** - Track interview history and scores

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- Node.js (v18+) & npm

### 2. Backend Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Configure API Keys in .env (Add MISTRAL_API_KEY)
python app.py
```
The backend server will start at `http://127.0.0.1:5000`

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```
The frontend will start at `http://localhost:5173`

## 🔗 Access the Application

- **Frontend (Web UI):** [http://localhost:5173](http://localhost:5173)
- **Backend (API):** [http://127.0.0.1:5000](http://127.0.0.1:5000)
- **Backend Health Check:** [http://127.0.0.1:5000/api/health](http://127.0.0.1:5000/api/health)

## API Endpoints

### User Management
- `POST /api/user/register` - Register or login user by name
- `GET /api/user/profile/<username>` - Get user profile
- `PUT /api/user/profile/<username>` - Update profile

### Resume & Skills
- `POST /api/resume/upload/<username>` - Upload and analyze resume
- `POST /api/resume/match/<username>` - Match resume to job description

### Interview
- `POST /api/interview/start/<username>` - Start interview session
- `POST /api/interview/hr/question` - Get AI-generated HR question
- `POST /api/interview/hr/answer` - Submit and analyze HR answer
- `POST /api/interview/complete/<username>` - Complete interview and get feedback

### Technical Round (MCQ)
- `GET /api/mcq/questions` - Get MCQ questions
- `POST /api/mcq/evaluate` - Evaluate MCQ answers

### Coding Round
- `GET /api/coding/problems` - Get coding problems
- `POST /api/coding/execute` - Execute code with test cases
- `POST /api/coding/submit` - Submit final solution

## Project Structure

```
ai interview/
├── app.py                 # Main Flask application
├── config.py              # Configuration
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (API keys)
│
├── routes/                # API routes
│   ├── user_routes.py
│   ├── resume_routes.py
│   ├── interview_routes.py
│   ├── mcq_routes.py
│   └── coding_routes.py
│
├── services/              # Business logic
│   ├── mistral_service.py    # Mistral AI integration
│   ├── resume_parser.py      # Resume text extraction
│   ├── code_executor.py      # Code execution (Judge0)
│   └── mcq_evaluator.py      # MCQ evaluation
│
├── utils/                 # Utilities
│   └── storage.py         # JSON file storage
│
└── data/                  # Data storage
    ├── users.json         # User profiles
    ├── interviews.json    # Interview history
    ├── feedback.json      # Feedback reports
    ├── questions_mcq.json # MCQ question bank
    ├── questions_coding.json # Coding problems
    └── resumes/           # Uploaded resumes
```

## How It Works

### User Flow

1. **Registration**
   - User enters their name
   - System creates/retrieves user profile
   - All data tracked by username in JSON files

2. **Resume Upload** (Optional)
   - Upload PDF/DOCX/TXT resume
   - Mistral AI extracts skills automatically
   - System analyzes skill gaps

3. **Start Interview**
   - Choose difficulty level
   - Select rounds (HR, Technical, Coding)

4. **HR Round** (AI-Powered)
   - Mistral AI generates contextual questions
   - User provides answers (text/voice)
   - AI analyzes response quality

5. **Technical Round** (MCQ)
   - Answer multiple-choice questions
   - Instant deterministic evaluation
   - Category-wise performance tracking

6. **Coding Round**
   - Solve coding problems
   - Code executed with test cases
   - Real-time feedback

7. **Feedback**
   - Mistral AI generates comprehensive feedback
   - Identifies strengths and weaknesses
   - Provides learning resources

## Data Storage

All data is stored in simple JSON files (no database required):

- **users.json** - User profiles and skills
- **interviews.json** - Interview session history
- **feedback.json** - AI-generated feedback reports

## AI vs Non-AI Features

### AI-Powered (Mistral AI)
✅ Resume skill extraction  
✅ Job description matching  
✅ HR interview questions  
✅ Answer analysis  
✅ Personalized feedback  

### Non-AI (Deterministic)
✅ MCQ evaluation  
✅ Code test case execution  
✅ Score calculation  

## Configuration

### Mistral AI Models
- Default: `mistral-large-latest`
- Alternatives: `mistral-medium`, `mistral-small`

Edit in `config.py`:
```python
MISTRAL_MODEL = 'mistral-large-latest'
```

### Judge0 (Code Execution)
- Free tier available
- Optional: Configure in `.env` for real code execution
- Falls back to mock execution if not configured

## Testing the API

### Example: Register User
```bash
curl -X POST http://127.0.0.1:5000/api/user/register \
  -H "Content-Type: application/json" \
  -d '{"username": "John Doe", "experience_level": "Junior", "target_role": "Full Stack Developer"}'
```

### Example: Get HR Question
```bash
curl -X POST http://127.0.0.1:5000/api/interview/hr/question \
  -H "Content-Type: application/json" \
  -d '{"username": "John Doe", "session_id": "123"}'
```

## Next Steps

1. **Add More Questions:** Expand `data/questions_mcq.json` and `data/questions_coding.json`.
2. **Deploy:** Prepare for production deployment (AWS/Heroku/Vercel).
3. **Enhance UI:** Add more interactive charts and visualizations for feedback.
4. **Voice Support:** Improve voice-to-text accuracy for HR rounds.

## Requirements

- Python 3.8+
- Mistral API key
- (Optional) Judge0 API key for code execution

## License

MIT License

## Support

For issues or questions, please create an issue in the repository.
