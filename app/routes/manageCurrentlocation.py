from fastapi import APIRouter, HTTPException
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from app.database import db_intance
from app.models.modelLocaion import Location, UpdateLocation
from app.message import getMsg

router = APIRouter()

@router.get('/gets')
async def gets():
    try:
        result = []
        doc = db_intance.get_collection("CurrentLocation").find().sort({"timeStamp": -1})
        if doc:
            for rs in doc:
                rs['_id'] = str(rs['_id'])
                dt_object = datetime.fromisoformat(str(rs['timeStamp']))+timedelta(hours=7)
                rs['timeStamp'] = dt_object.strftime("%Y-%m-%d %H:%M:%S")
                result.append(rs)
            return result
        else:
            raise HTTPException(status_code=404, detail=getMsg(40402))
    except HTTPException as httpErr:
        raise httpErr
    except Exception as err:
        print(err)
        raise HTTPException(status_code=500, detail=getMsg(50002))
    
async def updateCurrent(updateLocation : UpdateLocation):
    try:
        doc = db_intance.get_collection("CurrentLocation").update_one(
            {'location': updateLocation["location"], 'tagMac': updateLocation["tagMac"]},
            {'$set': {"avg_rssi": updateLocation["avg_rssi"]}}
        )
        if doc.matched_count == 0:
            db_intance.get_collection("CurrentLocation").delete_one({'tagMac': updateLocation["tagMac"]})
            db_intance.get_collection("CurrentLocation").insert_one(updateLocation)
            return True
        if doc.modified_count == 1:
            return print("Update rssi ", updateLocation["location"])
        if doc.matched_count == 1 and doc.modified_count == 0:
            return print("rssi value is the same")
    except Exception as err:
        return print(err)
