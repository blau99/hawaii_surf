import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Date 
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = declarative_base()

# reflect the tables
# Create Measurement and Station classes
# ----------------------------------
class Measurement(Base):
    __tablename__ = 'measurements'
    id = Column(Integer, primary_key=True)
    station = Column(String(255))
    date = Column(Date)
    prcp = Column(Float)
    tobs = Column(Integer)

class Station(Base):
    __tablename__ = 'stations'
    id = Column(Integer, primary_key=True)
    station = Column(Integer)
    name = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Float)


# Create our session (link) from Python to the DB
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
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date>'2016-08-23').order_by(Measurement.date).all()
    
    temps = []
    for temp in results:
        temp_dict = {}
        temp_dict["date"] = temp.date
        temp_dict["tobs"] = temp.tobs
        temps.append(temp_dict)

    return jsonify(temps)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Measurement.date,Measurement.station)\
                       .filter(Measurement.date>'2016-08-23').all()

    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement.date,Measurement.tobs)\
                       .filter(Measurement.station == 'USC00519281')\
                       .filter(Measurement.date>'2016-08-23').all()

    return jsonify(results)


@app.route("/api/v1.0/<start>") 

def calc_temps_start(start_date,end_date):
    results = session.query(func.min(Measurement.tobs), 
       func.avg(Measurement.tobs), 
       func.max(Measurement.tobs)).\
    filter(Measurement.date > start_date).filter(Measurement.date < end_date).first()
    
    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def calc_temps(start_date,end_date):
    results = session.query(func.min(Measurement.tobs), 
       func.avg(Measurement.tobs), 
       func.max(Measurement.tobs)).\
    filter(Measurement.date > start_date).filter(Measurement.date < end_date).first()
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
