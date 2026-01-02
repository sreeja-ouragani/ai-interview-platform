import PyPDF2
import docx
import os
from typing import Optional

class ResumeParser:
    """Parse resume files (PDF, DOCX, TXT)"""
    
    @staticmethod
    def parse_pdf(file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            return ""
    
    @staticmethod
    def parse_docx(file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text.strip()
        except Exception as e:
            print(f"Error parsing DOCX: {e}")
            return ""
    
    @staticmethod
    def parse_txt(file_path: str) -> str:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except Exception as e:
            print(f"Error parsing TXT: {e}")
            return ""
    
    @staticmethod
    def parse_resume(file_path: str) -> Optional[str]:
        """
        Parse resume file based on extension
        
        Args:
            file_path: Path to resume file
        
        Returns:
            Extracted text or None if parsing failed
        """
        if not os.path.exists(file_path):
            return None
        
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.pdf':
            return ResumeParser.parse_pdf(file_path)
        elif ext in ['.docx', '.doc']:
            return ResumeParser.parse_docx(file_path)
        elif ext == '.txt':
            return ResumeParser.parse_txt(file_path)
        else:
            return None
