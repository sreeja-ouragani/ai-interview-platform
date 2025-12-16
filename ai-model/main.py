from interview_engine import start_complete_interview

def main():
    """Test the complete interview flow"""
    
    print("🧠 AI-Powered Interview Platform")
    print("=" * 40)
    
    # Step 1: Get user name (simulating frontend input)
    user_name = input("Enter your name: ")
    
    # Step 2: Get resume and job description (simulating file upload)
    print(f"\nHello {user_name}! Let's start your interview preparation.")
    
    resume_text = input("\nPaste your resume text: ")
    job_description = input("\nPaste job description: ")
    
    # Run complete interview
    try:
        results = start_complete_interview(user_name, resume_text, job_description)
        
        # Display final results (simulating frontend dashboard)
        print("\n" + "="*50)
        print(f"🎯 INTERVIEW RESULTS FOR {results['user_name'].upper()}")
        print("="*50)
        
        print(f"\n📊 SCORES BREAKDOWN:")
        print(f"Technical Knowledge: {results['technical_knowledge']}/30")
        print(f"Logic Building: {results['logic_building']}/30") 
        print(f"Coding Skills: {results['coding_skills']}/20")
        print(f"Communication: {results['communication']}/45")
        print(f"Originality: {results['originality']}/100")
        print(f"\nTOTAL SCORE: {results['total_score']}/225")
        
        print(f"\n🎯 ATS SCORE: {results['ats_score']}%")
        
        print(f"\n💡 FEEDBACK:")
        print(f"{results['feedback']}")
        
        print(f"\n📈 PIE CHART DATA:")
        for category, score in results['pie_chart'].items():
            percentage = (score / results['total_score']) * 100 if results['total_score'] > 0 else 0
            print(f"{category}: {percentage:.1f}%")
            
    except Exception as e:
        print(f"Error during interview: {e}")

if __name__ == "__main__":
    main()