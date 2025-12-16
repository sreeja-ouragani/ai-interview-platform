import subprocess
import sys
import spacy

def install_requirements():
    """Install all required packages"""
    print("Installing requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def download_spacy_model():
    """Download SpaCy English model"""
    print("Downloading SpaCy model...")
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])

def setup_nltk():
    """Download NLTK data"""
    print("Setting up NLTK...")
    import nltk
    nltk.download('punkt')
    nltk.download('cmudict')

if __name__ == "__main__":
    try:
        install_requirements()
        download_spacy_model()
        setup_nltk()
        print("✅ Setup complete! You can now run the project.")
    except Exception as e:
        print(f"❌ Setup failed: {e}")