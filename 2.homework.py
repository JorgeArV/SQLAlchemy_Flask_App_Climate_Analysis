#1. We import our dependencies
from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

import datetime as dt
import numpy as np
import pandas as pd

#2. Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#3. reflect an existing database into a new model
Base = automap_base()
#4. reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement
#Flask 
app = Flask(__name__)

#Route #1
@app.route("/")
def main():    
    return ("Welcome to my answer to the 'Step 2 - Climate App' section of the homework! These are all the routes available: <br/>"
            "1. /api/v1.0/precipitation <br/>"
            "2. /api/v1.0/stations <br/>"
            "3. /api/v1.0/tobs <br/>"
            "4. /api/v1.0/YYY-MM-DD/YYY-MM-DD<br/>"
            "5. /api/v1.0/YYY-MM-DD")

#Route #2 --> Please note: the indications in the instructions and grading rubric do not match. The grading rubric states that I must get the data from the LAST YEAR, while the indications request ALL datapoints. I have chosen to follow the rubric indications.
@app.route("/api/v1.0/precipitation")
def precipitation(): 
    session = Session(engine)
    #  We calculate the latest data point in the data set and make sure it is a date, not a string:
    latest_data_point_0 = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    latest_data_point_1 = dt.datetime.strptime(latest_data_point_0[0], "%Y-%m-%d")
    latest_data_point_1
    # We calculate the date 1 year ago of the last data point
    one_year_ago = latest_data_point_1 - dt.timedelta(days=1*365)
    one_year_ago
    # We perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()

    session.close()
    return jsonify(results)

#Route #3
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    # We perform a query to retreive the stations and their name (unsure if the indication to show 'list of stations' means the code or the name of the station. Hence, I have added both data points)
    results2 = session.query(Station.station, Station.name).all()

    session.close()
    return jsonify(results2)

#Route #4 --> Please note: the indications in the instructions and grading rubric do not match. The indications ask to return a JSON list of TOBS for the second last year. The rubrics ask for a JSON list of TOBS for the last year. To remain consistent, I have chosen to follow the rubric indications.
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    #We perform a query to determine the most active station:
    choice = session.query(Measurement.station).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).limit(1).all()
    choice_clean = choice[0][0]
    choice_clean
    #  We calculate the latest data point in the data set and make sure it is a date, not a string:
    latest_data_point_0 = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    latest_data_point_1 = dt.datetime.strptime(latest_data_point_0[0], "%Y-%m-%d")
    latest_data_point_1
    # We calculate the date 1 year ago of the last data point
    one_year_ago = latest_data_point_1 - dt.timedelta(days=1*365)
    one_year_ago
    #We perform a query to obtain dates and temperature observations of the most active station for the last year of data:
    results3 = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= one_year_ago).filter(Measurement.station == choice_clean).all()

    session.close()
    return jsonify(results3)

#Route #5 (opition 1)
@app.route("/api/v1.0/<start>/<end>")
def dates(start,end):

    session = Session(engine)
    results4 = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    session.close()
    return jsonify(results4)
    #return f"Below you will find the minimum temperature, maximum temperature and average temperature recorded in this database between the dates you included in the URL {jsonify(results4)}"

#Route #5 (opition 2)
@app.route("/api/v1.0/<start>")
def dates1(start):

    session = Session(engine)
    results5 = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()
    return jsonify(results5)

if __name__ == '__main__': 
    app.run(debug=True)








