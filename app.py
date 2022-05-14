from sqlite3 import Date
from flask import Flask, jsonify

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)
Base = automap_base()
Base.prepare(engine, reflect = True)
measures = Base.classes.measurement
stations = Base.classes.station
sess = Session(engine)
latest_date = sess.query(measures.date).\
                        order_by(measures.date.desc()).\
                        limit(1).all()[0][0]

querydate = dt.datetime.strptime(latest_date, '%Y-%m-%d') - dt.timedelta(days=365)

# Perform a query to retrieve the data and precipitation scores
data_a = sess.query(measures.date, measures.prcp).\
        filter(measures.date > querydate).\
        order_by(measures.date).all()

#Perform a query to pull stations
data_b = sess.query(stations.station, stations.name, stations.latitude, stations.longitude)

#Most active station query

## find the most active station first:
stations_data = sess.query(measures.station, func.count(measures.station)).\
            group_by(measures.station).\
            order_by(func.count(measures.station).desc()).all()
station_1 = stations_data[0][0]

##pull the last year of data for that station
data_c = sess.query(measures.date, measures.tobs).filter(measures.date <= latest_date).\
        filter(measures.date >= querydate).filter(measures.station == station_1)


sess.close()

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate Data API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
    )


#Build the route and JSON response for the precipitation data
@app.route("/api/v1.0/precipitation")
def data_1_func():
    data_1 = []
    for date, pcrp  in data_a:
            data_1_dict = {}
            data_1_dict[f'{date}'] = pcrp
            data_1.append(data_1_dict)


    return jsonify(data_1)


#Build the route and JSON reponse for the station data
@app.route("/api/v1.0/stations")
def data_2_func():
    data_2 = []
    for station, name, latitude, longitud in data_b:
            data_2_dict = {}
            data_2_dict[f'Station'] = station
            data_2_dict[f'Name'] = name
            data_2_dict[f'Latitude'] = latitude
            data_2_dict[f'Longitude'] = longitud
            data_2.append(data_2_dict)


    return jsonify(data_2)
    

#Build the route and JSON reponse for the most active station data
@app.route("/api/v1.0/tobs")
def data_3_func():
    data_3 = []
    for date, tobs in data_c:
            data_3_dict = {}
            data_3_dict[f'Date'] = date
            data_3_dict[f'TOBS'] = tobs
            data_3.append(data_3_dict)


    return jsonify(data_3)



if __name__ == '__main__':
    app.run(debug=True)














app = Flask(__name__)

hello_dict = {"Hello": "World!"}


@app.route("/")
def home():
    return "Hi"


@app.route("/normal")
def normal():
    return hello_dict


@app.route("/jsonified")
def jsonified():
    return jsonify(hello_dict)


if __name__ == "__main__":
    app.run(debug=True)