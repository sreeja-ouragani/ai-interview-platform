def generate_smart_feedback(answer, correctness, grammar_errors, sentiment_score):
    """Generate intelligent feedback based on answer quality"""
    answer_lower = answer.lower().strip()
    
    # Check for obvious wrong indicators
    if any(phrase in answer_lower for phrase in ["i don't know", "not sure", "no idea"]):
        return "❌ Wrong answer! You clearly don't understand the concept. Please study this topic."
    
    if correctness == "wrong":
        if len(answer) < 15:
            return "❌ Wrong answer! Your response is too brief and doesn't address the question."
        else:
            return "❌ Wrong answer! Your explanation shows misunderstanding of the concept."
    
    elif correctness == "partial":
        if grammar_errors > 2:
            return "⚠️ Partially correct, but your explanation lacks clarity and has grammar issues."
        else:
            return "⚠️ Partially correct, but you're missing key details. Expand your answer."
    
    else:  # correct
        if sentiment_score > 0.3 and grammar_errors == 0:
            return "✅ Excellent answer! Clear, accurate, and well-explained."
        elif grammar_errors > 0:
            return "✅ Correct answer, but watch your grammar and filler words."
        else:
            return "✅ Good answer! You understand the concept well."