from django.db import models

class Resume(models.Model):
    resume_text = models.TextField() #store resume text
    category = models.CharField(max_length= 100) #store job cat

    
    def __str__(self):
        return self.category
