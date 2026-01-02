from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from config import Config
from typing import List, Dict, Optional

class MistralService:
    """Service for interacting with Mistral AI API"""
    
    def __init__(self):
        # Strip whitespace from API key to avoid authentication errors
        api_key = Config.MISTRAL_API_KEY.strip() if Config.MISTRAL_API_KEY else ""
        self.client = MistralClient(api_key=api_key)
        self.model = Config.MISTRAL_MODEL
    
    def generate_response(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """
        Generate a response from Mistral AI
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0.0 to 1.0)
        
        Returns:
            Generated response text
        """
        try:
            chat_messages = [
                ChatMessage(role=msg['role'], content=msg['content'])
                for msg in messages
            ]
            
            response = self.client.chat(
                model=self.model,
                messages=chat_messages,
                temperature=temperature
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"Error calling Mistral API: {e}")
            return f"Error: {str(e)}"
    
    def extract_skills_from_resume(self, resume_text: str) -> Dict:
        """
        Extract skills from resume text using Mistral AI
        
        Args:
            resume_text: The text content of the resume
        
        Returns:
            Dictionary with extracted skills and analysis
        """
        prompt = f"""Analyze the following resume and extract details.
Resume Text:
{resume_text}

Provide the response in STRICT JSON format with the following keys and structure:
{{
    "technical_skills": ["skill1", "skill2"],
    "soft_skills": ["skill1", "skill2"],
    "domain_expertise": ["area1", "area2"],
    "experience_years": "X years",
    "skill_level": "Fresher/Junior/Mid/Senior"
}}
Ensure technical_skills and soft_skills are arrays of strings."""
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        response = self.generate_response(messages, temperature=0.1)
        
        try:
            import json
            # Extract JSON from potential markdown blocks
            clean_response = response.replace('```json', '').replace('```', '').strip()
            start_idx = clean_response.find('{')
            end_idx = clean_response.rfind('}') + 1
            if start_idx != -1:
                json_str = clean_response[start_idx:end_idx]
                return json.loads(json_str)
            return {"raw_analysis": response}
        except:
            return {"raw_analysis": response}
    
    def match_resume_to_job(self, resume_skills: Dict, job_description: str) -> Dict:
        """
        Match resume skills to job description
        """
        prompt = f"""Compare the candidate's skills with the job requirements.
Candidate Skills: {resume_skills}
Job Description: {job_description}

Provide response in STRICT JSON format:
{{
    "match_score": 75,
    "missing_skills": ["skillA", "skillB"],
    "matching_skills": ["skillC", "skillD"],
    "recommendations": ["Do X", "Learn Y"]
}}
IMPORTANT: missing_skills must be a LIST of specific skill names (e.g. 'React', 'Docker') that are required but missing.
103: Do NOT list skills if the candidate has a functional equivalent (e.g., if JD asks for 'AWS' and candidate has 'Azure', or if JD asks for 'Cloud' and candidate has 'AWS', do NOT list it as missing).
104: Do NOT list 'System Design' or 'Cloud Architecture' as missing unless the candidate is Senior level or specifically claims to be an architect.
105: Do NOT just say 'technical_skills'."""
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        response = self.generate_response(messages, temperature=0.1)
        
        try:
            import json
            clean_response = response.replace('```json', '').replace('```', '').strip()
            start_idx = clean_response.find('{')
            end_idx = clean_response.rfind('}') + 1
            if start_idx != -1:
                json_str = clean_response[start_idx:end_idx]
                return json.loads(json_str)
            return {"raw_analysis": response}
        except:
            return {"raw_analysis": response}

    def analyze_introduction(self, intro_text: str) -> Dict:
        """
        Analyze candidate's self-introduction
        """
        prompt = f"""Analyze the following self-introduction from a job candidate.
Introduction: "{intro_text}"

Extract the following in STRICT JSON format:
{{
    "spoken_skills": ["skill1", "skill2"],
    "experience_summary": "Brief summary...",
    "key_projects": ["project1", "project2"],
    "confidence_level": "High/Medium/Low"
}}
Ensure spoken_skills is a list of strings."""
        
        messages = [{"role": "user", "content": prompt}]
        response = self.generate_response(messages, temperature=0.2)
        
        try:
            import json
            clean_response = response.replace('```json', '').replace('```', '').strip()
            start_idx = clean_response.find('{')
            end_idx = clean_response.rfind('}') + 1
            if start_idx != -1:
                return json.loads(clean_response[start_idx:end_idx])
            return {"raw_analysis": response}
        except:
            return {"raw_analysis": response}
    
    def generate_hr_question(self, context: Dict, conversation_history: List[Dict] = None, tone: str = 'friendly') -> str:
        """
        Generate HR interview question based on context with tone variation
        
        Args:
            context: User profile and interview context
            conversation_history: Previous Q&A in the interview
            tone: Interview tone - 'friendly' or 'strict'
        
        Returns:
            Generated HR question
        """
        history_text = ""
        if conversation_history:
            history_text = "\n".join([
                f"Q: {item['question']}\nA: {item['answer']}"
                for item in conversation_history[-3:]  # Last 3 exchanges
            ])
        
        # Define tone-specific instructions
        tone_instructions = {
            'friendly': "You are a warm, encouraging HR interviewer. Be supportive and conversational. Make the candidate feel comfortable.",
            'strict': "You are a professional, formal HR interviewer. Be direct and thorough. Ask probing follow-up questions."
        }
        
        system_prompt = tone_instructions.get(tone, tone_instructions['friendly'])
        
        prompt = f"""Generate a relevant interview question based on:

Candidate Profile:
- Name: {context.get('name', 'Candidate')}
- Experience Level: {context.get('experience_level', 'Not specified')}
- Target Role: {context.get('target_role', 'Not specified')}

Previous Conversation:
{history_text if history_text else 'This is the start of the interview.'}

INSTRUCTION: 
1. You MUST reference specific details from the Candidate Profile, such as their specific projects, skills from resume, or points mentioned in their intro. 
2. Do NOT be generic. If they know 'React', ask about React. If they mentioned 'hiking' in intro, use it as an icebreaker if appropriate.
3. ADAPT to the conversation history. Do NOT ask questions that are similar to previous ones.
4. BE UNIQUE AND SPECIFIC to this candidate.

Generate ONE short, natural, conversational HR interview question (max 15 words) that strictly relates to their profile/intro.
Do not include any preamble, just the question."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        return self.generate_response(messages, temperature=0.8)
    
    def analyze_hr_response(self, question: str, answer: str, context: Dict) -> Dict:
        """
        Analyze candidate's HR interview response
        
        Args:
            question: The question asked
            answer: Candidate's answer
            context: Interview context
        
        Returns:
            Analysis with score and feedback
        """
        prompt = f"""Analyze this HR interview response:

Question: {question}
Answer: {answer}

Evaluate on:
1. Relevance (0-10)
2. Clarity (0-10)
3. Confidence (0-10)
4. Completeness (0-10)
5. Overall Score (0-100)
6. Strengths
7. Areas for improvement
8. Suggested better answer

Provide response in JSON format. For "score", ensure it is a NUMBER between 0-100.
If "Overall Score" is missing, calculate it as average of 0-10 ratings * 10."""
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        response = self.generate_response(messages, temperature=0.3)
        
        try:
            import json
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
            else:
                return {"raw_analysis": response}
        except:
            return {"raw_analysis": response}
    
    def generate_feedback(self, interview_data: Dict) -> Dict:
        """
        Generate comprehensive feedback for completed interview
        
        Args:
            interview_data: Complete interview session data
        
        Returns:
            Detailed feedback and recommendations
        """
        prompt = f"""Provide comprehensive interview feedback based on:

Interview Performance:
{interview_data}

Generate:
1. Overall performance summary
2. Strengths (list)
3. Weaknesses (list)
4. Specific mistake explanations
5. Industry-standard expected answers
6. Learning resources recommendations (MUST include YouTube search terms or video links)
7. Action plan for improvement

Provide response in JSON format with EXACT keys: "summary", "strengths", "weaknesses", "recommendations", "action_plan". 
Ensure "strengths" and "weaknesses" are simple lists of strings. "recommendations" should contain the YouTube links.
"""
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        response = self.generate_response(messages, temperature=0.5)
        
        try:
            import json
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
            else:
                return {"raw_analysis": response}
        except:
            return {"raw_analysis": response}
    
    def generate_managerial_question(self, context: Dict, conversation_history: List[Dict] = None, tone: str = 'friendly') -> str:
        """
        Generate managerial/behavioral interview question
        
        Args:
            context: User profile and interview context
            conversation_history: Previous Q&A
            tone: Interview tone - 'friendly' or 'strict'
        
        Returns:
            Generated managerial question
        """
        history_text = ""
        if conversation_history:
            history_text = "\n".join([
                f"Q: {item['question']}\nA: {item['answer']}"
                for item in conversation_history[-3:]
            ])
        
        tone_instructions = {
            'friendly': "You are a supportive manager assessing leadership and teamwork skills. Be encouraging.",
            'strict': "You are a senior manager evaluating decision-making and problem-solving. Be challenging."
        }
        
        system_prompt = tone_instructions.get(tone, tone_instructions['friendly'])
        
        prompt = f"""Generate a managerial/behavioral interview question:

Candidate Profile:
- Experience Level: {context.get('experience_level', 'Not specified')}
- Target Role: {context.get('target_role', 'Not specified')}

Previous Conversation:
{history_text if history_text else 'This is the start of the managerial round.'}

Focus on:
- Leadership and team management
- Conflict resolution
- Decision making under pressure
- Project management

INSTRUCTION:
1. You MUST reference specific details from the Candidate Profile (Projects, Experience, or Intro Context). 
2. Ask a behavioral question that forces them to reflect on THEIR specific experiences mentioned in resume/intro.
3. Be specific to their domain (e.g. if Developer, ask about dev conflict; if Sales, ask about client conflict).
4. Ensure the question is DIFFERENT from any previous questions in the history.
5. CONVERSATIONAL HANDLING: If the previous answer was "I don't know", "I'm not sure", or vague:
   - Start by acknowledging it kindly (e.g., "That's completely fine," or "No worries,").
   - Then ask a simpler or different question to help them feel comfortable.

Generate ONE short, concise behavioral/conversational question (max 20 words).
Do not include preamble, just the question."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        return self.generate_response(messages, temperature=0.8)
    
    def generate_learning_path(self, user_skills: Dict, weak_areas: List[str], target_role: str) -> Dict:
        """
        Generate personalized learning path based on skill gaps
        
        Args:
            user_skills: Current user skills
            weak_areas: Identified weak areas
            target_role: Target job role
        
        Returns:
            Structured learning path with resources
        """
        prompt = f"""Create a personalized learning path for:

Current Skills:
{user_skills}

Weak Areas:
{weak_areas}

Target Role: {target_role}

Generate a structured learning path with:
1. Priority skills to learn (ordered by importance)
2. For each skill:
   - Current level (Beginner/Intermediate/Advanced)
   - Target level
   - Estimated time to learn (in hours)
   - Learning resources (courses, books, practice platforms)
   - Milestones to track progress
3. Overall timeline (weeks/months)

Provide response in JSON format with keys: priority_skills, timeline_weeks, milestones"""
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        response = self.generate_response(messages, temperature=0.4)
        
        try:
            import json
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
            else:
                return {"raw_plan": response}
        except:
            return {"raw_plan": response}
    
    def detect_code_plagiarism(self, submitted_code: str, reference_codes: List[str] = None) -> Dict:
        """
        AI-powered plagiarism detection using Mistral AI
        
        Args:
            submitted_code: Code submitted by user
            reference_codes: Optional list of reference codes to compare against
        
        Returns:
            Plagiarism analysis with score and explanation
        """
        prompt = f"""Analyze this code for potential plagiarism and code quality:

Code to analyze:
```
{submitted_code}
```

Analyze and provide:
1. Plagiarism likelihood (0-100 score)
2. Code originality assessment
3. Common patterns detected (e.g., copied from online sources, tutorial code)
4. Code quality indicators
5. Suspicious elements (TODO comments, placeholder names, debug prints)

Provide response in JSON format with keys: plagiarism_score, is_plagiarized (true/false), originality_level, suspicious_patterns, quality_score, explanation
"""
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        response = self.generate_response(messages, temperature=0.3)
        
        try:
            import json
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                result = json.loads(json_str)
                
                # Ensure required fields
                if 'plagiarism_score' not in result:
                    result['plagiarism_score'] = 0
                if 'is_plagiarized' not in result:
                    result['is_plagiarized'] = result.get('plagiarism_score', 0) > 70
                
                return result
            else:
                return {
                    "plagiarism_score": 0,
                    "is_plagiarized": False,
                    "raw_analysis": response
                }
        except:
            return {
                "plagiarism_score": 0,
                "is_plagiarized": False,
                "raw_analysis": response
            }
