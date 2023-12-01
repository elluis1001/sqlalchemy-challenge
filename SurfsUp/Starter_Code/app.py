# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect = True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>"
    )
# Convert the query results from your precipitation analysis 
    # (i.e. retrieve only the last 12 months of data)
    #  to a dictionary using date as the key and prcp as the value.
@app.route("/api/v1.0/precipitation")

def precipitation():
    previous_year = dt.date(2016, 8, 17)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= previous_year).all()
    rain = {date:  prcp for date, prcp in precipitation}
    return jsonify(rain)

# Return a JSON list of stations from the dataset.
def stations():
    list_stations = session.query(Station.station).all()
    stations = list(np.ravel(list_stations))
    return jsonify(stations = stations)

if __name__ == "__main__":
    app.run(debug=True)

