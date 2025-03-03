import spacy
import nltk
from textblob import TextBlob
from nltk.tokenize import word_tokenize
from nltk.corpus import cmudict

# Load SpaCy English model
nlp = spacy.load("en_core_web_sm")

# Download necessary NLTK resources
nltk.download("punkt")
nltk.download("cmudict")

# Load CMU Pronouncing Dictionary
cmu_dict = cmudict.dict()

# Function to evaluate answer quality
def analyze_answer(answer):
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

    # Generate feedback
    if sentiment_score > 0.2 and grammar_errors == 0:
        feedback = "Great answer! Well structured."
    elif sentiment_score > -0.2:
        feedback = "Decent answer, but could use more details."
    else:
        feedback = "Your answer lacks clarity. Try rewording it."

    return {
        "feedback": feedback,
        "sentiment_score": sentiment_score,
        "grammar_errors": grammar_errors,
        "readability_score": flesch_score
    }

# Example usage
if __name__ == "__main__":
    answer = input("Enter your interview answer: ")
    print(analyze_answer(answer))
