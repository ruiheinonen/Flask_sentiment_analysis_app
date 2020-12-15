#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 20:15:59 2020

@author: fi000980702
"""
from flask import render_template
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import TextAreaField , SubmitField
from wtforms.validators import DataRequired
from flask import request

import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import models 
from tensorflow.keras import backend as K

import pickle

app = Flask(__name__, template_folder='templates')
@app.route('/')
def home():
	return render_template('homepage.html')

with open('tokenizer.pickle', 'rb') as handle:
    loaded_tokenizer = pickle.load(handle)

@app.route('/predict',methods=['GET', 'POST'])
def predict():

    if request.method == 'POST':
        message = request.form['message']
        data = [message]
        
        K.clear_session()
              
        seq = loaded_tokenizer.texts_to_sequences(data)
        padded = pad_sequences(seq, maxlen=len(data)) 
        model = models.load_model('sentiment_model.h5')
        pred = model.predict(padded)
        
        K.clear_session()
        
        return render_template('resultpage.html', prediction = pred)

if __name__ == '__main__':
	app.run()
