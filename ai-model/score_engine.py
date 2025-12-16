class ScoreEngine:
    def __init__(self):
        self.technical_knowledge = 0
        self.logic_building = 0
        self.coding_skills = 0
        self.communication = 0
        self.originality = 100  # Start at 100, reduce for plagiarism

    def update_technical(self, correctness):
        if correctness == "correct":
            self.technical_knowledge += 10
        elif correctness == "partial":
            self.technical_knowledge += 5
        # Wrong = +0

    def update_logic(self, clarity_score):
        self.logic_building += clarity_score

    def update_coding(self, test_results):
        if test_results == "all_passed":
            self.coding_skills += 20
        elif test_results == "some_passed":
            self.coding_skills += 10
        # None passed = +0

    def update_communication(self, confidence_level):
        if confidence_level == "high":
            self.communication += 15
        elif confidence_level == "average":
            self.communication += 8
        else:  # low
            self.communication += 3

    def update_originality(self, plagiarism_score):
        # Reduce originality based on plagiarism (0-100 scale)
        self.originality = max(0, 100 - plagiarism_score)

    def final_result(self):
        total = (self.technical_knowledge + self.logic_building + 
                self.coding_skills + self.communication + self.originality)
        
        return {
            "technical_knowledge": self.technical_knowledge,
            "logic_building": self.logic_building,
            "coding_skills": self.coding_skills,
            "communication": self.communication,
            "originality": self.originality,
            "total_score": total,
            "pie_chart": {
                "Technical Knowledge": self.technical_knowledge,
                "Logic Building": self.logic_building,
                "Coding Skills": self.coding_skills,
                "Communication": self.communication,
                "Originality": self.originality
            }
        }
