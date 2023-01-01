from datetime import datetime, date, time, timedelta

from pydantic import BaseModel, EmailStr, PositiveInt, PositiveFloat

class TripBase(BaseModel):
    time_created: datetime | None
    time_updated: datetime | None
    description: str
    is_ongoing: bool | None
    agent_email: EmailStr | None
    cost: float | None
    participants: int | None
    fav_posint: PositiveInt | None
    fav_posreal: PositiveFloat | None
    start_date: date | None
    flight_landing: datetime | None
    check_in_time: time | None
    on_holiday_for: timedelta | None
