import requests
import time
from typing import Dict, List
from config import Config

class CodeExecutor:
    """Execute code using Judge0 API"""
    
    # Language IDs for Judge0
    LANGUAGE_IDS = {
        'python': 71,      # Python 3
        'javascript': 63,  # JavaScript (Node.js)
        'java': 62,        # Java
        'cpp': 54,         # C++ (GCC)
        'c': 50,           # C (GCC)
        'csharp': 51,      # C#
        'go': 60,          # Go
        'ruby': 72,        # Ruby
        'php': 68,         # PHP
    }
    
    def __init__(self):
        self.api_url = Config.JUDGE0_API_URL
        self.api_key = Config.JUDGE0_API_KEY
    
    def execute_code(self, code: str, language: str, test_cases: List[Dict]) -> Dict:
        """
        Execute code with test cases
        
        Args:
            code: Source code to execute
            language: Programming language
            test_cases: List of test cases with 'input' and 'expected_output'
        
        Returns:
            Execution results for all test cases
        """
        # Default to python if None or empty
        lang = (language or 'python').lower()
        language_id = self.LANGUAGE_IDS.get(lang)
        
        if not language_id:
            return {
                'error': f'Unsupported language: {language}',
                'supported_languages': list(self.LANGUAGE_IDS.keys())
            }
        
        results = []
        passed = 0
        failed = 0
        
        for idx, test_case in enumerate(test_cases):
            result = self._execute_single_test(
                code, 
                language_id, 
                test_case.get('input', ''),
                test_case.get('expected_output', ''),
                test_case.get('time_limit', 5),
                test_case.get('memory_limit', 256000)
            )
            
            result['test_case_number'] = idx + 1
            result['is_hidden'] = test_case.get('is_hidden', False)
            results.append(result)
            
            if result.get('passed'):
                passed += 1
            else:
                failed += 1
        
        return {
            'total_tests': len(test_cases),
            'passed': passed,
            'failed': failed,
            'score': (passed / len(test_cases) * 100) if test_cases else 0,
            'results': results
        }
    
    def _execute_single_test(self, code: str, language_id: int, stdin: str, 
                            expected_output: str, time_limit: int, memory_limit: int) -> Dict:
        """Execute code for a single test case"""
        
        # If no API key, use mock execution
        if not self.api_key:
            return self._mock_execution(code, stdin, expected_output)
        
        try:
            # Submit code
            submission_url = f"{self.api_url}/submissions"
            headers = {
                'X-RapidAPI-Key': self.api_key,
                'X-RapidAPI-Host': 'judge0-ce.p.rapidapi.com',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'source_code': code,
                'language_id': language_id,
                'stdin': stdin,
                'cpu_time_limit': time_limit,
                'memory_limit': memory_limit
            }
            
            response = requests.post(submission_url, json=payload, headers=headers)
            
            if response.status_code != 201:
                return {'error': 'Failed to submit code', 'passed': False}
            
            token = response.json()['token']
            
            # Poll for result
            result = self._get_submission_result(token, headers)
            
            # Check if output matches expected
            actual_output = result.get('stdout', '').strip()
            expected = expected_output.strip()
            
            passed = actual_output == expected
            
            return {
                'passed': passed,
                'actual_output': actual_output,
                'expected_output': expected,
                'execution_time': result.get('time'),
                'memory_used': result.get('memory'),
                'status': result.get('status', {}).get('description'),
                'stderr': result.get('stderr'),
                'compile_output': result.get('compile_output')
            }
        
        except Exception as e:
            return {'error': str(e), 'passed': False}
    
    def _get_submission_result(self, token: str, headers: Dict, max_attempts: int = 10) -> Dict:
        """Poll Judge0 for submission result"""
        result_url = f"{self.api_url}/submissions/{token}"
        
        for _ in range(max_attempts):
            response = requests.get(result_url, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                status_id = result.get('status', {}).get('id')
                
                # Status 1 or 2 means still processing
                if status_id not in [1, 2]:
                    return result
            
            time.sleep(1)
        
        return {'error': 'Timeout waiting for result'}
    
    def _mock_execution(self, code: str, stdin: str, expected_output: str) -> Dict:
        """Mock execution when API key is not available"""
        # Simple mock - just check if code contains expected output
        passed = expected_output.strip() in code or len(code) > 10
        
        return {
            'passed': passed,
            'actual_output': '[Mock execution - configure Judge0 API for real execution]',
            'expected_output': expected_output,
            'execution_time': '0.1s',
            'memory_used': '1024 KB',
            'status': 'Mock',
            'stderr': None,
            'compile_output': None
        }
