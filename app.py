# -*- coding: utf-8 -*-
"""Untitled14.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eKactgUbnbYdhlRJZqzPu-egBYfAiKXZ
"""
import re
import string
from flask import Flask,jsonify,request
from sklearn.feature_extraction.text import TfidfVectorizer
import xgboost
import pickle

# load phase
tf1 = pickle.load(open("tfidfvocab.pkl", 'rb'))
loaded_model = pickle.load(open("xgbmodel.sav", 'rb'))

#load vectorizer
vectorizer = TfidfVectorizer(binary=True,vocabulary = tf1)
vectorizer.fit(tf1)

def text_preproc(x):
  #case folding
  x = x.lower()
  #remove url
  x = re.sub(r'https*\S+', ' ', x)
  #remove username
  x = re.sub(r'<username>\s+', ' ', x)
  #remove punctuation
  x = re.sub('[%s]' % re.escape(string.punctuation), ' ', x)
  #remove number
  x = re.sub(r'\d', '', x)
  #remove double space
  x = re.sub(r'\s{2,}', ' ', x)
  return x

app = Flask(__name__)

@app.route('/api/sentence', methods=["GET"])
def sentece():
    arr_text = []
    text = request.args.get("text")
    arr_text.append(text) 
    clean_arr_text = list(map(text_preproc,arr_text))
    x_sentence = vectorizer.transform(clean_arr_text)
    y_pred = loaded_model.predict(x_sentence)
    resp = jsonify({"text":text,"prediction":int(y_pred[0])})
    return resp

@app.route('/')
def index():
    return "<h1>Prekocy-API !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)