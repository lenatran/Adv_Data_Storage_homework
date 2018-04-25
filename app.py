# Dependencies
import pandas as pd
import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Create engine to hawaii.sqlite
engine = create_engine("sqlite:///hawaii.sqlite")

# Declare a Base
Base = automap_base()

# Reflect the database tables
Base.prepare(engine, reflect=True)

# Create variables for classes
Measurement = Base.classes.measurements
Station = Base.classes.stations

# Create session
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start<br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")    
def precipitation():
    """Return a list of dates and precipitation observations for the last year"""
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    last_year_rain = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > last_year\
                                                                  ).order_by(Measurement.date).all()
    rain = []
    for r in last_year_rain:
        rain_results = {}
        rain_results["date"] = r.date
        rain_results["prcp"] = r.prcp
        rain.append(rain_results)

    return jsonify(rain)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    station_results = session.query(Station.name, Station.station).all()
    station_list = []
    
    for s in station_results:
        station_row = {}
        station_row["name"] = s.name
        station_row["station"] = s.station
        station_list.append(station_row)

    return jsonify(station_list)
        
    
@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of all temperature observations for the previous year"""
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs_year = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > last_year\
                                                                        ).order_by(Measurement.date).all()
    tobs_list = []
    
    for t in tobs_year:
        tobs_results = {}
        tobs_results["date"] = t.date
        tobs_results["tobs"] = t.tobs
        tobs_list.append(tobs_results)

    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
def start_date(start):
    """Return TMIN, TAVG, and TMAX for all dates greater than and equal to start date"""
    start_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)\
                                 ).filter(Measurement.date >= start).all()
    results_list = []
    
    for data in start_results:
        results_row = {}
        results_row["TMIN"] = start_results[0][0]
        results_row["TAVG"] = start_results[0][1]
        results_row["TMAX"] = start_results[0][2]
        results_list.append(results_row)
        
    return jsonify(results_list)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """Return TMIN, TAVG, and TMAX for all dates between the start and end date inclusive"""
    start_end_dates  = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)\
                                   ).filter((Measurement.date >= start) & (Measurement.date <= end)).all()   
    results_list = []
    
    for data in start_end_dates:
        results_row = {}
        results_row["TMIN"] = start_end_dates[0][0]
        results_row["TAVG"] = start_end_dates[0][1]
        results_row["TMAX"] = start_end_dates[0][2]
        results_list.append(results_row)
        
    return jsonify(results_list)


if __name__ == "__main__":
    app.run(debug=True)