from django.test import TestCase
from ml_model import predict_single_resume
from classifier.models import Resume

class TestPredictSingleResume(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.resumes = [
            {"resume_text": "Experienced software engineer with knowledge in Java, Python, and algorithms.", "category": "Software Engineering"},
            {"resume_text": "Data analyst skilled in SQL and Tableau.", "category": "Data Science"},
            {"resume_text": "Marketing specialist with expertise in SEO and content strategy.", "category": "Marketing"}
        ]
        for resume_data in cls.resumes:
            Resume.objects.create(**resume_data)

    def test_predict_single_resume(self):
        resume_text = "Experienced software engineer with knowledge in Java, Python, and algorithms."
        predicted_category = predict_single_resume(resume_text=resume_text, version="1.0.0")
        expected_categories = ["AI ENGINEERING", "DATA SCIENCE", "MARKETING", "PYTHON-DEVELOPER", "SOFTWARE ENGINEERING"]
        self.assertIn(predicted_category, expected_categories)
