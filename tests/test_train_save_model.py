from django.test import TestCase
import os
from ml_model import train_model
from classifier.models import Resume

class TestTrainSaveModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.resumes = [
            {"resume_text": "Software engineer with 5 years of experience in Python.", "category": "Engineering"},
            {"resume_text": "Data analyst skilled in SQL and Tableau.", "category": "Data Science"},
            {"resume_text": "Marketing specialist with expertise in SEO and content strategy.", "category": "Marketing"}
        ]
        for resume_data in cls.resumes:
            Resume.objects.create(**resume_data)
                   
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        if os.path.exists("classifier/model/model_v1.0.1.pkl"):
            os.remove("classifier/model/model_v1.0.1.pkl")
        if os.path.exists("classifier/vectorizer/vectorizer_v1.0.1.pkl"):
            os.remove("classifier/vectorizer/vectorizer_v1.0.1.pkl")

    def test_train_save_model(self):
        try:
            X_test, y_test, model, vectorizer = train_model(version="1.0.1")
            self.assertTrue(os.path.exists("classifier/model/model_v1.0.1.pkl"))
            self.assertTrue(os.path.exists("classifier/vectorizer/vectorizer_v1.0.1.pkl"))
        except ValueError as e:
            self.fail(f"Training failed: {e}")
