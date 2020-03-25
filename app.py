import pandas as pd
import datetime as dt
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)
app = Flask(__name__)

@app.route("/")
def Homepage():
    return (
        f" List of all available routes: <br/>"
        f"------------------------------------- <br/>"
        f"1. /api/v1.0/precipitation <br/>"
        f"2. /api/v1.0/stations <br/>"
        f"3. /api/v1.0/tobs <br/>"
        f"4. /api/v1.0/<start>  <br/>"
        f"5. /api/v1.0/<start>/<end> <br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp = session.query(Measurement.date,Measurement.prcp).\
                    filter(func.strftime("%Y-%m-%d", Measurement.date) >= "2016-08-23").\
                    order_by(Measurement.date).all()
    prcp_list = []
    for i in prcp:
        dictionary_of_prcp = {}
        dictionary_of_prcp[i.date] = i.prcp
        prcp_list.append(dictionary_of_prcp)

    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():

    active_stations = session.query(Station)
    active_stations_data = []

    for j in active_stations:
        s_dict = {}
        s_dict["Station"] = j.station
        s_dict["Name"] = j.name
        active_stations_data.append(s_dict)

    return jsonify(active_stations_data)

@app.route("/api/v1.0/tobs")
def tobs():

    temps = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23').filter(Measurement.station == 'USC00519281').all()

    tobs_list = []

    for i,j in temps:
        tobs_dict= {}
        tobs_dict[i] = j
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def temperature_start(start):

    temp_data_list = []
    

    TMIN = session.query(func.min(Measurement.tobs)).filter(Measurement.date == start).all()
    TAVG = session.query(func.avg(Measurement.tobs)).filter(Measurement.date == start).all()
    TMAX = session.query(func.max(Measurement.tobs)).filter(Measurement.date == start).all()

    for i in TMIN: 
        temp_data_dict_i = {}
        temp_data_dict_i["TMIN"] = i
        temp_data_list.append(temp_data_dict_i)
    for j in TAVG: 
        temp_data_dict_j = {}
        temp_data_dict_j["TAVG"] = j
        temp_data_list.append(temp_data_dict_j)
    for k in TMAX: 
        temp_data_dict_k = {}
        temp_data_dict_k["TMAX"] = k
        temp_data_list.append(temp_data_dict_k)
    return jsonify(temp_data_list)

@app.route("/api/v1.0/<start>/<end>")
def calc_temps(start, end):

    temp_data_list_se = []
    

    TMIN = session.query(func.min(Measurement.tobs)).filter(Measurement.date.between(start,end)).all()
    TAVG = session.query(func.avg(Measurement.tobs)).filter(Measurement.date.between(start,end)).all()
    TMAX = session.query(func.max(Measurement.tobs)).filter(Measurement.date.between(start,end)).all()

    for i in TMIN: 
        temp_data_dict_i = {}
        temp_data_dict_i["TMIN"] = i
        temp_data_list_se.append(temp_data_dict_i)
    for j in TAVG: 
        temp_data_dict_j = {}
        temp_data_dict_j["TAVG"] = j
        temp_data_list_se.append(temp_data_dict_j)
    for k in TMAX: 
        temp_data_dict_k = {}
        temp_data_dict_k["TMAX"] = k
        temp_data_list_se.append(temp_data_dict_k)
    return jsonify(temp_data_list_se)

if __name__ == "__main__":
    app.run(debug=True)