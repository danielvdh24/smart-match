from django.test import TestCase
from classifier.models import Resume

class SetUpClassTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.resume_data = [
            {"resume_text": "Software engineer with 5 years of experience in Python.", "category": "Engineering"},
            {"resume_text": "Data analyst skilled in SQL and Tableau.", "category": "Data Science"},
            {"resume_text": "Marketing specialist with expertise in SEO and content strategy.", "category": "Marketing"}
        ]
        cls.resumes = [Resume.objects.create(**resume) for resume in cls.resume_data]

    def test_resume_data_is_set_up(self):
        self.assertEqual(Resume.objects.count(), len(self.resume_data))
        for resume in Resume.objects.all():
            self.assertTrue(resume.resume_text.strip())
