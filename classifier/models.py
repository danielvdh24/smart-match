from django.db import models

class Resume(models.Model):
    resume_text = models.TextField() #store resume text
    category = models.CharField(max_length= 100) #store job cat

    
    def __str__(self):
        return self.category

class PredictionLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)  #set current timestamp
    resume_text = models.TextField()  #store submitted resume text
    prediction_result = models.CharField(max_length=255)  #store predicted categories

    def __str__(self):
        return f"Prediction at {self.timestamp}: {self.prediction_result}"