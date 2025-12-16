from question_generator import generate_hr_question
from textblob import TextBlob
import re

def conduct_hr_interview():
    """Conduct HR interview and return confidence level"""
    question = generate_hr_question()
    print("\nHR Interviewer:", question)
    answer = input("Speak (type simulated): ")
    
    confidence_level = analyze_communication(answer)
    return confidence_level

def analyze_communication(answer):
    """Analyze communication skills and return confidence level"""
    blob = TextBlob(answer)
    sentiment = blob.sentiment.polarity
    
    # Check for confidence indicators
    confidence_words = ["confident", "sure", "definitely", "absolutely", "certainly"]
    hesitation_words = ["um", "uh", "maybe", "i think", "probably", "not sure"]
    
    confidence_count = sum(1 for word in confidence_words if word in answer.lower())
    hesitation_count = sum(1 for word in hesitation_words if word in answer.lower())
    
    # Length and structure analysis
    word_count = len(answer.split())
    has_structure = bool(re.search(r'(first|second|finally|because|therefore)', answer.lower()))
    
    # Calculate confidence level
    score = 0
    
    # Sentiment contribution
    if sentiment > 0.3:
        score += 3
    elif sentiment > 0:
        score += 2
    else:
        score += 1
    
    # Confidence words boost
    score += min(2, confidence_count)
    
    # Hesitation penalty
    score -= min(2, hesitation_count)
    
    # Length and structure bonus
    if word_count > 20 and has_structure:
        score += 2
    elif word_count > 10:
        score += 1
    
    # Determine final level
    if score >= 6:
        return "high"
    elif score >= 3:
        return "average"
    else:
        return "low"

def conduct_multiple_hr_questions(num_questions=3):
    """Conduct multiple HR questions and return average confidence"""
    confidence_levels = []
    
    for i in range(num_questions):
        print(f"\n--- HR Question {i+1} ---")
        level = conduct_hr_interview()
        confidence_levels.append(level)
    
    # Calculate average confidence
    level_scores = {"high": 3, "average": 2, "low": 1}
    avg_score = sum(level_scores[level] for level in confidence_levels) / len(confidence_levels)
    
    if avg_score >= 2.5:
        return "high"
    elif avg_score >= 1.5:
        return "average"
    else:
        return "low"
