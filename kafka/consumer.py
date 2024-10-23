import sys
import os

work_dir = os.getenv("WORK_DIR")
sys.path.append(work_dir)


from kafka_connection import kafka_consumer
import joblib
import pandas as pd
import json

from src.models.model import HappinessPredictions
from src.database.dbconnection import getconnection
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

if __name__ == '__main__':

    engine = getconnection()
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        if inspect(engine).has_table('HappinessPredictions'):
            HappinessPredictions.__table__.drop(engine)
        HappinessPredictions.__table__.create(engine)
        print("Table created successfully.")
    except SQLAlchemyError as e:
        print(f"Error creating table: {e}")

    model = joblib.load("./model_training/polymodel.pkl")

    consumer = kafka_consumer()

    for m in consumer:
        print(f"Mensaje recibido: {m.value}")
        m_value = json.loads(m.value)
        m_normalize = pd.json_normalize(m_value)

        m_predict = m_normalize.drop(columns="Score")
        prediction = model.predict(m_predict)

        m_normalize['Predited_Score'] = prediction


        try:
            m_normalize.to_sql("HappinessPredictions", con=engine, if_exists='append', index=False)
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Error: {e}")




