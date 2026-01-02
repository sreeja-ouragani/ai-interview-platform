from typing import Dict, List

class MCQEvaluator:
    """Evaluate Multiple Choice Questions"""
    
    @staticmethod
    def evaluate_mcq(question: Dict, user_answer: str) -> Dict:
        """
        Evaluate a single MCQ
        
        Args:
            question: Question dict with 'correct_answer' key
            user_answer: User's selected answer
        
        Returns:
            Evaluation result with score and feedback
        """
        correct_answer = question.get('correct_answer', '').strip().upper()
        user_answer = user_answer.strip().upper()
        
        is_correct = user_answer == correct_answer
        
        return {
            'is_correct': is_correct,
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'score': 1 if is_correct else 0,
            'explanation': question.get('explanation', 'No explanation available')
        }
    
    @staticmethod
    def evaluate_mcq_set(questions: List[Dict], user_answers: Dict[str, str]) -> Dict:
        """
        Evaluate a set of MCQs
        
        Args:
            questions: List of question dicts with IDs
            user_answers: Dict mapping question_id to user's answer
        
        Returns:
            Overall evaluation with score and breakdown
        """
        total_questions = len(questions)
        correct_count = 0
        results = []
        
        for question in questions:
            question_id = question.get('id')
            user_answer = user_answers.get(question_id, '')
            
            result = MCQEvaluator.evaluate_mcq(question, user_answer)
            result['question_id'] = question_id
            result['question_text'] = question.get('question', '')
            
            if result['is_correct']:
                correct_count += 1
            
            results.append(result)
        
        score_percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
        
        return {
            'total_questions': total_questions,
            'correct_answers': correct_count,
            'incorrect_answers': total_questions - correct_count,
            'score_percentage': round(score_percentage, 2),
            'results': results
        }
    
    @staticmethod
    def get_performance_analysis(evaluation_result: Dict) -> Dict:
        """
        Analyze performance on MCQ set
        
        Args:
            evaluation_result: Result from evaluate_mcq_set
        
        Returns:
            Performance analysis
        """
        score = evaluation_result['score_percentage']
        
        if score >= 80:
            performance_level = 'Excellent'
            feedback = 'Outstanding performance! You have a strong grasp of the concepts.'
        elif score >= 60:
            performance_level = 'Good'
            feedback = 'Good job! Review the incorrect answers to improve further.'
        elif score >= 40:
            performance_level = 'Average'
            feedback = 'Decent attempt. Focus on strengthening your weak areas.'
        else:
            performance_level = 'Needs Improvement'
            feedback = 'Keep practicing! Review the concepts and try again.'
        
        # Identify weak topics
        weak_topics = []
        for result in evaluation_result['results']:
            if not result['is_correct']:
                # You can add topic categorization here
                weak_topics.append(result['question_id'])
        
        return {
            'performance_level': performance_level,
            'feedback': feedback,
            'weak_questions': weak_topics,
            'score': score
        }
