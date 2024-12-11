from django.test import TestCase
from ml_model import predict_top_5_resume
from classifier.models import Resume

class TestPredictTop5Resume(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.resumes = [
            {"resume_text": "Experienced software engineer with knowledge in Java, Python, and algorithms.", "category": "Python Developer"},
            {"resume_text": "Data analyst skilled in SQL and Tableau.", "category": "Data Science"},
            {"resume_text": "Marketing specialist with expertise in SEO and content strategy.", "category": "Marketing"}
        ]
        for resume_data in cls.resumes:
            Resume.objects.create(**resume_data)

    def test_predict_top_5_resume(self):
        resume_text = "Highly experienced data scientist with a background in machine learning, AI, and big data."
        top_5_predictions = predict_top_5_resume(resume_text=resume_text, version="1.0.0")
        print("Top 5 Predictions:", top_5_predictions)
        self.assertTrue(any("DATA SCIENCE" in prediction for prediction in top_5_predictions))
        self.assertTrue(any("PYTHON DEVELOPER" in prediction for prediction in top_5_predictions))
