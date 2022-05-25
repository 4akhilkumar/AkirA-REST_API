from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

import requests

import re
import matplotlib.pyplot as plt
import string
from nltk.corpus import stopwords
import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize.treebank import TreebankWordDetokenizer
from collections import Counter
# from wordcloud import WordCloud
from nltk.corpus import stopwords
import nltk
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords
import gensim
from sklearn.model_selection import train_test_split
# import spacy
import pickle
import warnings
warnings.filterwarnings('ignore')
# import seaborn as sns
# from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt 
import tensorflow as tf
import keras
import numpy as np
import pandas as pd

from keras.models import Sequential
from keras import layers
# from keras.optimizers import RMSprop,Adam
from tensorflow.keras.optimizers import RMSprop,Adam
from keras.preprocessing.text import Tokenizer
# from keras.preprocessing.sequence import pad_sequences
from keras import regularizers
from keras import backend as K
from keras.callbacks import ModelCheckpoint

# Sentiment Analysis
train = pd.read_csv(r'akira_api_apps\sentimentAnalysis\sentimentAnalysisData\train.csv')

#Is there any other different value than neutral, negative and positive?
train['sentiment'].unique()

#How's distributed the dataset? Is it biased?
train.groupby('sentiment').nunique()

#Let's keep only the columns that we're going to use
train = train[['selected_text','sentiment']]

#Is there any null value?
train["selected_text"].isnull().sum()

#Let's fill the only null value.
train["selected_text"].fillna("No content", inplace = True)

def depure_data(data):
    
    #Removing URLs with a regular expression
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    data = url_pattern.sub(r'', data)

    # Remove Emails
    data = re.sub('\S*@\S*\s?', '', data)

    # Remove new line characters
    data = re.sub('\s+', ' ', data)

    # Remove distracting single quotes
    data = re.sub("\'", "", data)
        
    return data

temp = []
#Splitting pd.Series to list
data_to_list = train['selected_text'].values.tolist()
for i in range(len(data_to_list)):
    temp.append(depure_data(data_to_list[i]))
list(temp[:5])

def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations

data_words = list(sent_to_words(temp))

# print(data_words[:10])

def detokenize(text):
    return TreebankWordDetokenizer().detokenize(text)

data = []
for i in range(len(data_words)):
    data.append(detokenize(data_words[i]))
# print(data[:5])

data = np.array(data)

labels = np.array(train['sentiment'])
y = []
for i in range(len(labels)):
    if labels[i] == 'neutral':
        y.append(0)
    if labels[i] == 'negative':
        y.append(1)
    if labels[i] == 'positive':
        y.append(2)
y = np.array(y)
labels = tf.keras.utils.to_categorical(y, 3, dtype="float32")
del y

from keras.models import Sequential
from keras import layers
from keras.optimizers import RMSprop,Adam
from keras.preprocessing.text import Tokenizer
# from keras.preprocessing.sequence import pad_sequences
from keras_preprocessing.sequence import pad_sequences
from keras import regularizers
from keras import backend as K
from keras.callbacks import ModelCheckpoint
max_words = 5000
max_len = 200

tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(data)
sequences = tokenizer.texts_to_sequences(data)
# tweets = keras.preprocessing.sequence.pad_sequences(sequences, maxlen=max_len)
tweets = pad_sequences(sequences, maxlen=max_len)
# print(tweets)

#Splitting the data
X_train, X_test, y_train, y_test = train_test_split(tweets,labels, random_state=0)
# print (len(X_train),len(X_test),len(y_train),len(y_test))

# model2 = Sequential()
# model2.add(layers.Embedding(max_words, 40, input_length=max_len))
# model2.add(layers.Bidirectional(layers.LSTM(20,dropout=0.6)))
# model2.add(layers.Dense(3,activation='softmax'))
# model2.compile(optimizer='rmsprop',loss='categorical_crossentropy', metrics=['accuracy'])
# #Implementing model checkpoins to save the best metric and do not lose it on training.
# checkpoint2 = ModelCheckpoint("best_model2.hdf5", monitor='val_accuracy', verbose=1,save_best_only=True, mode='auto', period=1,save_weights_only=False)
# history = model2.fit(X_train, y_train, epochs=70,validation_data=(X_test, y_test),callbacks=[checkpoint2])

#Let's load the best model obtained during training
best_model = keras.models.load_model(r"akira_api_apps\sentimentAnalysis\sentimentAnalysisData\biderectionModel.hdf5")
print("Model Loaded")

@api_view(['POST'])
def sentimentAnalysis(request):
    if request.method == "POST":
        text = request.POST.get('feedback')

        sentiment = ['Neutral','Negative','Positive']
        try:
            sequence = tokenizer.texts_to_sequences([text])
            test = pad_sequences(sequence, maxlen=max_len)
            textSentiment = sentiment[np.around(best_model.predict(test), decimals=0).argmax(axis=1)[0]]
        except Exception as e:
            print(e)
        data = {
            'textSentiment': textSentiment
        }
        return Response(data)