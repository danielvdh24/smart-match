from django.test import TestCase
from ml_model import evaluate_model

class TestEvaluateModel(TestCase):
    def test_evaluate_model(self):
        try:
            evaluate_model(version="1.0.0")
        except Exception as e:
            self.fail(f"Model evaluation failed: {e}")
