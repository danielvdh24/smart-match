import csv
from classifier.models import Resume

def populate_database():
    with open('classifier/data/resume.csv', newline = '', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile) #read the csv file
        for row in reader: #iterate through each row 
            Resume.objects.create(
                resume_text=row['Resume_str'],
                category=row['Category']
            )
    print("Databse populated successfully")