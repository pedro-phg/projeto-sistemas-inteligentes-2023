import pickle
import re

import nltk
from allauth.account.models import EmailAddress
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from googletrans import Translator
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import WordPunctTokenizer

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('rslp')


class Post(models.Model):
    content = models.TextField(max_length=144)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    emotion = models.IntegerField(null=True, default=0)
    racist_sexist = models.IntegerField(null=True, default=0)

    



    def predict_emotion(self):

        def preprocess_tweet_text(text:str) -> str:
            """
            Limpa e pré-processa um tweet.

            Argumentos:
            text: string - Uma string que contém o tweet a ser limpo.

            Retorna:
            string - Uma string que contém o tweet pré-processado.
            """
            # Define as expressões regulares para encontrar e substituir menções (@) e URLs
            pat1 = r'@[A-Za-z0-9]+'
            pat2 = r'https?://[A-Za-z0-9./]+'
            combined_pat = r'|'.join((pat1, pat2))
            tok = WordPunctTokenizer()

            # Converte os caracteres HTML em texto usando BeautifulSoup
            soup = BeautifulSoup(text, 'lxml')
            souped = soup.get_text()

            # Remove menções e URLs
            stripped = re.sub(combined_pat, '', souped)

            try:
                # Remove caracteres especiais
                clean = stripped.decode("utf-8-sig").replace(u"\ufffd", "?")
            except:
                clean = stripped

            # Remove caracteres que não são letras do alfabeto
            letters_only = re.sub("[^a-zA-Z]", " ", clean)

            # Converte todas as letras para minúsculas
            lower_case = letters_only.lower()

            # Separa as palavras
            words = tok.tokenize(lower_case)
            
            # Remover stopwords
            stop_words = set(stopwords.words('english'))
            words = [word for word in words if word not in stop_words]
                
            # Unir as palavras pré-processadas em uma única string
            tweet = ' '.join(words)

            # Retorna a string com as palavras pré-processadas
            return (" ".join(words)).strip()

        with open('services/sentiment_classifier_v2.pkl', 'rb') as f:
            text_classifier = pickle.load(f)
        
        emotion = text_classifier.predict([preprocess_tweet_text(self.content)])[0]
        self.emotion = emotion
        return emotion

    def verify_if_could_be_racist_or_sexist(self):
        with open('services/racist_sexist_classifier.pkl', 'rb') as f:
            text_classifier = pickle.load(f)

        racist_sexist = text_classifier.predict([self.content])[0]
        self.racist_sexist = racist_sexist
        return racist_sexist
    
    def __str__(self) -> str:
        return f'{self.author} ({self.content})'
