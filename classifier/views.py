import os
import sys
import csv
from django.http import JsonResponse
from django.contrib.messages import get_messages, add_message
from django.contrib.messages.constants import ERROR, SUCCESS, WARNING
from django.shortcuts import render

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_model import predict_top_5_resume
from populate_database import populate_database

def home(request):
    return render(request, "home.html")

def classify_resume(request):
    predictions = None
    if request.method == 'POST':
        resume_text = request.POST.get('resumeStr', '')
        if resume_text:
            predictions = predict_top_5_resume(resume_text)
    return render(request, 'home.html', {'predictions': predictions})

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