"""
Loads the trained Naive Bayes spam classifier and exposes simple methods
for the detection checks to use. Keeps all the joblib/sklearn details in
one place so the rest of the code just asks "is this spam?".

The model is loaded ONCE (lazily, on first use) and cached, so repeated
calls during a recompute don't reload it from disk each time.
"""

import os
import joblib

# The model file produced by `python manage.py train_spam_classifier`.
MODEL_PATH = os.path.join(
    os.path.dirname(__file__), 'ml', 'spam_model.joblib'
)


class SpamClassifierService:
    # Cached model — loaded once, reused for the life of the process.
    _model = None
    _load_attempted = False

    @classmethod
    def _get_model(cls):
        """
        Load the model the first time it's needed, then return the cached
        copy. If the model file doesn't exist (e.g. training hasn't been
        run), this returns None and the checks degrade gracefully to
        "not spam" rather than crashing the whole recompute.
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
        """
        Returns the model's probability (0.0-1.0) that the text is spam.
        Returns 0.0 if there's no text or the model isn't available.

        We use the probability (not just the yes/no prediction) so the
        checks can require a CONFIDENCE threshold before flagging —
        reducing false positives on borderline text.
        """
        if not text or not text.strip():
            return 0.0

        model = cls._get_model()
        if model is None:
            return 0.0

        # predict_proba gives a probability per class. We find which
        # column corresponds to 'spam' and return that probability.
        probabilities = model.predict_proba([text])[0]
        spam_index = list(model.classes_).index('spam')
        return float(probabilities[spam_index])

    @classmethod
    def is_spam(cls, text, threshold):
        """
        True if the text's spam probability is at or above the threshold.
        The threshold lets us demand high confidence (e.g. 0.8) rather
        than just "more likely spam than not" (0.5).
        """
        return cls.spam_probability(text) >= threshold