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



#TRAIN AND SAVE THE MODEL


def train_model(version="1.0.0"):
    resumes = Resume.objects.all()
    data = {'Resume_str': [], 'Category': []}
    for resume in resumes:
        data['Resume_str'].append(resume.resume_text)
        data['Category'].append(resume.category)

    X = data['Resume_str']
    y = data['Category']

    #convert text to numerical features using TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    X_tfidf = vectorizer.fit_transform(X)

    #split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)

    #train a naive Bayes classifier
    model = MultinomialNB()
    model.fit(X_train, y_train)

    #save the model and vectorizer with version tags
    model_filename = f"classifier/model/model_v{version}.pkl"
    vectorizer_filename = f"classifier/vectorizer/vectorizer_v{version}.pkl"
    with open(model_filename, 'wb') as model_file:
        pickle.dump(model, model_file)
    with open(vectorizer_filename, 'wb') as vectorizer_file:
        pickle.dump(vectorizer, vectorizer_file)

    print(f"Model and vectorizer saved as version {version}!")
    return X_test, y_test, model, vectorizer  #return test data for evaluation




#EVALUATE A SAVED MODEL ON THE TEST SET


def evaluate_model(version="1.0.0"):
    model_filename = f"classifier/model/model_v{version}.pkl"
    vectorizer_filename = f"classifier/vectorizer/vectorizer_v{version}.pkl"

    if not os.path.exists(model_filename) or not os.path.exists(vectorizer_filename):
        print(f"Model version {version} not found. Please train the model first.")
        return

    #load model and vectorizer
    with open(model_filename, 'rb') as model_file:
        model = pickle.load(model_file)
    with open(vectorizer_filename, 'rb') as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)

    #load data
    resumes = Resume.objects.all()
    data = {'Resume_str': [], 'Category': []}
    for resume in resumes:
        data['Resume_str'].append(resume.resume_text)
        data['Category'].append(resume.category)

    X = data['Resume_str']
    y = data['Category']

    #transform data using the loaded vectorizer
    X_tfidf = vectorizer.transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)

    #evaluate the model
    y_pred = model.predict(X_test)
    print("\nModel Evaluation:")
    print(classification_report(y_test, y_pred, zero_division=0))





#PREDICT THE CATEGORY OF A SINGLE RESUME


def predict_single_resume(resume_text, version="1.0.0"):
    model_filename = f"classifier/model/model_v{version}.pkl"
    vectorizer_filename = f"classifier/vectorizer/vectorizer_v{version}.pkl"

    if not os.path.exists(model_filename) or not os.path.exists(vectorizer_filename):
        print(f"Model version {version} not found. Please train the model first.")
        return None

    #load model and vectorizer
    with open(model_filename, 'rb') as model_file:
        model = pickle.load(model_file)
    with open(vectorizer_filename, 'rb') as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)

    #transform the input resume text
    X_input = vectorizer.transform([resume_text])

    #predict the category
    prediction = model.predict(X_input)
    return prediction[0]




#PREDICT THE TOP 5 CATEGORY OF A SINGLE RESUME


def predict_top_5_resume(resume_text, version="1.0.0"):
    model_filename = f"classifier/model/model_v{version}.pkl"
    vectorizer_filename = f"classifier/vectorizer/vectorizer_v{version}.pkl"

    if not os.path.exists(model_filename) or not os.path.exists(vectorizer_filename):
        print(f"Model version {version} not found. Please train the model first.")
        return None

    #load model and vectorizer
    with open(model_filename, 'rb') as model_file:
        model = pickle.load(model_file)
    with open(vectorizer_filename, 'rb') as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)

    #transform the input resume text
    X_input = vectorizer.transform([resume_text])

    #get the probabilities for each category
    probabilities = model.predict_proba(X_input)[0]
    classes = model.classes_

    #combine classes with their probabilities
    top_5 = sorted(zip(classes, probabilities), key=lambda x: x[1], reverse=True)[:5]

    #format result
    prediction = [
        f"{category.replace('-', ' ')}: {probability * 100:.2f}%"
        for category, probability in top_5
    ]
    return prediction




#command line interface for training, evaluating, and predicting
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Train, evaluate, or predict using the model")
    parser.add_argument("action", choices=["train", "evaluate", "predict"])
    parser.add_argument("--version", default="1.0.0")
    parser.add_argument("--resume")

    args = parser.parse_args()

    if args.action == "train":
        train_model(version=args.version)
    elif args.action == "evaluate":
        evaluate_model(version=args.version)
    elif args.action == "predict":
        if not args.resume:
            print("Please provide a resume text using --resume.")
        else:
            category = predict_single_resume(resume_text=args.resume, version=args.version)
            if category:
                print(f"Predicted Category: {category}")
