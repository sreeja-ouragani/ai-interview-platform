import spacy

nlp = spacy.load("en_core_web_sm")

def analyze_resume(resume_text, jd_text):
    resume_tokens = set([t.text.lower() for t in nlp(resume_text) if t.is_alpha])
    jd_tokens = set([t.text.lower() for t in nlp(jd_text) if t.is_alpha])

    matched = resume_tokens & jd_tokens
    ats_score = int((len(matched) / max(len(jd_tokens), 1)) * 100)

    skill_gaps = list(jd_tokens - resume_tokens)

    return {
        "ats_score": ats_score,
        "skill_gaps": skill_gaps[:5]
    }
