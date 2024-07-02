from fastapi import FastAPI, APIRouter
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.database import db_instance
from datetime import datetime, timedelta
import numpy as np
from app.routes.manageCurrentlocation import updateCurrent
from app.routes.manageLocationHistory import updateHistory
from app.arrayTags import get_registered
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
        registered_tags = get_registered()
        # Fetch data with deviceClass "arubaTag" or "iBeacon"
        data = list(
            db_instance.get_collection("SignalReport")
            .find(
                {
                    "tagMac": {"$in": registered_tags},
                    "timeStamp": {"$gt": datetime.now() - timedelta(hours=7, seconds=40)},
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

            if data:
                highest_rssi_per_tagMac = {}

                for record in data:
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
                print(output_json)

            output_tagMac = {tag["tagMac"] for tag in output_json if "tagMac" in tag}
            # find common value in output and tags
            common_tags = set(registered_tags).intersection(output_tagMac)
            not_common_tags = [tag for tag in registered_tags if tag not in common_tags]
            print(not_common_tags)
            for output in output_json:
                create = await updateCurrent(output)
                if create:
                    await updateHistory(output)
            # change data not have signal
            for tag in not_common_tags:
                data = {
                        "tagMac": tag,
                        "location": "Lost signal",
                        "avg_rssi": "-",
                        "timeStamp": datetime.now(),
                    }
                lost = await updateCurrent(data)
                if lost:
                    await updateHistory(data)
        else:
            print("No data to insert")
    finally:
        lock.release()


def run_update_rssi():
    asyncio.run(update_rssi())

async def delete_old_data():
    print("Starting delete_old_data function")
    data = list(db_instance.get_collection("SignalReport").find())
    latest_timestamp = max(record["timeStamp"] for record in data)
    cutoff_time = latest_timestamp - timedelta(minutes=10)
    result = db_instance.get_collection("SignalReport").delete_many({
        'timeStamp': {'$lt': cutoff_time}
    })
    print(f"Deleted {result.deleted_count} documents older than {cutoff_time}")

def run_delete_old_data():
    asyncio.run(delete_old_data())


# Initialize the scheduler
def scheduler():
    scheduler = BackgroundScheduler()

    # Job to update RSSI every minute
    trigger_update = IntervalTrigger(seconds=30)
    scheduler.add_job(run_update_rssi, trigger_update)
    

    # Job to delete old data every 2 hours
    trigger_delete = IntervalTrigger(minutes=10)
    scheduler.add_job(run_delete_old_data, trigger_delete)

    scheduler.start()


scheduler()