from resume_analyzer import analyze_resume
from question_generator import generate_technical_questions, generate_coding_question, generate_hr_question
from answer_analysis import analyze_answer
from coding_engine import evaluate_code
from voice_engine import conduct_multiple_hr_questions
from score_engine import ScoreEngine
from plagiarism_detector import detect_plagiarism, check_code_plagiarism

class InterviewFlow:
    def __init__(self, user_name):
        self.user_name = user_name
        self.scores = ScoreEngine()
        self.ats_result = None
        self.skill_gaps = []
        
    def step1_ats_analysis(self, resume_text, job_description):
        """Step 1: Resume + ATS Analysis"""
        print(f"\n🔍 Analyzing {self.user_name}'s resume...")
        
        self.ats_result = analyze_resume(resume_text, job_description)
        self.skill_gaps = self.ats_result.get('skill_gaps', [])
        
        print(f"ATS Score: {self.ats_result['ats_score']}%")
        if self.ats_result['ats_score'] < 70:
            print(f"⚠️ Skill Gaps Detected: {', '.join(self.skill_gaps[:3])}")
        
        return self.ats_result
    
    def step2_technical_round(self, job_description):
        """Step 2: Technical Q&A Round"""
        print(f"\n💡 Starting Technical Interview for {self.user_name}...")
        
        # Generate questions based on skill gaps
        questions = generate_technical_questions(job_description, self.skill_gaps, n=3)
        
        for i, q_data in enumerate(questions, 1):
            print(f"\n--- Technical Question {i} ---")
            print(f"Q: {q_data['question']}")
            
            answer = input("Your Answer: ")
            
            # Analyze answer
            analysis = analyze_answer(answer, q_data.get('expected_keywords'), q_data['question'])
            
            # Check plagiarism
            plagiarism = detect_plagiarism(answer, q_data['question'])
            
            # Update scores
            self.scores.update_technical(analysis['correctness'])
            self.scores.update_logic(analysis['logic_score'])
            self.scores.update_originality(plagiarism['plagiarism_score'])
            
            print(f"✅ {analysis['feedback']}")
    
    def step3_coding_round(self, job_description):
        """Step 3: Coding Challenge"""
        print(f"\n💻 Coding Challenge for {self.user_name}...")
        
        coding_q = generate_coding_question(job_description)
        print(f"\nProblem: {coding_q['question']}")
        
        user_code = input("\nEnter your code:\n")
        
        # Evaluate code
        test_results = evaluate_code(user_code, coding_q)
        
        # Check code plagiarism
        code_plagiarism = check_code_plagiarism(user_code, coding_q['question'])
        
        # Update scores
        self.scores.update_coding(test_results)
        self.scores.update_originality(code_plagiarism['plagiarism_score'])
        
        print(f"Test Results: {test_results}")
    
    def step4_hr_round(self):
        """Step 4: HR Voice Interview"""
        print(f"\n🎤 HR Interview Round for {self.user_name}...")
        
        confidence_level = conduct_multiple_hr_questions(num_questions=2)
        
        # Update communication score
        self.scores.update_communication(confidence_level)
        
        print(f"Communication Level: {confidence_level}")
    
    def step5_final_results(self):
        """Step 5: Generate Final Results"""
        print(f"\n📊 Generating Results for {self.user_name}...")
        
        final_result = self.scores.final_result()
        
        # Add user info and ATS data
        final_result.update({
            "user_name": self.user_name,
            "ats_score": self.ats_result['ats_score'] if self.ats_result else 0,
            "skill_gaps": self.skill_gaps,
            "feedback": self.generate_feedback(final_result)
        })
        
        return final_result
    
    def generate_feedback(self, results):
        """Generate personalized feedback"""
        pie_data = results['pie_chart']
        lowest_area = min(pie_data, key=pie_data.get)
        
        feedback_map = {
            "Technical Knowledge": "Focus on core technical concepts and domain knowledge.",
            "Logic Building": "Work on explaining your thought process more clearly.",
            "Coding Skills": "Practice more coding problems and algorithm implementation.",
            "Communication": "Improve confidence and clarity in verbal communication.",
            "Originality": "Avoid generic answers. Be more specific and original."
        }
        
        suggestion = feedback_map.get(lowest_area, "Keep practicing all areas.")
        
        if self.skill_gaps:
            suggestion += f" Priority skills to learn: {', '.join(self.skill_gaps[:3])}."
        
        return suggestion

def start_complete_interview(user_name, resume_text, job_description):
    """Main function to run complete interview flow"""
    interview = InterviewFlow(user_name)
    
    # Run all steps
    interview.step1_ats_analysis(resume_text, job_description)
    interview.step2_technical_round(job_description)
    interview.step3_coding_round(job_description)
    interview.step4_hr_round()
    
    # Get final results
    results = interview.step5_final_results()
    
    return results