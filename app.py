from flask import Flask, jsonify
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

#set up for DB

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurements = Base.classes.measurement
Station = Base.classes.station

# Set up for flask

app = Flask(__name__)

# ROUTES

@app.route("/")
def welcome():
    "Listing all available routes"
    return (
        f"Your routes are:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    session = Session(bind=engine)

    results = session.query(Measurements.date, Measurements.prcp).all()

    session.close()

    all_precip = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        all_precip.append(precip_dict)

    return jsonify(all_precip)

@app.route("/api/v1.0/stations")
def stations():

    session = Session(bind=engine)

    results = session.query(Station.station).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def observations():

    session = Session(bind=engine)

    high_obs = session.query(Measurements.tobs).\
    filter(Measurements.station == 'USC00519281').filter(Measurements.date >= '2016-08-18').\
    filter(Measurements.date <= '2017-08-18').all()

    session.close()

    obs_prevyear = list(np.ravel(high_obs))

    return jsonify(obs_prevyear)


@app.route("/api/v1.0/<start>")
def stats_start(start):

    start_date = start

    session = Session(bind=engine)
    
    sel = [func.min(Measurements.tobs), 
       func.max(Measurements.tobs), 
       func.avg(Measurements.tobs)]

    results = session.query(*sel).filter(Measurements.date >= start_date).all()
       
    session.close()

    temp_list = list(np.ravel(results))

    return jsonify(temp_list)
    
@app.route("/api/v1.0/<start>/<end>")
def stats_end(start, end):

    start_date = start
    end_date = end

    session = Session(bind=engine)
    
    sel = [func.min(Measurements.tobs), 
       func.max(Measurements.tobs), 
       func.avg(Measurements.tobs)]

    results = session.query(*sel).filter(Measurements.date >= start_date).filter(Measurements.date <= end_date).all()
       
    session.close()

    temp_list = list(np.ravel(results))

    return jsonify(temp_list)

if __name__ == '__main__':
    app.run(debug=True)