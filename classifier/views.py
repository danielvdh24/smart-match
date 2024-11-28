import os
import sys
import pickle
from django.shortcuts import render, HttpResponse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_model import predict_top_5_resume

def home(request):
    return render(request, "home.html")

def classify_resume(request):
    predictions = None
    if request.method == 'POST':
        resume_text = request.POST.get('resumeStr', '')
        if resume_text:
            predictions = predict_top_5_resume(resume_text)
    return render(request, 'home.html', {'predictions': predictions})