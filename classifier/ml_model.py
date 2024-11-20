import os
import sys

#add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_classification.settings')

import django
django.setup()

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from classifier.models import Resume
import pickle

#load the dataset
def load_data():
    resumes = Resume.objects.all()

    data = {'Resume_str': [], 'Category': []}
    for resume in resumes:
        data['Resume_str'].append(resume.resume_text)
        data['Category'].append(resume.category)

    return data


#preprocess the data
def preprocess_data(data):
    X = data['Resume_str'] 
    y = data['Category']  
    return X, y

#train the model
def train_model():
    data = load_data()
    X, y = preprocess_data(data)

    #convert text to numerical features using TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    X_tfidf = vectorizer.fit_transform(X)

    #split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)

    #train a naive bayes classifier
    model = MultinomialNB()
    model.fit(X_train, y_train)

    #evaluate the model
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred, zero_division=0))

    #save the model and vectorizer for later use
    with open('classifier/model.pkl', 'wb') as model_file:
        pickle.dump(model, model_file)
    with open('classifier/vectorizer.pkl', 'wb') as vectorizer_file:
        pickle.dump(vectorizer, vectorizer_file)

    print("Model and vectorizer saved successfully!")

#run the training process if this script is executed directly
if __name__ == "__main__":
    train_model()
