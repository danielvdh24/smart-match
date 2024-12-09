import os
import sys
import pickle
from django.shortcuts import render, HttpResponse
import subprocess
from django.http import JsonResponse
import json


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_model import predict_top_5_resume

version =  "1.0.0"

def home(request):
    return render(request, "home.html")

def classify_resume(request):
    predictions = None
    if request.method == 'POST':
        resume_text = request.POST.get('resumeStr', '')
        if resume_text:
            predictions = predict_top_5_resume(resume_text, version)
    return render(request, 'home.html', {'predictions': predictions})

def execute_command(request):
    if request.method == "POST":
        try:
            body_unicode = request.body.decode('utf-8')  # Decode byte stream
            body = json.loads(body_unicode)  # Parse JSON into dictionary
            print(body)
            
            global version
            version = '.'.join(body)

           # Execute the command
            result = subprocess.check_output(['python', 'ml_model.py', 'train', '--version', version], text=True)

           
            return JsonResponse({"success": True, "output": result})
        except subprocess.CalledProcessError as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request"})

