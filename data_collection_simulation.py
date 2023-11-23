# data_collection_simulation.py

import os
import time
import random
import json

def simulate_data_collection():
    # Simulate collecting data for a week
    for day in range(7):
        # Simulate hourly data collection
        for hour in range(24):
            # Simulate data for each hour
            data = {
                'timestamp': time.time(),
                'label': random.choice(['normal', 'anomaly']),
                'other_info': 'additional metadata'
            }

            # Save the data to a file
            filename = f"data_{day}_{hour}.json"
            with open(filename, 'w') as f:
                json.dump(data, f)

            print(f"Data collected and saved: {filename}")

            # Pause for a short time to simulate hourly intervals
            time.sleep(1)

if __name__ == "__main__":
    simulate_data_collection()
