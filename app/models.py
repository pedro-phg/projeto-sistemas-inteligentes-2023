import pickle

from django.contrib.auth.models import User
from django.db import models
from googletrans import Translator


class Post(models.Model):
    content = models.TextField(max_length=144)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    emotion = models.IntegerField(null=True, default=0)

    def predict_emotion(self):
        with open('services/sentiment_classifier.pkl', 'rb') as f:
            text_classifier = pickle.load(f)
        
        emotion = text_classifier.predict([self.content])[0]
        self.emotion = emotion
        return emotion

    def translate_text_to_english(self):
        translator = Translator()
        translated_text = translator.translate(self.content, dest='en').text
        self.content = translated_text
        return translated_text
    
    def translate_text_to_portuguese(self):
        translator = Translator()
        translated_text = translator.translate(self.content, dest='pt').text
        self.content = translated_text
        return translated_text

