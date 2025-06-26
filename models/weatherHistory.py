from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db=SQLAlchemy()

class WeatherHistory(db.Model):
    __tablename__="weatherHistory"
    id=db.Column(db.Integer,primary_key=True)
    city=db.Column(db.String(100),nullable=False,index=True)
    timestamp=db.Column(db.DateTime,nullable=False,default=datetime.utcnow,index=True)
    data=db.Column(db.JSON,nullable=False)
