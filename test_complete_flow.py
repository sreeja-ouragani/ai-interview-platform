"""
AI Interview Platform - Real-Time Interactive Flow with Enhanced Voice Interface
Complete interview simulation with AI-powered plagiarism detection
"""

import requests
import json
import time
import os

# Global imports
import subprocess
try:
    import speech_recognition as sr
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    sr = None

BASE_URL = "http://127.0.0.1:5000/api"

# Global variables
recognizer = None
mic = None

# Initialize voice engine if available
if VOICE_AVAILABLE:
    try:
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 2000
        recognizer.dynamic_energy_threshold = True
        mic = sr.Microphone()
        print("✅ Voice system initialized (Windows Native + SpeechRecognition)")
    except Exception as e:
        print(f"⚠️ Voice Init Error: {e}")
        VOICE_AVAILABLE = False

def speak(text):
    """Speak text using Windows native TTS via PowerShell"""
    if not text:
        return

    print(f"\n🎧 AI is speaking...", end="", flush=True)
    
    # Sanitize text for PowerShell
    # Replace curly quotes with straight ones, then escape single quotes by doubling them
    safe_text = text.replace("’", "'").replace("‘", "'").replace('"', '').replace('\n', ' ')
    safe_text = safe_text.replace("'", "''") 
    
    ps_command = f"Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('{safe_text}')"
    
    try:
        subprocess.run(["powershell", "-Command", ps_command], check=False)
    except Exception as e:
        print(f"\n⚠️ TTS Error: {e}")
        time.sleep(2)
    
    print(" ✅ Done")

def listen():
    """Listen continuously until silence is detected"""
    if not VOICE_AVAILABLE:
        return input("\n✍️  Your answer (type): ")
    
    print(f"\n🎤 {'='*70}")
    print("🎤 LISTENING... Speak your answer freely.")
    print("👉 Stop speaking for 3 seconds to submit automatically.")
    print(f"{'='*70}")
    
    full_transcript = []
    
    with mic as source:
        print("   (Adjusting for ambient noise... please wait)")
        recognizer.adjust_for_ambient_noise(source, duration=1.0)
        recognizer.dynamic_energy_threshold = True
        recognizer.pause_threshold = 2.0  # Wait 2 seconds of silence before considering it "done"
        
        # Try to capture the whole phrase in one go if possible, or loop for long answers
        try:
            print("   (Listening...)")
            # Listen until silence is detected
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=None)
            print("   (Processing...)")
            
            text = recognizer.recognize_google(audio).lower()
            print(f"   ➜ Heard: \"{text}\"")
            return text
            
        except sr.WaitTimeoutError:
            print("   ⌛ Silence detected (Timeout). Assuming you are done.")
            return ""
        except sr.UnknownValueError:
            print("   ⚠️ Not clear. Please try again or type.")
            return input("\n✍️  Your answer (type fallback): ")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            return ""

def print_header(title):
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

def print_step(step, description):
    print(f"\n{'🔹'} {step}: {description}")
    print("-" * 80)

def wait_continue():
    input("\n⏸️  Press ENTER to continue...")

# ============================================================================
# START INTERVIEW PROCESS
# ============================================================================

print_header("🎯 AI INTERVIEW PLATFORM - REAL-TIME INTERVIEW")
print("\n📋 Interview Flow:")
print("  1. Registration")
print("  2. Technical MCQ Round")
print("  3. Coding Round (AI Plagiarism Detection)")
print("  4. Managerial Round (Voice-based AI)")
print("  5. HR Round (Voice-based AI)")
print("  6. Feedback & Results")
print("  7. Recruiter Evaluation\n")

if VOICE_AVAILABLE:
    print("✅ Voice mode: ENABLED")
else:
    print("⚠️  Voice mode: DISABLED (Install: pip install SpeechRecognition pyttsx3 pyaudio)")

# ============================================================================
# STEP 1: USER REGISTRATION
# ============================================================================

print_header("STEP 1: USER REGISTRATION")

username = input("\n👤 Enter your full name: ").strip()
if not username:
    print("❌ Name is required!")
    exit()

experience = input("💼 Experience level (Fresher/Junior/Mid/Senior): ").strip() or "Junior"
target_role = input("🎯 Target role: ").strip() or "Full Stack Developer"

# New: Ask for Job Description
print("\n📋 (Optional) Paste the Job Description here for better Skill Gap Analysis:")
print("   (Press ENTER to use a default generic description)")
custom_jd = input("   👉 JD: ").strip()

