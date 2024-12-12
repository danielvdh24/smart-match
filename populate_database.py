import csv
from classifier.models import Resume

def populate_database(path):
    with open('classifier/data/' + path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile) #read the CSV file
        for row in reader: #iterate through each row
            Resume.objects.create(
                resume_text=row['Resume_str'],
                category=row['Category']
            )
    print(f"Database populated with {path} successfully.")