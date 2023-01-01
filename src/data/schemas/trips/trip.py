from typing import Optional

from data.schemas.trips.tripBase import TripBase

class Trip(TripBase):
    id: int

    class Config:
        orm_mode = True