print(f"\n✅ Registering {username}...")

user_data = {
    "username": username,
    "experience_level": experience,
    "target_role": target_role,
    "target_company_type": "Product",
    "job_description": custom_jd # Store this if needed
}

response = requests.post(f"{BASE_URL}/user/register", json=user_data)
if response.status_code in [200, 201]:
    print(f"✅ Registration successful!")
    print(f"👤 Name: {username}")
    print(f"💼 Level: {experience}")
    print(f"🎯 Role: {target_role}")
else:
    print(f"❌ Registration failed: {response.text}")
    exit()

# ============================================================================
# STEP 1.5: RESUME UPLOAD & SKILL GAP ANALYSIS
# ============================================================================

# ============================================================================
# STEP 1.5: RESUME UPLOAD & SKILL GAP ANALYSIS
# ============================================================================

print("\n" + "-"*80)
print("📄 RESUME UPLOAD & SKILL ANALYSIS")
print("-" * 80)

import tkinter as tk
from tkinter import filedialog

def select_file():
    root = tk.Tk()
    root.withdraw() # Hide small window
    root.attributes('-topmost', True) # Bring to front
    print("\n📂 Opening file picker... Please select your resume.")
    file_path = filedialog.askopenfilename(
        title="Select Resume",
        filetypes=[("Resume Files", "*.pdf *.docx *.txt")]
    )
    root.destroy()
    return file_path

