"""
Offline mode for testing without API limits
"""

# Pre-defined questions and answers for testing
TECHNICAL_QUESTIONS = {
    "ai": [
        {
            "question": "What is the difference between supervised and unsupervised learning?",
            "expected_keywords": ["labeled data", "training", "classification", "clustering", "regression"]
        },
        {
            "question": "Explain how neural networks work.",
            "expected_keywords": ["neurons", "weights", "activation", "backpropagation", "layers"]
        },
        {
            "question": "What is overfitting and how do you prevent it?",
            "expected_keywords": ["generalization", "validation", "regularization", "dropout", "cross-validation"]
        }
    ],
    "python": [
        {
            "question": "What are Python decorators?",
            "expected_keywords": ["function", "wrapper", "@", "modify", "behavior"]
        },
        {
            "question": "Explain list comprehension in Python.",
            "expected_keywords": ["syntax", "loop", "condition", "efficient", "readable"]
        }
    ],
    "general": [
        {
            "question": "What is machine learning?",
            "expected_keywords": ["algorithms", "data", "patterns", "predictions", "learning"]
        }
    ]
}

CODING_QUESTIONS = [
    {
        "question": "Write a function to check if a number is prime.",
        "test_cases": [
            {"input": [7], "expected": True},
            {"input": [4], "expected": False}
        ]
    },
    {
        "question": "Write a function to reverse a string.",
        "test_cases": [
            {"input": ["hello"], "expected": "olleh"},
            {"input": ["python"], "expected": "nohtyp"}
        ]
    }
]

HR_QUESTIONS = [
    "Tell me about yourself.",
    "Why do you want this job?",
    "What are your strengths and weaknesses?",
    "Where do you see yourself in 5 years?"
]

def get_offline_technical_questions(job_desc, skill_gaps=None, n=3):
    """Get pre-defined technical questions"""
    # Simple keyword matching to select relevant questions
    job_lower = job_desc.lower()
    
    if "ai" in job_lower or "ml" in job_lower or "machine learning" in job_lower:
        return TECHNICAL_QUESTIONS["ai"][:n]
    elif "python" in job_lower:
        return TECHNICAL_QUESTIONS["python"][:n]
    else:
        return TECHNICAL_QUESTIONS["general"][:n]

def get_offline_coding_question():
    """Get pre-defined coding question"""
    import random
    return random.choice(CODING_QUESTIONS)

def get_offline_hr_question():
    """Get pre-defined HR question"""
    import random
    return random.choice(HR_QUESTIONS)

def evaluate_answer_offline(answer, expected_keywords):
    """Simple offline answer evaluation"""
    answer_lower = answer.lower().strip()
    
    # Check for obvious wrong indicators
    wrong_indicators = ["i don't know", "not sure", "no idea", "idk", "dunno"]
    if any(indicator in answer_lower for indicator in wrong_indicators):
        return "wrong"
    
    # Check length
    if len(answer_lower) < 10:
        return "wrong"
    
    # Check keyword matching
    if not expected_keywords:
        return "partial"
    
    matched = sum(1 for keyword in expected_keywords if keyword.lower() in answer_lower)
    
    if matched >= len(expected_keywords) * 0.7:
        return "correct"
    elif matched >= len(expected_keywords) * 0.3:
        return "partial"
    else:
        return "wrong"