from fastapi import FastAPI, APIRouter
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.database import db_intance
from datetime import datetime, timedelta
import numpy as np
from app.routes.manageCurrentlocation import updateCurrent, deleteCurrent
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
        data = list(
            db_intance.get_collection("SignalReport")
            .find(
                {
                    "deviceClass": {"$in": ["arubaTag", "iBeacon"]},
                    "timeStamp": {"$gt": datetime.now() - timedelta(hours=8)},
                }
            )
            .sort([("timeStamp", -1)])
        )

        if data:
            # Convert timeStamp to datetime if necessary
            for dt in data:
                if isinstance(dt["timeStamp"], str):
                    dt["timeStamp"] = datetime.strptime(
                        dt["timeStamp"], "%Y-%m-%dT%H:%M:%S"
                    )

            # Find the latest timestamp
            latest_timestamp = max(record["timeStamp"] for record in data)
            time_threshold = latest_timestamp - timedelta(seconds=30)

            # Filter records within the last 30 seconds of the latest timestamp
            relevant_data = [
                record
                for record in data
                if time_threshold <= record["timeStamp"] <= latest_timestamp
            ]

            if relevant_data:
                highest_rssi_per_tagMac = {}

                for record in relevant_data:
                    tag_mac = record["tagMac"]
                    location = record["location"]
                    rssi_values = [rssi["rssi"] for rssi in record["rssi"]]
                    avg_rssi = np.mean(rssi_values)

                    # Update the highest avg_rssi for each tagMac
                    if (
                        tag_mac not in highest_rssi_per_tagMac
                        or avg_rssi > highest_rssi_per_tagMac[tag_mac]["avg_rssi"]
                    ):
                        highest_rssi_per_tagMac[tag_mac] = {
                            "tagMac": tag_mac,
                            "location": location,
                            "avg_rssi": avg_rssi,
                            "timeStamp": record["timeStamp"],
                        }

                # Prepare the data for insertion
                output_json = list(highest_rssi_per_tagMac.values())
            # find all tags
            tags = db_intance.get_collection("tags").find({})
            # get tagMac to array
            tags_tagMac = {tag["tagMac"] for tag in tags if "tagMac" in tag}
            output_tagMac = {tag["tagMac"] for tag in output_json if "tagMac" in tag}
            # find common value in output and tags
            common_tags = set(tags_tagMac).intersection(output_tagMac)
            not_common_tags = [tag for tag in tags_tagMac if tag not in common_tags]
            for output in output_json:
                create = await updateCurrent(output)
                if create:
                    await updateHistory(output)
            # delete data not update next
            for tag in not_common_tags:
                delete = await deleteCurrent(tag)
                if delete:
                    data = {
                        "tagMac": tag,
                        "location": "Lost signal",
                        "avg_rssi": "-",
                        "timeStamp": datetime.now(),
                    }
                    await updateHistory(data)
        else:
            print("No data to insert")
    finally:
        lock.release()


def run_update_rssi():
    asyncio.run(update_rssi())

async def delete_old_data():
    print("Starting delete_old_data function")
    data = list(db_intance.get_collection("SignalReport").find())
    latest_timestamp = max(record["timeStamp"] for record in data)
    cutoff_time = latest_timestamp - timedelta(hours=2)
    result = db_intance.get_collection("SignalReport").delete_many({
        'timeStamp': {'$lt': cutoff_time}
    })
    print(f"Deleted {result.deleted_count} documents older than {cutoff_time}")

def run_delete_old_data():
    asyncio.run(delete_old_data())


# Initialize the scheduler
def scheduler():
    scheduler = BackgroundScheduler()

    # Job to update RSSI every minute
    trigger_update = IntervalTrigger(seconds=5)
    scheduler.add_job(run_update_rssi, trigger_update)

    # Job to delete old data every 2 hours
    trigger_delete = IntervalTrigger(hours=2)
    scheduler.add_job(run_delete_old_data, trigger_delete)

    scheduler.start()


scheduler()