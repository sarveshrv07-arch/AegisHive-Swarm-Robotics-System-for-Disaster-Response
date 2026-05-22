import pandas as pd

from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import train_test_split

from joblib import dump


class SurvivorAI:

    def train_model(self):

        # Load dataset

        data = pd.read_csv(
            'datasets/survivor_dataset.csv'
        )

        # Features

        X = data[['heat', 'motion']]

        # Labels

        y = data['survivor']

        # Split data

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

        # Create AI model

        model = RandomForestClassifier()

        # Train AI

        model.fit(X_train, y_train)

        # Save trained model

        dump(
            model,
            'trained_models/survivor_classifier.pkl'
        )

        print("AI MODEL TRAINED SUCCESSFULLY")
