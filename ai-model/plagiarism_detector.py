import google.generativeai as genai
import os
from dotenv import load_dotenv
import re

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.5-flash")

def detect_plagiarism(answer, question_context=""):
    """
    Simple plagiarism detection using pattern matching and AI analysis
    Returns plagiarism score (0-100, where 100 = high plagiarism)
    """
    
    # Basic pattern checks
    generic_patterns = [
        r"according to my knowledge",
        r"in my opinion",
        r"i think that",
        r"it depends on",
        r"there are many ways"
    ]
    
    pattern_score = 0
    for pattern in generic_patterns:
        if re.search(pattern, answer.lower()):
            pattern_score += 15
    
    # AI-based originality check
    prompt = f"""
    Analyze this interview answer for originality (0-100 scale):
    Question context: {question_context}
    Answer: {answer}
    
    Rate plagiarism likelihood:
    - 0-20: Original, specific answer
    - 21-40: Somewhat generic but acceptable
    - 41-60: Very generic, template-like
    - 61-80: Likely copied or memorized
    - 81-100: Definitely plagiarized
    
    Return only the number.
    """
    
    try:
        ai_score = int(model.generate_content(prompt).text.strip())
    except:
        ai_score = 30  # Default moderate score
    
    # Combine scores (weighted average)
    final_score = min(100, (pattern_score * 0.3) + (ai_score * 0.7))
    
    return {
        "plagiarism_score": int(final_score),
        "originality_level": "high" if final_score < 30 else "medium" if final_score < 60 else "low"
    }

def check_code_plagiarism(code, problem_statement):
    """
    Check if code looks like a standard template or copied solution
    """
    
    # Basic checks for overly generic variable names
    generic_indicators = ["temp", "var", "x", "y", "result", "output"]
    generic_count = sum(1 for var in generic_indicators if var in code.lower())
    
    # Check for comments that seem copied
    comment_patterns = [
        r"#.*solution.*online",
        r"//.*copied.*from",
        r"#.*stackoverflow",
        r"//.*geeksforgeeks"
    ]
    
    comment_score = 0
    for pattern in comment_patterns:
        if re.search(pattern, code.lower()):
            comment_score += 40
    
    # AI analysis for code originality
    prompt = f"""
    Analyze this code for plagiarism indicators (0-100):
    Problem: {problem_statement}
    Code: {code}
    
    Check for:
    - Generic variable names
    - Standard template patterns
    - Lack of personal coding style
    
    Return plagiarism score (0-100).
    """
    
    try:
        ai_score = int(model.generate_content(prompt).text.strip())
    except:
        ai_score = 25
    
    total_score = min(100, (generic_count * 5) + comment_score + (ai_score * 0.6))
    
    return {
        "plagiarism_score": int(total_score),
        "originality_level": "high" if total_score < 25 else "medium" if total_score < 50 else "low"
    }