# Import dependecies
import datetime as dt
import numpy as np
import pandas as pd

# Import SQLAlchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#Import Flask dependency
from flask import Flask, jsonify

#Set up database engine for the flask
engine = create_engine("sqlite:///hawaii.sqlite")

#Create a function to allow access and query SQLite
Base = automap_base()

#Reflect the table
Base.prepare(engine, reflect=True)

#Save the references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session link from Python to database
session = Session(engine)

#Set up flask application
app = Flask(__name__)
#All routes go under here or else code may not run properly.

#Welcome route
@app.route('/') # it defines the starting point
def welcome():
    return (
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''') #/api/v1.0/ signifies that this is version 1 of the application

# Create a route for precipitation
@app.route('/api/v1.0/precipitation')
# Create precipitation function
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# Create stations route
@app.route('/api/v1.0/stations')
#Create stations function
def stations():
    results = session.query(Station.station).all()
    # Unravelling the results into one-dimentional array and convert into a list
    stations =list(np.ravel(results))
    return jsonify(stations=stations)# This format the list into json

# Craete route for tobs
@app.route('/api/v1.0/tobs')
#Create temp function
def temp_monthly():
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
# Create route for temp start & end 
@app.route('/api/v1.0/temp/<start>')
@app.route('/api/v1.0/temp/<start>/<end>')

#Create stat function
def stats(start=None, end=None): #Adding parameters
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)]

    # To determine start and ending date
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
        temps = list(np.ravel(results))
        return jsonify(temps)

    # Calculate the temp min, max and avg with the start and end dates.
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
