import google.generativeai as genai
import os
import re
from dotenv import load_dotenv
from answer_analysis import analyze_answer  # Import analysis function

# Load API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("API key not found. Add GEMINI_API_KEY in .env file.")
genai.configure(api_key=API_KEY)

# Function to clean AI-generated questions and remove numbering
def clean_questions(questions):
    cleaned = []
    for q in questions:
        # Remove unwanted numbering (e.g., "1. ", "2) ", "- ")
        q = re.sub(r"^\d+\.\s*|\d+\)\s*|- ", "", q).strip()
        if q:  # Ensure non-empty questions
            cleaned.append(q)
    return cleaned

# Function to generate interview questions
def generate_interview_questions(job_role, num_questions=5):
    prompt = f"Generate {num_questions} interview questions for a {job_role} role."
<<<<<<< HEAD
    model = genai.GenerativeModel("models/gemini-2.5-flash")
=======
    model = genai.GenerativeModel("models/gemini-1.5-pro")
>>>>>>> f9f69028bc289077f2fdba004522fcd615b36afd
    response = model.generate_content(prompt)

    # Extract text response and clean questions
    if response and hasattr(response, 'text'):
        raw_questions = response.text.strip().split("\n")
        return clean_questions(raw_questions)
    else:
        return ["Error: No response from AI model"]

# Main execution
if __name__ == "__main__":
    job_role = input("Enter job role: ")
    questions = generate_interview_questions(job_role)

    print("\nGenerated Interview Questions:")
    for i, question in enumerate(questions, 1):
        print(f"{i}. {question}")  # Correct numbering

        # Get user response
        answer = input("\nYour Answer: ")

        # Analyze answer using answer_analysis.py
        analysis = analyze_answer(answer)

        # Display feedback
        print("\n📊 **AI Feedback:**")
        print(f"✅ Feedback: {analysis['feedback']}")
        print(f"📝 Grammar Errors: {analysis['grammar_errors']}")
        print(f"📉 Readability Score: {analysis['readability_score']:.2f}")
        print(f"😊 Sentiment Score: {analysis['sentiment_score']:.2f}\n")
