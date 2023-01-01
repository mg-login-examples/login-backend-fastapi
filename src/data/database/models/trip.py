from datetime import datetime, date, time, timedelta

from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, Interval, Time, Date
from sqlalchemy.sql import func
from sqlalchemy_utils import EmailType

from data.database.models.base import Base

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    description = Column(String(1000))
    is_ongoing = Column(Boolean, default=True, nullable=True)
    agent_email = Column(EmailType, unique=True, index=True)
    cost = Column(Float, nullable=True)
    participants = Column(Integer, nullable=True)
    fav_posint = Column(Integer, nullable=True)
    fav_posreal = Column(Float, nullable=True)
    start_date = Column(Date, default=date(2023, 8, 6), nullable=True)
    flight_landing = Column(DateTime(timezone=True), default=datetime(2023, 8, 5, 6, 40), nullable=True)
    check_in_time = Column(Time, default=time(11, 30), nullable=True)
    on_holiday_for = Column(Interval, default=timedelta(days=10, hours=4, minutes=45, seconds=4), nullable=True)
