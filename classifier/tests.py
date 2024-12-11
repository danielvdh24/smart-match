from django.test import TestCase
from django.urls import reverse

#USER UI TESTS

class ResumeInputTests(TestCase):
    def test_valid_resume_submission(self):
        #simulate submitting a reusme 
        response = self.client.post(reverse('classify_resume'), {
            'resumeStr': "Experienced accountant skilled in money."
        })
        #check if the form submission is successful
        self.assertEqual(response.status_code, 200)
        #decode the response content
        content = response.content.decode()
        #check to see if the output contains 5 job titles
        job_titles = content.count("<li>")
        self.assertEqual(job_titles, 5)

class ResumeFormValidationTests(TestCase):
    def test_resume_field_is_required(self):
        #fetching the form page
        response = self.client.get(reverse('Home'))
        self.assertEqual(response.status_code, 200)
        #check that the textarea field has the 'required' attribute
        content = response.content.decode()
        self.assertIn('required', content)
        self.assertIn('name="resumeStr"', content)


#ADMIN UI TESTS