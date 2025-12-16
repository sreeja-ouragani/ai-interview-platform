import sys
import os
sys.path.append('ai-model')

from interview_engine import start_complete_interview

def quick_test():
    """Quick test with sample data"""
    
    print("🧠 AI Interview Platform - Quick Test")
    print("=" * 40)
    
    # Sample data for testing
    user_name = "Test User"
    
    sample_resume = """
    John Doe
    Software Engineer
    Skills: Python, JavaScript, React, Node.js, SQL
    Experience: 3 years in web development
    Education: Computer Science degree
    """
    
    sample_job = """
    Senior Python Developer
    Required Skills: Python, Django, PostgreSQL, AWS, Docker
    Experience: 3+ years
    Responsibilities: Backend development, API design, database optimization
    """
    
    print(f"Testing interview flow for: {user_name}")
    print("Using sample resume and job description...")
    
    try:
        results = start_complete_interview(user_name, sample_resume, sample_job)
        
        print("\n" + "="*50)
        print("🎯 TEST RESULTS")
        print("="*50)
        
        print(f"User: {results['user_name']}")
        print(f"ATS Score: {results['ats_score']}%")
        print(f"Total Score: {results['total_score']}")
        
        print("\nScore Breakdown:")
        for category, score in results['pie_chart'].items():
            print(f"  {category}: {score}")
        
        print(f"\nFeedback: {results['feedback']}")
        
        print("\n✅ Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    quick_test()