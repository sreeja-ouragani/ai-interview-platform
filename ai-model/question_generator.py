import google.generativeai as genai
import os
from dotenv import load_dotenv
from offline_mode import get_offline_technical_questions, get_offline_coding_question, get_offline_hr_question

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-2.5-flash")

# Flag to use offline mode when API fails
USE_OFFLINE_MODE = False

def generate_technical_questions(job_desc, skill_gaps=None, n=3):
    """Generate technical questions with expected keywords"""
    global USE_OFFLINE_MODE
    
    if USE_OFFLINE_MODE:
        return get_offline_technical_questions(job_desc, skill_gaps, n)
    
    try:
        gap_context = f"Focus on these missing skills: {', '.join(skill_gaps)}" if skill_gaps else ""
        
        prompt = f"""
        Generate {n} technical interview questions for this job:
        {job_desc}
        {gap_context}
        
        For each question, also provide 3-5 key terms/concepts that should appear in a good answer.
        Format: Question | Keywords: term1, term2, term3
        """
        
        response = model.generate_content(prompt).text
        questions = []
        
        for line in response.split("\n"):
            if "|" in line and "Keywords:" in line:
                parts = line.split("|")
                question = parts[0].strip()
                keywords = [k.strip() for k in parts[1].replace("Keywords:", "").split(",")]
                questions.append({
                    "question": question,
                    "expected_keywords": keywords
                })
            elif line.strip() and not line.startswith("Keywords:"):
                questions.append({
                    "question": line.strip(),
                    "expected_keywords": []
                })
        
        return questions[:n]
        
    except Exception as e:
        print(f"⚠️ API limit reached. Switching to offline mode...")
        USE_OFFLINE_MODE = True
        return get_offline_technical_questions(job_desc, skill_gaps, n)

def generate_coding_question(job_desc, difficulty="medium"):
    """Generate coding question with test cases"""
    global USE_OFFLINE_MODE
    
    if USE_OFFLINE_MODE:
        return get_offline_coding_question()
    
    try:
        prompt = f"""
        Generate one {difficulty} coding interview question for: {job_desc}
        
        Include:
        1. Clear problem statement
        2. Input/output examples
        3. At least 2 test cases
        
        Format:
        PROBLEM: [statement]
        EXAMPLE: [input/output]
        TEST_CASES: [case1] | [case2]
        """
        
        response = model.generate_content(prompt).text
        
        # Parse response
        problem = ""
        test_cases = []
        
        lines = response.split("\n")
        for line in lines:
            if line.startswith("PROBLEM:"):
                problem = line.replace("PROBLEM:", "").strip()
            elif line.startswith("TEST_CASES:"):
                cases_text = line.replace("TEST_CASES:", "").strip()
                # Simple parsing - in real implementation, use better parsing
                test_cases = [{"input": [1, 2], "expected": 3}]  # Placeholder
        
        return {
            "question": problem or response,
            "test_cases": test_cases,
            "difficulty": difficulty
        }
        
    except Exception as e:
        print(f"⚠️ API limit reached. Using offline coding question...")
        USE_OFFLINE_MODE = True
        return get_offline_coding_question()

def generate_hr_question():
    global USE_OFFLINE_MODE
    
    if USE_OFFLINE_MODE:
        return get_offline_hr_question()
    
    try:
        prompt = "Ask one friendly HR interview question."
        return model.generate_content(prompt).text
    except Exception as e:
        print(f"⚠️ API limit reached. Using offline HR question...")
        USE_OFFLINE_MODE = True
        return get_offline_hr_question()
