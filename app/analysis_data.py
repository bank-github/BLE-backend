from fastapi import FastAPI, APIRouter
from apscheduler.schedulers.background import BackgroundScheduler
from app.database import db_intance
from datetime import datetime, timedelta
import numpy as np

app = FastAPI()
router = APIRouter()

def update_rssi():
    print("Starting update_rssi function")

    # Fetch data with deviceClass "arubaTag" or "iBeacon"
    data = list(db_intance.get_collection("SignalReport").find({
        'deviceClass': {'$in': ["arubaTag", "iBeacon"]}
    }).sort({"timeStamp": -1}))

    # Fetch tags data
    tags = list(db_intance.get_collection("tags").find())
    tags_dict = {tag["tagMac"]: tag for tag in tags}

    if data:
        # Convert timeStamp to datetime if necessary
        for dt in data:
            if isinstance(dt["timeStamp"], str):
                dt["timeStamp"] = datetime.strptime(dt["timeStamp"], "%Y-%m-%dT%H:%M:%S")

        # Find the latest timestamp
        latest_timestamp = max(record["timeStamp"] for record in data)
        time_threshold = latest_timestamp - timedelta(seconds=30)

        # Filter records within the last 30 seconds of the latest timestamp
        relevant_data = [record for record in data if time_threshold <= record["timeStamp"] <= latest_timestamp]

        if relevant_data:
            highest_rssi_per_tagMac = {}

            for record in relevant_data:
                tag_mac = record["tagMac"]
                location = record["location"]
                rssi_values = [rssi['rssi'] for rssi in record["rssi"]]
                avg_rssi = np.mean(rssi_values)

                # Update the highest avg_rssi for each tagMac
                if tag_mac not in highest_rssi_per_tagMac or avg_rssi > highest_rssi_per_tagMac[tag_mac]["avg_rssi"]:
                    highest_rssi_per_tagMac[tag_mac] = {
                        "tagMac": tag_mac,
                        "deviceClass": record["deviceClass"],
                        "location": location,
                        "avg_rssi": avg_rssi,
                        "timeStamp": record["timeStamp"]
                    }

            # Prepare the data for insertion
            output_json = list(highest_rssi_per_tagMac.values())
            for output in output_json:
                tag_mac = output["tagMac"]
                if tag_mac in tags_dict:
                    output["assetName"] = tags_dict[tag_mac].get("assetName")

            # Update Analyse_Location collection
            LocationHistory_collection = db_intance.get_collection("LocationHistory")
            CurrentLocation = db_intance.get_collection("CurrentLocation")
            CurrentLocation.delete_many({})
            print("Deleted old data from Analyse_Location")

            LocationHistory_collection.insert_many(output_json)
            CurrentLocation.insert_many(output_json)
            print("Inserted new data into Analyse_Location")
    else:
        print("No data to insert")

# Initialize the scheduler
def scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_rssi, 'interval', minutes=1)
    scheduler.start()
