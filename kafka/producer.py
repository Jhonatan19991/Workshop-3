import sys
import os

work_dir = os.getenv("WORK_DIR")
sys.path.append(work_dir)

import time
import json
import pandas as pd
from transforms.transform import  prepare_data
from kafka_connection import kafka_producer

if __name__ == "__main__":
    df = prepare_data()
    producer = kafka_producer()

    for row in df.values:
        dict_row = dict(row)
        to_json = json.dumps(dict_row)
        producer.send("workshop3", value=to_json)
        time.sleep(3)
        print("message sent")
    
    producer.close()
    print("all messages already send")


