"""
Individual component testing script
"""

def test_resume_analyzer():
    print("🔍 Testing Resume Analyzer...")
    from resume_analyzer import analyze_resume
    
    resume = "Python developer with ML experience"
    job_desc = "AI Engineer position requiring Python and Machine Learning"
    
    result = analyze_resume(resume, job_desc)
    print(f"ATS Score: {result['ats_score']}%")
    print(f"Skill Gaps: {result['skill_gaps']}")
    print("✅ Resume Analyzer working\n")

def test_question_generator():
    print("❓ Testing Question Generator...")
    from question_generator import generate_technical_questions, generate_coding_question, generate_hr_question
    
    # Technical questions
    questions = generate_technical_questions("AI Engineer", ["python", "ml"], 2)
    print(f"Technical Questions: {len(questions)} generated")
    for q in questions:
        print(f"  - {q['question'][:50]}...")
    
    # Coding question
    coding_q = generate_coding_question("Python Developer")
    print(f"Coding Question: {coding_q['question'][:50]}...")
    
    # HR question
    hr_q = generate_hr_question()
    print(f"HR Question: {hr_q[:50]}...")
    print("✅ Question Generator working\n")

def test_answer_analysis():
    print("📝 Testing Answer Analysis...")
    from answer_analysis import analyze_answer
    
    # Test different answer types
    test_cases = [
        ("Machine learning uses algorithms to learn from data", ["algorithms", "data", "learning"]),
        ("I don't know", ["algorithms", "data"]),
        ("It's about computers", ["algorithms", "data"])
    ]
    
    for answer, keywords in test_cases:
        result = analyze_answer(answer, keywords, "What is machine learning?")
        print(f"Answer: '{answer[:30]}...'")
        print(f"  Correctness: {result['correctness']}")
        print(f"  Feedback: {result['feedback']}")
        print()
    print("✅ Answer Analysis working\n")

def test_coding_engine():
    print("💻 Testing Coding Engine...")
    from coding_engine import evaluate_code
    
    # Test valid code
    good_code = """
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
"""
    
    # Test invalid code
    bad_code = "print('hello world'"
    
    question_data = {"question": "Check if number is prime"}
    
    result1 = evaluate_code(good_code, question_data)
    result2 = evaluate_code(bad_code, question_data)
    
    print(f"Good code result: {result1}")
    print(f"Bad code result: {result2}")
    print("✅ Coding Engine working\n")

def test_voice_engine():
    print("🎤 Testing Voice Engine...")
    from voice_engine import analyze_communication
    
    test_answers = [
        "I am confident in my abilities and have strong technical skills",
        "Um, I think maybe I can do this job",
        "I don't know if I'm qualified"
    ]
    
    for answer in test_answers:
        confidence = analyze_communication(answer)
        print(f"Answer: '{answer[:40]}...'")
        print(f"  Confidence Level: {confidence}")
        print()
    print("✅ Voice Engine working\n")

def test_score_engine():
    print("📊 Testing Score Engine...")
    from score_engine import ScoreEngine
    
    scores = ScoreEngine()
    
    # Simulate scoring
    scores.update_technical("correct")
    scores.update_logic(8)
    scores.update_coding("all_passed")
    scores.update_communication("high")
    scores.update_originality(20)  # 20% plagiarism
    
    result = scores.final_result()
    
    print("Final Scores:")
    for category, score in result['pie_chart'].items():
        print(f"  {category}: {score}")
    print(f"Total Score: {result['total_score']}")
    print("✅ Score Engine working\n")

def test_plagiarism_detector():
    print("🔍 Testing Plagiarism Detector...")
    from plagiarism_detector import detect_plagiarism, check_code_plagiarism
    
    # Test text plagiarism
    original_answer = "Machine learning is a subset of AI that uses algorithms to learn patterns from data"
    generic_answer = "I think machine learning is about computers learning stuff"
    
    result1 = detect_plagiarism(original_answer)
    result2 = detect_plagiarism(generic_answer)
    
    print(f"Original answer plagiarism: {result1['plagiarism_score']}%")
    print(f"Generic answer plagiarism: {result2['plagiarism_score']}%")
    
    # Test code plagiarism
    code = "def hello(): print('hello world')"
    code_result = check_code_plagiarism(code, "Write a hello world function")
    print(f"Code plagiarism: {code_result['plagiarism_score']}%")
    print("✅ Plagiarism Detector working\n")

def run_all_tests():
    print("🧪 COMPONENT TESTING STARTED")
    print("=" * 50)
    
    try:
        test_resume_analyzer()
        test_question_generator()
        test_answer_analysis()
        test_coding_engine()
        test_voice_engine()
        test_score_engine()
        test_plagiarism_detector()
        
        print("🎉 ALL COMPONENTS WORKING CORRECTLY!")
        
    except Exception as e:
        print(f"❌ Error in component testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()