while True:
    print("\n👉 Please select your resume file to upload.")
    choice = input("   Press ENTER to open file picker (or type 'skip' or 'path'): ").strip()
    
    if choice.lower() == 'skip':
        print("⚠️  Skipping resume analysis.")
        break
    
    if os.path.exists(choice):
        resume_path = choice
    else:
        resume_path = select_file()
    
    if not resume_path:
        print("⚠️  No file selected. Please try again.")
        continue
        
    print(f"\n⏳ Uploading and analyzing {os.path.basename(resume_path)}...")
    
    try:
        with open(resume_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{BASE_URL}/resume/upload/{username}", files=files)
            
        if response.status_code == 200:
            data = response.json()
            skills = data.get('skills', {})
            
            print(f"\n✅ Resume Analyzed Successfully!")
            print(f"\n🧠 Extracted Skills:")
            
            tech_skills = skills.get('technical_skills', [])
            if isinstance(tech_skills, str): tech_skills = [tech_skills]
            print(f"   💻 Technical: {', '.join(tech_skills[:15])}")
            
            soft_skills = skills.get('soft_skills', [])
            if isinstance(soft_skills, str): soft_skills = [soft_skills]
            print(f"   🗣️  Soft Skills: {', '.join(soft_skills[:10])}")
            
            print(f"   📊 Experience: {skills.get('experience_years', 'N/A')}")
            
            # Perform Skill Gap Analysis
            print(f"\n🔍 Performing Skill Gap Analysis for '{target_role}'...")
            
            if custom_jd:
                jd_text = custom_jd
                print("   (Using provided Job Description)")
            else:
                # Dynamic JD Generation
                tech_stack = "Python, JavaScript, SQL, Git"
                if "full stack" in target_role.lower():
                    tech_stack += ", React, Node.js, HTML/CSS, REST APIs"
                elif "data" in target_role.lower():
                    tech_stack += ", Pandas, NumPy, SQL, Machine Learning"
                
                senior_reqs = ""
                if "senior" in experience.lower():
                    senior_reqs = ", System Design, Cloud Architecture, Leadership"
                
                jd_text = f"We are looking for a {target_role} with expertise in {tech_stack}{senior_reqs}."
                print(f"   (Using auto-generated JD for {target_role}: {jd_text})")
            
            match_response = requests.post(f"{BASE_URL}/resume/match/{username}", json={"job_description": jd_text})
            
            if match_response.status_code == 200:
                match_data = match_response.json().get('match_result', {})
                print(f"\n📊 Match Score: {match_data.get('match_score', 0)}/100")
                
                missing = match_data.get('missing_skills', [])
                if missing:
                    print(f"⚠️  Missing Skills: {', '.join(missing)}")
                else:
                    print(f"✅ No major skill gaps found!")
            else:
                print("⚠️  Could not perform gap analysis.")
            
            break
        else:
            print(f"❌ Upload failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error during upload: {e}")

wait_continue()

# ============================================================================
# STEP 2: START INTERVIEW SESSION
# ============================================================================

print_header("STEP 2: START INTERVIEW SESSION")

interview_data = {
    "difficulty": "Medium",
    "rounds": ["Technical", "Coding", "Managerial", "HR"]
}

response = requests.post(f"{BASE_URL}/interview/start/{username}", json=interview_data)
session = response.json().get('session', {})
session_id = session.get('session_id')

print(f"✅ Interview session started!")
print(f"🎫 Session ID: {session_id}")
print(f"📋 Rounds: {' → '.join(session.get('rounds', []))}")
print(f"⚡ Difficulty: {session.get('difficulty')}")

wait_continue()

# ============================================================================
# STEP 3: TECHNICAL MCQ ROUND (Non-AI)
# ============================================================================

print_header("STEP 3: TECHNICAL MCQ ROUND")

print("\n📝 Fetching MCQ questions...")
# Request all difficulties to ensure we get 10 questions
response = requests.get(f"{BASE_URL}/mcq/questions?difficulty=all&count=10")
questions = response.json().get('questions', [])

print(f"✅ You have {len(questions)} questions")
print("⏱️  Answer each question by typing A, B, C, or D\n")

user_answers = {}
for i, q in enumerate(questions, 1):
    print(f"\n{'='*80}")
    print(f"Question {i}/{len(questions)}")
    print(f"{'='*80}")
    print(f"\n❓ {q['question']}\n")
    
    for option in q['options']:
        print(f"   {option}")
    
    while True:
        answer = input("\n✍️  Your answer (A/B/C/D): ").strip().upper()
        if answer in ['A', 'B', 'C', 'D']:
            user_answers[q['id']] = answer
            print(f"✅ Answer recorded: {answer}")
            break
        else:
            print("❌ Invalid input. Please enter A, B, C, or D")

print("\n🔍 Evaluating your answers...")
eval_data = {"answers": user_answers}
response = requests.post(f"{BASE_URL}/mcq/evaluate", json=eval_data)

if response.status_code == 200:
    result = response.json()
    evaluation = result.get('evaluation', {})
    analysis = result.get('analysis', {})
    
    print(f"\n{'='*80}")
    print("📊 TECHNICAL MCQ RESULTS")
    print(f"{'='*80}")
    print(f"✅ Correct Answers: {evaluation.get('correct_answers')}/{evaluation.get('total_questions')}")
    print(f"📈 Score: {evaluation.get('score_percentage')}%")
    print(f"🎯 Performance: {analysis.get('performance_level')}")
    print(f"💬 Feedback: {analysis.get('feedback')}")
    
    mcq_score = evaluation.get('score_percentage', 0)
else:
    print("❌ Evaluation failed")
    mcq_score = 0

wait_continue()

# ============================================================================
# STEP 4: CODING ROUND (AI Plagiarism Detection)
# ============================================================================

print_header("STEP 4: CODING ROUND (AI Plagiarism Detection)")

print("\n💻 Fetching coding problems...")
response = requests.get(f"{BASE_URL}/coding/problems?difficulty=Easy")
problems = response.json().get('problems', [])

if not problems:
    print("❌ No problems available")
    coding_score = 0
else:
    # Select up to 2 problems
    selected_problems = problems[:2]
    total_coding_score = 0
    
    for i, problem in enumerate(selected_problems, 1):
        print(f"\n{'#'*80}")
        print(f"CODING CHALLENGE {i}/{len(selected_problems)}")
        print(f"{'#'*80}")
        
        print(f"\n{'='*80}")
        print(f"Problem: {problem['title']}")
        print(f"{'='*80}")
        print(f"\n📝 {problem['description']}")
        print(f"\n📋 Example:")
        print(problem.get('example', ''))
        
        print(f"\n🧪 Sample Test Cases:")
        for idx, tc in enumerate(problem.get('test_cases', [])[:2], 1):
            print(f"\n  Test Case {idx}:")
            print(f"    Input: {tc['input']}")
            print(f"    Expected Output: {tc['expected_output']}")
        
        print(f"\n{'='*80}")
        print("✍️  Write your solution below (type 'END' on a new line when done):")
        print(f"{'='*80}\n")
        
        code_lines = []
        while True:
            line = input()
            if line.strip() == 'END':
                break
            code_lines.append(line)
        
        code = '\n'.join(code_lines)
        
        if not code.strip():
            print("\n⚠️  No code provided!")
            code = ""
        
        print(f"\n🔍 Submitting solution for Problem {i}...")
        print("⏳ Running test cases...")
        print("🤖 AI Plagiarism Detection in progress...")
        
        
        while True:
            action = input("\n👉 Type 'RUN' to test your code, or 'SUBMIT' to finish: ").strip().upper()
            
            if action == 'RUN':
                print(f"\n🏃 Running code against test cases...")
                run_data = {
                    "problem_id": problem['id'],
                    "code": code,
                    "language": "python"
                }
                
                # Use execute endpoint for just running
                response = requests.post(f"{BASE_URL}/coding/execute", json=run_data)
                
                if response.status_code == 200:
                    result_data = response.json().get('result', {})
                    print(f"\n📊 EXECUTION RESULTS:")
                    print(f"   ✅ Passed: {result_data.get('passed', 0)} / {result_data.get('total_tests', 0)}")
                    print(f"   ❌ Failed: {result_data.get('failed', 0)}")
                    
                    print(f"\n   📝 Output Details:")
                    for res in result_data.get('results', []):
                         status_icon = "✅" if res.get('passed') else "❌"
                         print(f"     TestCase {res.get('test_case_number')}: {status_icon}")
                         if not res.get('passed'):
                             print(f"       Expected: {res.get('expected_output')}")
                             print(f"       Actual:   {res.get('actual_output')}")
                else:
                    print(f"❌ Execution failed: {response.text}")
                    
            elif action == 'SUBMIT':
                break
            else:
                print("⚠️  Invalid command. Type RUN or SUBMIT.")

        print(f"\n🔍 Submitting final solution for Problem {i}...")
        print("⏳ Running final validation...")
        print("🤖 AI Plagiarism Detection in progress...")
        
        submit_data = {
            "username": username,
            "problem_id": problem['id'],
            "code": code,
            "language": "python"
        }
        
        response = requests.post(f"{BASE_URL}/coding/submit", json=submit_data)
        
        if response.status_code == 200:
            result = response.json()
            exec_result = result.get('result', {})
            plagiarism = result.get('plagiarism_check', {})
            
            print(f"\n{'='*80}")
            print(f"📊 RESULTS: {problem['title']}")
            print(f"{'='*80}")
            print(f"\n✅ Test Cases Passed: {exec_result.get('passed')}/{exec_result.get('total_tests')}")
            print(f"📈 Score: {exec_result.get('score')}%")
            
            print(f"\n🤖 AI Plagiarism Detection:")
            print(f"  Status: {'⚠️ PLAGIARIZED' if plagiarism.get('is_plagiarized') else '✅ ORIGINAL'}")
            print(f"  Quality Score: {plagiarism.get('quality_score', 'N/A')}")
            
            total_coding_score += exec_result.get('score', 0)
        else:
            print("❌ Submission failed")
    
    # Average score
    coding_score = total_coding_score / len(selected_problems)
    print(f"\n🏆 Final Coding Round Score: {coding_score}%")

wait_continue()

# ============================================================================
# STEP 5: INTRO & ADAPTIVE VOICE ROUNDS (4 Questions Total)
# ============================================================================

print_header("STEP 5: INTRO & ADAPTIVE VOICE ROUNDS")

print("\n🎤 Welcome to the Adaptive Voice Interview!")
print("📋 Routine: 1 Self-Intro + 3 AI Generated Questions")
print("🎤 Voice mode: " + ("ENABLED ✅" if VOICE_AVAILABLE else "DISABLED (Text mode)"))

if VOICE_AVAILABLE:
    print("\n🔊 The AI recruiter will speak to you")
    print("🎤 You can respond by speaking (Voice Only Mode)")

input("\n▶️  Press ENTER to start Voice Interview Rounds...")

# --- QUESTION 1: SELF INTRODUCTION ---
print("\n" + "="*80)
print("ROUND 1: SELF INTRODUCTION")
print("="*80)

intro_q = "Hello! Let's start. Please introduce yourself and tell me about your background."
speak(intro_q)

print("\n🎤 LISTENING... Speak your introduction.")
if VOICE_AVAILABLE:
    intro_text = listen()
    print(f"✅ Introduction recorded\n")
else:
    intro_text = input("\n✍️  Your Introduction: ")

# Analyze Introduction
print("\n🧠 AI is analyzing your introduction...")
try:
    response = requests.post(f"{BASE_URL}/interview/intro", json={
        "username": username,
        "intro_text": intro_text
    })
    if response.status_code == 200:
        analysis = response.json().get('analysis', {})
        print(f"   ✅ Detected Skills: {', '.join(analysis.get('spoken_skills', []))}")
        print(f"   📊 Confidence: {analysis.get('confidence_level', 'N/A')}")
    else:
        print("   ⚠️ Analysis failed, proceeding...")
except Exception as e:
    print(f"   ⚠️ Connection error: {e}")


# --- QUESTIONS 2-5: PROJECT & BEHAVIORAL ROUNDS ---
# 2 Questions on Projects (Resume based)
# 2 Questions on Behavioral (Managerial)

rounds_config = [
    {"type": "project",    "tone": "neutral",  "label": "ROUND 2: PROJECT DEEP DIVE (1/2)"},
    {"type": "project",    "tone": "neutral",  "label": "ROUND 3: PROJECT DEEP DIVE (2/2)"},
    {"type": "managerial", "tone": "friendly", "label": "ROUND 4: BEHAVIORAL (1/2)"},
    {"type": "managerial", "tone": "strict",   "label": "ROUND 5: BEHAVIORAL (2/2)"}
]

conversation_history = []

for idx, round_cfg in enumerate(rounds_config):
    print("\n" + "="*80)
    print(round_cfg['label'])
    print("="*80)
    
    # generate question
    endpoint = f"{BASE_URL}/interview/{round_cfg['type']}/question"
    payload = {
        "username": username, 
        "session_id": session_id,
        "conversation_history": conversation_history,
        "tone": round_cfg['tone']
    }
    
    try:
        response = requests.post(endpoint, json=payload)
        if response.status_code == 200:
            question = response.json().get('question', '')
            speak(question)
            
            # Listen for answer
            if VOICE_AVAILABLE:
                answer = listen()
                print(f"✅ Answer recorded\n")
            else:
                answer = input("\n✍️  Your answer: ")
                
            # Add to history so next question is context-aware
            conversation_history.append({"question": question, "answer": answer})
            
            # Analyze answer immediately to get score
            analysis_endpoint = f"{BASE_URL}/interview/hr/answer" # Using HR endpoint for generic analysis reuse
            # NOTE: Ideally we would have specific endpoints or a unified 'analyze' endpoint.
            # For now, let's assume we can use the HR answer analysis or add a similar one.
            # However, looking at routes, 'submit_hr_answer' creates an analysis.
            # We need to capture these scores.
            
            # Let's call the analysis endpoint to get the score for this round
            # We'll treat all verbal answers as "HR-like" for analysis purposes in this script context 
            # to keep it simple, or we can just rely on the final aggregation.
            # BUT, the user wants "qualitative" to be "quantitative".
            # So we SHOULD analyze headers here.
            
            analyze_payload = {
                "username": username,
                "session_id": session_id,
                "question": question,
                "answer": answer
            }
            
            # We can use the existing /hr/answer route for detailed analysis of text
            # regardless of whether it was a "managerial" or "project" question, 
            # as the underlying mechanism `analyze_hr_response` is generic enough (text -> analysis).
            
            anres = requests.post(f"{BASE_URL}/interview/hr/answer", json=analyze_payload)
            if anres.status_code == 200:
                an_data = anres.json().get('analysis', {})
                round_score = an_data.get('Overall Score', 0)
                # If it's a dict/json inside, we try to parse it, 
                # but `mistral_service` returns a dict directly now if successful.
                # MistralService.analyze_hr_response returns a DICT.
                
                # Normalize key access
                if isinstance(round_score, str):
                    try: 
                        round_score = float(round_score) 
                    except: 
                        round_score = 0
                
                # Store this score
                if 'scores' not in session: session['scores'] = []
                session['scores'].append(round_score)
                print(f"   📊 AI Score for this answer: {round_score}/100")
            
        else:
            print(f"❌ Failed to get question: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

wait_continue()

# Calculate Verbal Score
verbal_scores = session.get('scores', [])
verbal_avg = sum(verbal_scores) / len(verbal_scores) if verbal_scores else 0
print(f"📝 Average Verbal Score: {verbal_avg:.1f}")

# ============================================================================
# STEP 6: FEEDBACK & RESULTS
# ============================================================================

print_header("STEP 7: COMPREHENSIVE FEEDBACK & RESULTS")

print("\n🔍 AI is analyzing your complete interview performance...")
print("⏳ Generating personalized feedback...")

overall_score = (mcq_score * 0.2) + (coding_score * 0.4) + (verbal_avg * 0.4)

complete_data = {
    "interview_data": {
        "session_id": session_id,
        "username": username,
        "overall_score": overall_score,
        "rounds_completed": ["Technical", "Coding", "Managerial", "HR"],
        "mcq_score": mcq_score,
        "coding_score": coding_score,
        "verbal_score": verbal_avg
    }
}

response = requests.post(f"{BASE_URL}/interview/complete/{username}", json=complete_data)

if response.status_code == 200:
    result = response.json()
    feedback = result.get('feedback', {})
    
    print(f"\n{'='*80}")
    print("📊 FINAL INTERVIEW RESULTS")
    print(f"{'='*80}")
    print(f"\n🎯 Overall Score: {overall_score:.1f}/100")
    print(f"\n📈 Round-wise Scores:")
    print(f"  Technical MCQ: {mcq_score}%")
    print(f"  Coding: {coding_score}%")
    print(f"  Verbal (Managerial/HR/Project): {verbal_avg:.1f}%")
    
    print(f"\n💪 Strengths:")
    for strength in feedback.get('Strengths', []):
        print(f"  ✅ {strength}")
    
    print(f"\n⚠️  Areas for Improvement:")
    for weakness in feedback.get('Weaknesses', []):
        print(f"  📌 {weakness}")
    
    print(f"\n📚 Recommended Learning Resources:")
    for resource in feedback.get('Learning resources recommendations', []):
        print(f"  📖 {resource}")

wait_continue()

# ============================================================================
# STEP 8: RECRUITER EVALUATION (B2B)
# ============================================================================

print_header("STEP 8: RECRUITER DASHBOARD")

print("\n🏢 Simulating recruiter evaluation...")

# Register recruiter
recruiter_data = {
    "company_name": "TechCorp",
    "email": "hr@techcorp.com",
    "contact_person": "Hiring Manager"
}

requests.post(f"{BASE_URL}/recruiter/register", json=recruiter_data)

# Create batch
batch_data = {
    "company_name": "TechCorp",
    "batch_name": "Interview Batch 2025",
    "shortlist_threshold": 70
}

response = requests.post(f"{BASE_URL}/recruiter/batch/create", json=batch_data)
if response.status_code == 201:
    batch = response.json().get('batch', {})
    batch_id = batch.get('batch_id')
    
    # Add candidate to batch
    add_data = {
        "company_name": "TechCorp",
        "username": username
    }
    requests.post(f"{BASE_URL}/recruiter/batch/{batch_id}/add-candidate", json=add_data)
    
    # Auto-shortlist
    shortlist_data = {"company_name": "TechCorp"}
    response = requests.post(f"{BASE_URL}/recruiter/batch/{batch_id}/auto-shortlist", json=shortlist_data)
    
    if response.status_code == 200:
        result = response.json()
        
        print(f"\n{'='*80}")
        print("🏢 RECRUITER EVALUATION")
        print(f"{'='*80}")
        print(f"\n📊 Shortlist Threshold: {result.get('threshold')}%")
        print(f"🎯 Your Score: {overall_score:.1f}%")
        
        if username in result.get('shortlisted', []):
            print(f"\n✅ RESULT: SHORTLISTED! 🎉")
            print("Congratulations! You have been selected for the next round.")
        else:
            print(f"\n❌ RESULT: NOT SHORTLISTED")
            print("Keep practicing and try again!")

# ============================================================================
# COMPLETION
# ============================================================================

print(f"\n{'='*80}")
print("🎉 INTERVIEW PROCESS COMPLETE!")
print(f"{'='*80}")

print(f"""
✅ All Rounds Completed:
  1. ✅ User Registration
  2. ✅ Technical MCQ Round (Score: {mcq_score}%)
  3. ✅ Coding Round (Score: {coding_score}%) - AI Plagiarism Detection
  4. ✅ Managerial Round (Voice-based AI)
  5. ✅ HR Round (Voice-based AI)
  6. ✅ Comprehensive Feedback Generated (AI)
  7. ✅ Recruiter Evaluation Complete

🎯 Final Score: {overall_score:.1f}/100

Thank you for using the AI Interview Platform! 🚀
""")
