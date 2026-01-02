from difflib import SequenceMatcher
import re
from typing import List, Dict

class PlagiarismDetector:
    """Rule-based code plagiarism detection (No AI)"""
    
    @staticmethod
    def calculate_similarity(code1: str, code2: str) -> float:
        """
        Calculate similarity between two code snippets
        Returns similarity score between 0 and 1
        """
        # Normalize code (remove whitespace, comments)
        normalized1 = PlagiarismDetector._normalize_code(code1)
        normalized2 = PlagiarismDetector._normalize_code(code2)
        
        # Calculate similarity using SequenceMatcher
        similarity = SequenceMatcher(None, normalized1, normalized2).ratio()
        return similarity
    
    @staticmethod
    def _normalize_code(code: str) -> str:
        """Normalize code by removing comments and extra whitespace"""
        # Remove single-line comments
        code = re.sub(r'//.*?$', '', code, flags=re.MULTILINE)
        code = re.sub(r'#.*?$', '', code, flags=re.MULTILINE)
        
        # Remove multi-line comments
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        code = re.sub(r'""".*?"""', '', code, flags=re.DOTALL)
        code = re.sub(r"'''.*?'''", '', code, flags=re.DOTALL)
        
        # Remove extra whitespace
        code = re.sub(r'\s+', ' ', code)
        
        return code.strip().lower()
    
    @staticmethod
    def check_plagiarism(submitted_code: str, reference_codes: List[str], threshold: float = 0.85) -> Dict:
        """
        Check if submitted code is plagiarized
        
        Args:
            submitted_code: Code submitted by user
            reference_codes: List of reference codes to check against
            threshold: Similarity threshold (0-1) for plagiarism detection
        
        Returns:
            Dictionary with plagiarism detection results
        """
        max_similarity = 0.0
        matched_index = -1
        
        for idx, ref_code in enumerate(reference_codes):
            similarity = PlagiarismDetector.calculate_similarity(submitted_code, ref_code)
            if similarity > max_similarity:
                max_similarity = similarity
                matched_index = idx
        
        is_plagiarized = max_similarity >= threshold
        
        result = {
            'is_plagiarized': is_plagiarized,
            'max_similarity': round(max_similarity * 100, 2),
            'threshold': threshold * 100,
            'matched_index': matched_index if is_plagiarized else None,
            'status': 'PLAGIARIZED' if is_plagiarized else 'ORIGINAL'
        }
        
        return result
    
    @staticmethod
    def detect_common_patterns(code: str) -> Dict:
        """
        Detect if code contains common copy-paste patterns
        """
        patterns = {
            'has_todo_comments': bool(re.search(r'TODO|FIXME|HACK', code, re.IGNORECASE)),
            'has_placeholder_names': bool(re.search(r'\bfoo\b|\bbar\b|\btest\b|\btemp\b', code, re.IGNORECASE)),
            'has_debug_prints': bool(re.search(r'print\(|console\.log\(|System\.out\.println', code)),
            'code_length': len(code),
            'line_count': len(code.split('\n'))
        }
        
        # Calculate suspicion score
        suspicion_score = 0
        if patterns['has_todo_comments']:
            suspicion_score += 20
        if patterns['has_placeholder_names']:
            suspicion_score += 30
        if patterns['has_debug_prints']:
            suspicion_score += 10
        
        patterns['suspicion_score'] = suspicion_score
        patterns['is_suspicious'] = suspicion_score > 30
        
        return patterns
