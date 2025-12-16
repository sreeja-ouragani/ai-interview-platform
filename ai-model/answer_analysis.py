import spacy
import nltk
from textblob import TextBlob
from nltk.tokenize import word_tokenize
from nltk.corpus import cmudict
from smart_feedback import generate_smart_feedback

# Load SpaCy English model
nlp = spacy.load("en_core_web_sm")

# Download necessary NLTK resources
nltk.download("punkt")
nltk.download("cmudict")

# Load CMU Pronouncing Dictionary
cmu_dict = cmudict.dict()

# Function to evaluate answer quality
def analyze_answer(answer, expected_keywords=None, question=""):
    doc = nlp(answer)
    blob = TextBlob(answer)

    # Check for grammar errors (Detect unnecessary interjections like "uh", "um")
    grammar_errors = sum(1 for token in doc if token.tag_ == "UH")

    # Sentiment analysis
    sentiment_score = blob.sentiment.polarity  # -1 (negative) to 1 (positive)

    # Readability Score (Flesch-Kincaid formula)
    words = word_tokenize(answer)
    num_words = len(words)
    num_sentences = max(1, answer.count('.') + answer.count('!') + answer.count('?'))

    # Calculate syllables using CMU Dictionary
    syllables = sum(len([y for y in x if y.isdigit()]) for x in [cmu_dict.get(w.lower(), [['0']])[0] for w in words])

    flesch_score = 206.835 - 1.015 * (num_words / num_sentences) - 84.6 * (syllables / max(1, num_words))

    # AI-powered correctness evaluation
    correctness = evaluate_correctness(answer, expected_keywords, question)
    
    # Logic building score (clarity + structure)
    logic_score = calculate_logic_score(answer, flesch_score, grammar_errors)

    # Generate intelligent feedback based on correctness
    feedback = generate_smart_feedback(answer, correctness, grammar_errors, sentiment_score)

    return {
        "feedback": feedback,
        "correctness": correctness,
        "logic_score": logic_score,
        "sentiment_score": sentiment_score,
        "grammar_errors": grammar_errors,
        "readability_score": flesch_score
    }

def evaluate_correctness(answer, expected_keywords, question=""):
    """AI-powered evaluation of answer correctness with offline fallback"""
    from offline_mode import evaluate_answer_offline
    
    # Check for obviously wrong answers first
    wrong_indicators = [
        "i don't know", "not sure", "no idea", "don't understand",
        "idk", "dunno", "maybe", "i think maybe", "probably not",
        "i'm not certain", "unclear", "confused"
    ]
    
    answer_lower = answer.lower().strip()
    
    # If answer is too short or contains wrong indicators
    if len(answer_lower) < 10 or any(indicator in answer_lower for indicator in wrong_indicators):
        return "wrong"
    
    # Try AI evaluation first, fallback to offline if API fails
    try:
        import google.generativeai as genai
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        
        prompt = f"""
        Evaluate this technical interview answer:
        
        Question: {question}
        Expected concepts: {', '.join(expected_keywords) if expected_keywords else 'General technical knowledge'}
        Student Answer: {answer}
        
        Rate the answer as:
        - CORRECT: Answer demonstrates clear understanding and covers key concepts
        - PARTIAL: Answer shows some understanding but missing important details
        - WRONG: Answer is incorrect, irrelevant, or shows no understanding
        
        Respond with only: CORRECT, PARTIAL, or WRONG
        """
        
        ai_response = model.generate_content(prompt).text.strip().upper()
        if "CORRECT" in ai_response:
            return "correct"
        elif "PARTIAL" in ai_response:
            return "partial"
        else:
            return "wrong"
            
    except Exception as e:
        # Use offline evaluation when API fails
        return evaluate_answer_offline(answer, expected_keywords)

def calculate_logic_score(answer, readability_score, grammar_errors):
    """Calculate logic building score based on clarity and structure"""
    # Base score from readability (0-10 scale)
    base_score = min(10, max(0, (readability_score - 30) / 10))
    
    # Penalty for grammar errors
    grammar_penalty = min(5, grammar_errors)
    
    # Structure bonus (check for logical connectors)
    connectors = ["because", "therefore", "however", "moreover", "furthermore", "consequently"]
    structure_bonus = min(3, sum(1 for conn in connectors if conn in answer.lower()))
    
    final_score = max(0, base_score - grammar_penalty + structure_bonus)
    return int(final_score)

# Example usage
if __name__ == "__main__":
    answer = input("Enter your interview answer: ")
    print(analyze_answer(answer))
