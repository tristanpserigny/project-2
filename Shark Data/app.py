import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

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


# @app.route("/pitches/<pitch>")
# def pitch_data(pitch):
#     """Return `otu_ids`, `otu_labels`,and `sample_values`."""
#     stmt = db.session.query(Samples).statement
#     df = pd.read_sql_query(stmt, db.session.bind)

#     # Filter the data based on the sample number and
#     # only keep rows with values above 1
#     sample_data = df.loc[df[sample] > 1, ["otu_id", "otu_label", sample]]

#     # Sort by sample
#     sample_data.sort_values(by=sample, ascending=False, inplace=True)

#     # Format the data to send as json
#     data = {
#         "otu_ids": sample_data.otu_id.values.tolist(),
#         "sample_values": sample_data[sample].values.tolist(),
#         "otu_labels": sample_data.otu_label.tolist(),
#     }
#    return jsonify(data)

# @app.route("/sharks")
# def sharks():
#     """Return a list of sample names."""

#     # Use Pandas to perform the sql query
#     stmt = db.session.query(Samples).statement
#     df = pd.read_sql_query(stmt, db.session.bind)

#     # Return a list of the column names (sample names)
#     return jsonify(list(df.columns)[2:])

# @app.route("/sharks/<shark>")
# def shark_data(shark):
#     """Return `otu_ids`, `otu_labels`,and `sample_values`."""
#     stmt = db.session.query(Samples).statement
#     df = pd.read_sql_query(stmt, db.session.bind)

#     # Filter the data based on the sample number and
#     # only keep rows with values above 1
#     sample_data = df.loc[df[sample] > 1, ["otu_id", "otu_label", sample]]

#     # Sort by sample
#     sample_data.sort_values(by=sample, ascending=False, inplace=True)

#     # Format the data to send as json
#     data = {
#         "otu_ids": sample_data.otu_id.values.tolist(),
#         "sample_values": sample_data[sample].values.tolist(),
#         "otu_labels": sample_data.otu_label.tolist(),
#     }
#     return jsonify(data)

# @app.route("/metadata/<sample>")
# def sample_metadata(sample):
#     """Return the MetaData for a given sample."""
#     sel = [
#         Samples_Metadata.sample,
#         Samples_Metadata.ETHNICITY,
#         Samples_Metadata.GENDER,
#         Samples_Metadata.AGE,
#         Samples_Metadata.LOCATION,
#         Samples_Metadata.BBTYPE,
#         Samples_Metadata.WFREQ,
#     ]

#     results = db.session.query(*sel).filter(Samples_Metadata.sample == sample).all()

#     # Create a dictionary entry for each row of metadata information
#     sample_metadata = {}
#     for result in results:
#         sample_metadata["sample"] = result[0]
#         sample_metadata["ETHNICITY"] = result[1]
#         sample_metadata["GENDER"] = result[2]
#         sample_metadata["AGE"] = result[3]
#         sample_metadata["LOCATION"] = result[4]
#         sample_metadata["BBTYPE"] = result[5]
#         sample_metadata["WFREQ"] = result[6]

#     print(sample_metadata)
#     return jsonify(sample_metadata)


# @app.route("/samples/<sample>")
# def samples(sample):
#     """Return `otu_ids`, `otu_labels`,and `sample_values`."""
#     stmt = db.session.query(Samples).statement
#     df = pd.read_sql_query(stmt, db.session.bind)

#     # Filter the data based on the sample number and
#     # only keep rows with values above 1
#     sample_data = df.loc[df[sample] > 1, ["otu_id", "otu_label", sample]]

#     # Sort by sample
#     sample_data.sort_values(by=sample, ascending=False, inplace=True)

#     # Format the data to send as json
#     data = {
#         "otu_ids": sample_data.otu_id.values.tolist(),
#         "sample_values": sample_data[sample].values.tolist(),
#         "otu_labels": sample_data.otu_label.tolist(),
#     }
#     return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
