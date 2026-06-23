
import os
import joblib

# The model file produced by `python manage.py train_spam_classifier`.
MODEL_PATH = os.path.join(
    os.path.dirname(__file__), 'ml', 'spam_model.joblib'
)


class SpamClassifierService:
    _model = None
    _load_attempted = False

    @classmethod
    def _get_model(cls):
        """
loads the trained data just once
        """
        if cls._model is None and not cls._load_attempted:
            cls._load_attempted = True
            try:
                cls._model = joblib.load(MODEL_PATH)
            except (FileNotFoundError, Exception):
                cls._model = None
        return cls._model

    @classmethod
    def spam_probability(cls, text):
        if not text or not text.strip():
            return 0.0

        model = cls._get_model()
        if model is None:
            return 0.0
        probabilities = model.predict_proba([text])[0] #probability of a text to be spam
        spam_index = list(model.classes_).index('spam') #get the index of the spam value
        return float(probabilities[spam_index]) #return the actual value from

    @classmethod
    def is_spam(cls, text, threshold):

        return cls.spam_probability(text) >= threshold