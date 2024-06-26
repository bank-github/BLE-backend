from fastapi import FastAPI, APIRouter
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.database import db_intance
from datetime import datetime, timedelta
import numpy as np
from app.routes.manageCurrentlocation import updateCurrent
from app.routes.manageLocationHistory import updateHistory
import asyncio
import threading

app = FastAPI()
router = APIRouter()

lock = threading.Lock()

async def update_rssi():
    if not lock.acquire(blocking=False):
        print("Previous update_rssi call is still running. Skipping this run.")
        return
    try:
        print("Starting update_rssi function")

        # Fetch data with deviceClass "arubaTag" or "iBeacon"
        data = list(db_intance.get_collection("SignalReport").find({
            'deviceClass': {'$in': ["arubaTag", "iBeacon"]}, "timeStamp": {"$gt": datetime.now() - timedelta(hours=1)}
        }).sort([("timeStamp", -1)]))

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

                for output in output_json:
                    create = await updateCurrent(output)
                    if create:
                        await updateHistory(output)
        else:
            print("No data to insert")
    finally:
        lock.release()

def run_update_rssi():
    asyncio.run(update_rssi())

# Initialize the scheduler
def scheduler():
    scheduler = BackgroundScheduler()
    trigger = IntervalTrigger(seconds=10)
    scheduler.add_job(run_update_rssi, trigger)
    scheduler.start()

scheduler()
