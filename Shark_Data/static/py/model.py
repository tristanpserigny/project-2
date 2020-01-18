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

def run_model(modelname, input_pitch, input_amount, input_exchange, input_valuation, input_gender, input_category):
    shark_to_model = modelname
    fileloc = f"{shark_to_model}_model.pkl"
    vocfile = f"{shark_to_model}_vocab.pkl"
    path = os.path.join("static","py",fileloc)
    vocpath = os.path.join("static","py",vocfile)
    the_model = joblib.load(path)

    transformer = TfidfTransformer()
    loaded_vectorizer = TfidfVectorizer(decode_error="replace",vocabulary=pickle.load(open(vocpath, "rb")))
    tfidf = transformer.fit_transform(loaded_vectorizer.fit_transform(np.array(input_pitch)))
    input_df = pd.DataFrame(tfidf.toarray(), columns=loaded_vectorizer.get_feature_names())

    input_df.loc[0,"Amount_Asked_For"] = input_amount
    input_df.loc[0,"Exchange_For_Stake"] = input_exchange
    input_df.loc[0,"Valuation"] = input_valuation
    input_df.loc[0,f"Gender_{input_gender}"] = 1
    input_df.loc[0,f"Category_{input_category}"] = 1

    prediction = the_model.predict(input_df)

    return prediction