import os
import sys
import pickle
import subprocess
from django.http import JsonResponse
import json
import csv
from django.http import JsonResponse
from django.shortcuts import render
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_model import predict_top_5_resume
from populate_database import populate_database
from .models import PredictionLog

version =  "1.0.0"

def home(request):
    return render(request, "home.html")

def classify_resume(request):
    if request.method == 'POST':
        resume_text = request.POST.get('resumeStr', '')
        if resume_text:
            predictions = predict_top_5_resume(resume_text, version)
            if predictions:
                PredictionLog.objects.create(
                    resume_text=resume_text,
                    prediction_result=", ".join(predictions)
                )
            return JsonResponse({'predictions': predictions})
    return JsonResponse({'predictions': []})




def fetch_all_models(request):
    try:
        # Get the current working directory using pwd, then append 'classifier/models'
        current_directory = os.getcwd()  # Get current working directory (pwd)
        models_directory = os.path.join(current_directory, 'classifier', 'model')  # Path to the models folder
        # List all files in the directory


        highest_version_file = subprocess.check_output(["./find_highest_version.sh"], text=True).strip()
        model_files_restof = []
  
        
        for filename in os.listdir(models_directory):
            file_path = os.path.join(models_directory, filename)
            if os.path.isfile(file_path):  # Only add files, not subdirectories
                model_files_restof.append(filename[:-4])# Append file name to list
        print(model_files_restof)
        return JsonResponse({"success": True, 'output': {"highest_version_file": highest_version_file, "model_files_restof": sorted(model_files_restof)}})

    except Exception as e:
        return JsonResponse({"success": False, 'error': str(e)})




def fetch_latest_model(request):
    if request.method == "GET":
        try:
            # Execute the script to find the highest version
            result = subprocess.check_output(["./find_highest_version.sh"], text=True).strip()

            return JsonResponse({"success": True, "output": result})
        except subprocess.CalledProcessError as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request"})
          

    

def train_command(request):
    if request.method == "POST":
        try:
            body_unicode = request.body.decode('utf-8')  # Decode byte stream
            body = json.loads(body_unicode)  # Parse JSON into dictionary
            print(body)
            
            version = '.'.join(body)

           # Execute the command
            result = subprocess.check_output(['python', 'ml_model.py', 'train', '--version', version], text=True)

           
            return JsonResponse({"success": True, "output": result})
        except subprocess.CalledProcessError as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request"})


def evaluate_command(request):
    if request.method == "POST":
        try:
            body_unicode = request.body.decode('utf-8')  # Decode byte stream
            body = json.loads(body_unicode)  # Parse JSON into dictionary

           # Execute the command
            result = subprocess.check_output(['python', 'ml_model.py', 'evaluate', '--version', body], text=True)
           
            # Apply regex to find "Accuracy:.*"
            match = re.search(r'Accuracy:.*', result)
            output = ""
            if match:
                output = match.group(0)
            else:
                output = "Accuracy not found in result"

            return JsonResponse({"success": True, "output": output})
        except subprocess.CalledProcessError as e:
            return JsonResponse({"success": False, "error": str(e)})
        except Exception as e:
            return JsonResponse({"success": False, "error": "Invalid request: " + str(e)})

def sys_vers_select_command(request):
    if request.method == "POST":
        try:
            body_unicode = request.body.decode('utf-8')  # Decode byte stream
            body = json.loads(body_unicode)  # Parse JSON into dictionary

            global version
            version = body
            print(version)

            return JsonResponse({"success": True})
        except subprocess.CalledProcessError as e:
            return JsonResponse({"success": False, "error": str(e)})
        except Exception as e:
            return JsonResponse({"success": False, "error": "Invalid request: " + str(e)})



def upload_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')

        if not csv_file:
            return JsonResponse({'status': 'error', 'message': 'No file uploaded.'})

        if not csv_file.name.endswith('.csv'):
            return JsonResponse({'status': 'error', 'message': 'Uploaded file is not a CSV.'})

        try:
            resume_csv_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'classifier/data',
                'Resume.csv'
            )

            with open(resume_csv_path, 'r', encoding='utf-8-sig') as resume_csv:
                resume_reader = csv.reader(resume_csv)
                existing_categories = {row[1].strip() for row in resume_reader if len(row) == 2}

            decoded_file = csv_file.read().decode('utf-8').splitlines()
            csv_reader = csv.reader(decoded_file)

            processed_data = []

            for row in csv_reader:
                if len(row) != 2:
                    continue

                category = row[1].strip()
                if category in existing_categories:
                    processed_data.append(row)

            data_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'classifier/data')
            existing_files = [f for f in os.listdir(data_folder) if f.startswith('Resume') and f.endswith('.csv')]

            numbers = []
            for file in existing_files:
                try:
                    number = int(file.replace('Resume', '').replace('.csv', ''))
                    numbers.append(number)
                except ValueError:
                    continue

            next_number = max(numbers, default=0) + 1
            new_csv_filename = f"Resume{next_number}.csv"
            new_csv_path = os.path.join(data_folder, new_csv_filename)

            if processed_data:
                with open(new_csv_path, 'w', newline='', encoding='utf-8-sig') as new_csv_file:
                    writer = csv.writer(new_csv_file)
                    writer.writerows(processed_data)

                populate_database(new_csv_filename)

                return JsonResponse({
                    'status': 'success',
                    'message': f'CSV processed successfully! {len(processed_data)} new rows added.'
                })

            return JsonResponse({'status': 'warning', 'message': 'No valid rows to add. Check categories.'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error: {str(e)}'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
