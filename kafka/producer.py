import os
import sys

work_dir = os.getenv("WORK_DIR")
sys.path.append(work_dir)


import time
import json
import pandas as pd
from transforms.transform import  prepare_data
from kafka_connection import kafka_producer

if __name__ == "__main__":
    x, y = prepare_data()
    df = pd.concat([x, y], axis=1)
    producer = kafka_producer()

    for index, row in df.iterrows():
        dict_row = dict(row)
        to_json = json.dumps(dict_row)
        producer.send("workshop3", value=to_json)
        time.sleep(3)
        print("message sent")
    
    producer.close()
    print("all messages already send")


