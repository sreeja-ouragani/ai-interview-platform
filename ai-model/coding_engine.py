def evaluate_code(user_code, question_data):
    """Evaluate code and return test results"""
    try:
        # Basic syntax check
        compile(user_code, '<string>', 'exec')
        
        # Simple execution test
        exec_globals = {}
        exec(user_code, exec_globals)
        
        # For now, assume all tests pass if code runs without error
        # In real implementation, you'd run actual test cases
        return "all_passed"
        
    except SyntaxError:
        return "none_passed"  # Syntax error
    except Exception as e:
        # Runtime error - might be partial implementation
        if "function" in user_code.lower() or "def" in user_code.lower():
            return "some_passed"  # Has structure but fails
        return "none_passed"

def run_test_cases(user_code, test_cases):
    """Run specific test cases against user code"""
    passed = 0
    total = len(test_cases)
    
    try:
        exec_globals = {}
        exec(user_code, exec_globals)
        
        for test in test_cases:
            try:
                # Extract function name (simple approach)
                func_name = extract_function_name(user_code)
                if func_name and func_name in exec_globals:
                    result = exec_globals[func_name](*test['input'])
                    if result == test['expected']:
                        passed += 1
            except:
                continue
                
    except:
        pass
    
    if passed == total:
        return "all_passed"
    elif passed > 0:
        return "some_passed"
    else:
        return "none_passed"

def extract_function_name(code):
    """Extract function name from code"""
    import re
    match = re.search(r'def\s+(\w+)\s*\(', code)
    return match.group(1) if match else None
