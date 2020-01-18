import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from string import punctuation
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
stopwords = stopwords.words( 'english' ) + list(punctuation)
stemmer = PorterStemmer()
import pickle
from sklearn.externals import joblib
import os

def run_model(input_pitch, input_amount, input_exchange, input_valuation, input_gender, input_category):
    dealloc = "Deal_Status_model.pkl"
    dealvoc = "Deal_Status_vocab.pkl"
    sharkloc = "Deal_Shark 1_model.pkl"
    sharkvoc = "Deal_Shark 1_vocab.pkl"
    path = os.path.join("static","py",dealloc)
    vocpath = os.path.join("static","py",dealvoc)
    sharkpath = os.path.join("static","py",sharkloc)
    sharkvocpath = os.path.join("static","py",sharkvoc)

    deal_model = joblib.load(path)
    shark_model = joblib.load(sharkpath)

    #Deal Model
    transformer = TfidfTransformer()
    loaded_vectorizer = TfidfVectorizer(decode_error="replace",vocabulary=pickle.load(open(vocpath, "rb")))
    tfidf = transformer.fit_transform(loaded_vectorizer.fit_transform(np.array(input_pitch)))
    input_df = pd.DataFrame(tfidf.toarray(), columns=loaded_vectorizer.get_feature_names())

    input_df.loc[0,"Amount_Asked_For"] = input_amount
    input_df.loc[0,"Exchange_For_Stake"] = input_exchange
    input_df.loc[0,"Valuation"] = input_valuation
    input_df.loc[0,f"Gender_{input_gender}"] = 1
    input_df.loc[0,f"Category_{input_category}"] = 1

    dealprediction = deal_model.predict(input_df)

    if (dealprediction[0] == 1):

        #Shark Model
        transformer = TfidfTransformer()
        loaded_vectorizer = TfidfVectorizer(decode_error="replace",vocabulary=pickle.load(open(sharkvocpath, "rb")))
        tfidf = transformer.fit_transform(loaded_vectorizer.fit_transform(np.array(input_pitch)))
        input_df_shark = pd.DataFrame(tfidf.toarray(), columns=loaded_vectorizer.get_feature_names())

        input_df_shark.loc[0,"Amount_Asked_For"] = input_amount
        input_df_shark.loc[0,"Exchange_For_Stake"] = input_exchange
        input_df_shark.loc[0,"Valuation"] = input_valuation
        input_df_shark.loc[0,f"Gender_{input_gender}"] = 1
        input_df_shark.loc[0,f"Category_{input_category}"] = 1

        sharkprediction = shark_model.predict(input_df_shark)

        return dealprediction[0], sharkprediction
    
    else:

        return dealprediction[0], np.nan

    