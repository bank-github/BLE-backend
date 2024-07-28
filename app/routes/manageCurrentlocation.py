from fastapi import APIRouter, HTTPException
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from app.database import db_instance
from app.models.modelLocaion import Location, UpdateLocation
from app.message import getMsg

router = APIRouter()

@router.get('/gets/{query}')
async def gets(query:str):
    try:
        result = []
        find = {}
        if query == "use":
            find = {"location": {"$ne": "No Signal"}}
        if query == "lost":
            find = {"location":"No Signal"}
        doc = db_instance.get_collection("CurrentLocation").find(find).sort({"timeStamp": -1})
        totalDoc = db_instance.get_collection("CurrentLocation").count_documents(find)
        # Fetch tags data
        tags = list(db_instance.get_collection("tags").find())
        tags_dict = {tag["tagMac"]: tag for tag in tags}
        if doc:
            for rs in doc:
                tag_mac = rs["tagMac"]
                if tag_mac in tags_dict:
                    rs["assetName"] = tags_dict[tag_mac].get("assetName")
                    rs["deviceClass"] = tags_dict[tag_mac].get("deviceClass")
                    rs["assetType"] = tags_dict[tag_mac].get("assetType")
                rs['_id'] = str(rs['_id'])
                dt_object = datetime.fromisoformat(str(rs['timeStamp']))+timedelta(hours=7)
                rs['timeStamp'] = dt_object.strftime("%Y-%m-%d %H:%M:%S")
                result.append(rs)
            return {
                'total': totalDoc,
                'data': result
            }
        else:
            raise HTTPException(status_code=404, detail=getMsg(40402))
    except HTTPException as httpErr:
        raise httpErr
    except Exception as err:
        print(err)
        raise HTTPException(status_code=500, detail=getMsg(50002))
    
async def updateCurrent(updateLocation : UpdateLocation):
    try:
        doc = db_instance.get_collection("CurrentLocation").update_one(
            {'location': updateLocation["location"], 'tagMac': updateLocation["tagMac"]},
            {'$set': {"avg_rssi": updateLocation["avg_rssi"]}}
        )
        if doc.matched_count == 0:
            db_instance.get_collection("CurrentLocation").delete_one({'tagMac': updateLocation["tagMac"]})
            db_instance.get_collection("CurrentLocation").insert_one(updateLocation)
            return True
        if doc.modified_count == 1:
            return print("Update rssi ", updateLocation["location"])
        if doc.matched_count == 1 and doc.modified_count == 0:
            return print("rssi value is the same")
    except Exception as err:
        return print(err)
    
# async def deleteCurrent(tag: str):
#     try:
#         doc =  db_instance.get_collection("CurrentLocation").delete_one({"tagMac": tag})
#         if doc.deleted_count == 1:
#             return True
#         if doc.deleted_count == 0:
#             return False
#     except Exception as err:
#         return print(err)
