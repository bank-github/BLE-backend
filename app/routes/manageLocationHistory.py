from fastapi import APIRouter, HTTPException
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from app.database import db_intance
from app.models.modelLocaion import UpdateLocation
from app.message import getMsg

router = APIRouter()

@router.get('/gets')
async def gets():
    try:
        result = []
        doc = db_intance.get_collection("LocationHistory").find().sort({"timeStamp": -1})
         # Fetch tags data
        tags = list(db_intance.get_collection("tags").find())
        tags_dict = {tag["tagMac"]: tag for tag in tags}
        if doc:
            for rs in doc:
                tag_mac = rs["tagMac"]
                if tag_mac in tags_dict:
                    rs["assetName"] = tags_dict[tag_mac].get("assetName")
                    rs["deviceClass"] = tags_dict[tag_mac].get("deviceClass")
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

@router.get('/gets/{mac}')
async def gets(mac: str):
    try:
        result = []
        doc = db_intance.get_collection("LocationHistory").find(({"tagMac": mac})).sort({"timeStamp": -1})
         # Fetch tags data
        tags = list(db_intance.get_collection("tags").find())
        tags_dict = {tag["tagMac"]: tag for tag in tags}
        if doc:
            for rs in doc:
                tag_mac = rs["tagMac"]
                if tag_mac in tags_dict:
                    rs["assetName"] = tags_dict[tag_mac].get("assetName")
                    rs["deviceClass"] = tags_dict[tag_mac].get("deviceClass")
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
    
async def updateHistory(updateLocation : UpdateLocation):
    try:
        db_intance.get_collection("LocationHistory").insert_one(updateLocation)
        return print("Add history: " + updateLocation['tagMac'])
    except Exception as err:
        return print(err)