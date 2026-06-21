"""
Trains the Naive Bayes spam classifier and saves it to disk.

Run:
    python manage.py train_spam_classifier

What it does:
1. Loads training data (hand-written examples + public SMS dataset if present)
2. Splits into train/test so we can measure real accuracy on unseen data
3. Builds a pipeline: CountVectorizer (text -> word counts) + MultinomialNB
4. Trains the model and reports accuracy/precision/recall on the test set
5. Saves the trained pipeline to spam_model.joblib for the detector to load
"""

import os

from django.core.management.base import BaseCommand

import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

from apps.bot_detection.ml.training_data import SPAM_EXAMPLES, HAM_EXAMPLES

# Where the dataset and model live.
ML_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'ml')
ML_DIR = os.path.abspath(ML_DIR)
SMS_DATASET = os.path.join(ML_DIR, 'SMSSpamCollection')
MODEL_PATH = os.path.join(ML_DIR, 'spam_model.joblib')


class Command(BaseCommand):
    help = "Train the Naive Bayes spam classifier and save it to disk."

    def handle(self, *args, **options):
        texts, labels = self._load_data()

        self.stdout.write(self.style.NOTICE(
            f"Loaded {len(texts)} examples "
            f"({labels.count('spam')} spam, {labels.count('ham')} ham)."
        ))

        # Split: 80% to train on, 20% held back to test honestly on data
        # the model has never seen. stratify keeps the spam/ham ratio
        # consistent across both splits.
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=0.2, random_state=42, stratify=labels
        )

        # The pipeline chains two steps so we can treat them as one object:
        #   1. CountVectorizer: turns each text into a vector of word counts
        #      (drops English stop words like "the" that carry no signal)
        #   2. MultinomialNB: the Naive Bayes classifier itself
        model = Pipeline([
            ('vectorizer', CountVectorizer(stop_words='english')),
            ('classifier', MultinomialNB()),
        ])

        self.stdout.write("Training...")
        model.fit(X_train, y_train)

        # Evaluate on the held-out test set.
        predictions = model.predict(X_test)
        report = classification_report(y_test, predictions)
        self.stdout.write(self.style.SUCCESS("\nTest set performance:\n"))
        self.stdout.write(report)

        # Save the whole pipeline (vectorizer + classifier together).
        joblib.dump(model, MODEL_PATH)
        self.stdout.write(self.style.SUCCESS(
            f"\nModel saved to {MODEL_PATH}"
        ))

    def _load_data(self):
        """Combine hand-written examples with the public SMS dataset."""
        texts = list(SPAM_EXAMPLES) + list(HAM_EXAMPLES)
        labels = (
            ['spam'] * len(SPAM_EXAMPLES) +
            ['ham'] * len(HAM_EXAMPLES)
        )

        # Add the public SMS dataset if it's been downloaded.
        if os.path.exists(SMS_DATASET):
            with open(SMS_DATASET, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split('\t', 1)
                    if len(parts) == 2:
                        label, text = parts
                        if label in ('spam', 'ham'):
                            texts.append(text)
                            labels.append(label)
            self.stdout.write("Included public SMS dataset.")
        else:
            self.stdout.write(self.style.WARNING(
                "SMS dataset not found — training on hand-written data only. "
                "Download it for better accuracy."
            ))

        return texts, labels