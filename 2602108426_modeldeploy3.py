# -*- coding: utf-8 -*-
"""2602108426_ModelDeploy3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17dj8rgGtl8kVy0_XtqAJp7IWDB-VeZt8
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier
import pickle

class ModelTrainer:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)

    def preprocess_data(self):
        # Data preprocessing steps
        self.data.dropna(subset=['CreditScore'], inplace=True)
        self.data.drop(columns=['Unnamed: 0', 'id', 'CustomerId', 'Surname'], inplace=True)

        # Define categorical and numeric columns
        self.categorical_columns = ['Geography', 'Gender', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'Tenure','churn']
        self.numeric_columns = ['CreditScore', 'Age', 'Balance', 'EstimatedSalary']

        # One-hot encode categorical columns
        self.data = pd.get_dummies(self.data, columns=self.categorical_columns[:-1], drop_first=True)

        # Standardize numeric columns
        scaler = StandardScaler()
        self.data[self.numeric_columns] = scaler.fit_transform(self.data[self.numeric_columns])

    def train_models(self):
        # Split data into train and test sets
        input_data = self.data.drop('churn', axis=1)
        output_data = self.data['churn']
        x_train, x_test, y_train, y_test = train_test_split(input_data, output_data, test_size=0.2, random_state=42)

        # Train RandomForestClassifier
        rf_classifier = RandomForestClassifier(random_state=42)
        rf_classifier.fit(x_train, y_train)
        self.rf_classifier = rf_classifier

        # Train XGBClassifier
        xgb_classifier = XGBClassifier(random_state=42)
        xgb_classifier.fit(x_train, y_train)
        self.xgb_classifier = xgb_classifier

    def evaluate_models(self, x_test, y_test):
        # Evaluate RandomForestClassifier
        rf_predictions = self.rf_classifier.predict(x_test)
        print("Random Forest Classifier Report:")
        print(classification_report(y_test, rf_predictions))

        # Evaluate XGBClassifier
        xgb_predictions = self.xgb_classifier.predict(x_test)
        print("XGBoost Classifier Report:")
        print(classification_report(y_test, xgb_predictions))

    def save_models(self, rf_model_path='rf_classifier_model.pkl', xgb_model_path='xgb_classifier_model.pkl'):
        # Save trained models
        with open(rf_model_path, 'wb') as file:
            pickle.dump(self.rf_classifier, file)

        with open(xgb_model_path, 'wb') as file:
            pickle.dump(self.xgb_classifier, file)

if __name__ == "__main__":
    data_path = '/content/sample_data/data_D.csv'

    model_trainer = ModelTrainer(data_path)
    model_trainer.preprocess_data()
    model_trainer.train_models()


    # Save models
    model_trainer.save_models()

