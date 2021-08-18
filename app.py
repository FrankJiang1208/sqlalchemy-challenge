from flask import Flask,jsonify
from flask.globals import session
import numpy as np
import datetime as dt
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base=automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
mm=Base.classes.measurement
sta=Base.classes.station


#create app
app=Flask(__name__)

@app.route("/")
def home():
    return (f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/start<br/>"
            f"/api/v1.0/start/end")

@app.route("/api/v1.0/precipitation")
def prcp():
    session=Session(engine)
    prcp_list=list(np.ravel(session.query(mm.date,mm.prcp).all()))
    session.close()
    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():
    session=Session(engine)
    sts_list=list(np.ravel(session.query(mm.station).group_by(mm.station).all()))
    session.close()
    return jsonify(sts_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session=Session(engine)
    last_date=session.query(mm.date).order_by(mm.date.desc()).first()
    last_date=last_date[0]
    last_date=dt.datetime.strptime(last_date, '%Y-%m-%d')
    prev_date=last_date-dt.timedelta(days=365)
    m_actice_sts=session.query(mm.station).group_by(mm.station).order_by(func.sum(mm.id).desc()).first()

    tobs_list=list(np.ravel(session.query(mm.date,mm.tobs).filter(mm.station==m_actice_sts[0]).filter(mm.date>=prev_date).filter(mm.date<=last_date).all()))
    session.close()
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start(start):
    session=Session(engine)
    start_list=list(np.ravel(session.query(func.min(mm.tobs),func.avg(mm.tobs),func.max(mm.tobs)).filter(mm.date>=start).all()))
    session.close()
    return jsonify(start_list)

@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    session=Session(engine)
    startend_list=list(np.ravel(session.query(func.min(mm.tobs),func.avg(mm.tobs),func.max(mm.tobs)).filter(mm.date>=start).filter(mm.date<=end).all()))
    session.close()
    return jsonify(startend_list)


if __name__ == '__main__':
    app.run(debug=True)