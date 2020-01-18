import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from string import punctuation
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
stopwords = stopwords.words( 'english' ) + list(punctuation)
stemmer = PorterStemmer()
import pickle

import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, os.path.join('static','py'))
from model import run_model

app = Flask(__name__)


#################################################
# Database Setup
#################################################

dbname = "SharkTank"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///db/{dbname}.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
Shark_Table = Base.classes.Shark_Tank
User_Table = Base.classes.User_Tank


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/names")
def names():
    """Return a list of sample names."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(Shark_Table).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the column names (sample names)
    return jsonify(list(df))

@app.route("/pitches")
def pitches():
    """Return a list of sample names."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(Shark_Table).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    data ={
        "Id": df.Id.values.tolist(),
        "Pitch Name": df.Title.values.tolist(),
        "Episode Code": df.Episode_Code.values.tolist()
    }
    # Return a list of the column names (sample names)
    return jsonify(data)


@app.route("/sharks")
def sharks():
    """Return a list of sample names."""

    results = db.session.query(Shark_Table).all()

    data = []
    for result in results:

        if(result.Deal_Status == "Deal Made"):
            data.append({
                "id": result.Id,
                "stake": result.Exchange_For_Stake,
                "ask": result.Amount_Asked_For,
                "valuation": result.Valuation,
                "deal": result.Deal_Status,
                "dealshark1": result.Deal_Shark_1,
                "dealshark2": result.Deal_Shark_2,
                "dealshark3": result.Deal_Shark_3,
                "dealshark4": result.Deal_Shark_4,
                "dealshark5": result.Deal_Shark_5
            })

        else:
            data.append({
                "id": result.Id,
                "stake": result.Exchange_For_Stake,
                "ask": result.Amount_Asked_For,
                "valuation": result.Valuation,
                "deal": result.Deal_Status,
                "dealshark1": result.Shark_1,
                "dealshark2": result.Shark_2,
                "dealshark3": result.Shark_3,
                "dealshark4": result.Shark_4,
                "dealshark5": result.Shark_5
            })

    # Return a list of the column names (sample names)
    return jsonify(data)

@app.route("/sharkpage")
def sharkpage():

    return render_template("shark.html")

@app.route('/map')
def map():
    return render_template('loc.html')

@app.route('/funpage', methods=['POST','GET'])
def funpage():
    if request.method == 'POST':
        result = request.form
        print(result)

        input_title = result["title"]
        input_pitch = [result["pitch"]]
        input_amount = int(result["ask"])
        input_exchange = int(result["stake"])
        input_valuation = int(result["val"])
        input_gender = result["gen"]
        input_category = result["cat"]

        dbresults = db.session.query(User_Table.Title).all()
        titles = [x[0] for x in dbresults]
        print(titles)
        
        if input_title not in titles:
            new = User_Table(Title=input_title, Category=input_category, Amount_Asked_For=input_amount, Exchange_For_Stake=input_exchange, Valuation=input_valuation, Description=input_pitch[0])
            db.session.add(new)
            db.session.commit()

        if (run_model("Barbara Corcoran", input_pitch, input_amount, (input_exchange / 100), input_valuation, input_gender, input_category)[0] == 0):
            barbpred = "Sorry, I'm out!"
        else:
            barbpred = "You've got a deal!"
        
        return render_template('fun.html', input_title=input_title, input_pitch=input_pitch[0], input_amount=input_amount, input_exchange=input_exchange, input_valuation=input_valuation, input_gender=input_gender, input_category=input_category, barbpred=barbpred)

    return render_template('fun.html')


@app.route('/userpitches')
def userpitches():
    results = db.session.query(User_Table).all()

    inputs = []
    for result in results:
        inputs.append({
            "id": result.Id,
            "title": result.Title,
            "category": result.Category,
            "ask": result.Amount_Asked_For,
            "exchange": result.Exchange_For_Stake,
            "valuation": result.Valuation,
            "description": result.Description
        })
    return jsonify(inputs)

@app.route('/userpitches/<title>')
def specific_pitch(title):
    results = db.session.query(User_Table).filter(User_Table.Title == title).all()

    inputs = []
    for result in results:
        inputs.append({
            "id": result.Id,
            "title": result.Title,
            "category": result.Category,
            "ask": result.Amount_Asked_For,
            "exchange": result.Exchange_For_Stake,
            "valuation": result.Valuation,
            "description": result.Description
        })
    return jsonify(inputs)

@app.route('/pitchpage')
def pitchpage():
    return render_template('pitch.html')


if __name__ == "__main__":
    app.run(debug=True)
