from sqlalchemy import Column, Integer, String, DateTime, Boolean, TEXT, Float
from sqlalchemy.orm import declarative_base, relationship

BASE = declarative_base()
MAX_STRING_SIZE = 100

class HappinessPredictions(BASE):
    __tablename__ = 'HappinessPredictions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    Economy = Column(Float, nullable=False)
    Family = Column(Float, nullable=False)
    Health = Column(Float, nullable=False)
    Freedom = Column(Float, nullable=False)
    Trust = Column(Float, nullable=False)
    Generosity = Column(Float, nullable=False)
    year = Column(Integer, nullable=False)
    Region_America = Column(Integer, nullable=False)
    Region_Asia = Column(Integer, nullable=False)
    Region_Europe = Column(Integer, nullable=False)
    Region_Oceania = Column(Integer, nullable=False)
    Predited_Score = Column(Float, nullable=False)
    Score = Column(Float, nullable=False)
