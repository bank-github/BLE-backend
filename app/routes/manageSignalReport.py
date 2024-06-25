from fastapi import APIRouter, HTTPException
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from app.database import db_intance
from app.models.modelSignalReport import SignalReport
from app.message import getMsg

router = APIRouter()

@router.get('/gets/{mac}')
async def gets(mac: str):
    try:
        print(datetime.now()- timedelta(hours=7))
        result = []
        doc = db_intance.get_collection("SignalReport").find({"tagMac": mac, "timeStamp":{"$gt": datetime.now()-timedelta(hours=8)}}).sort({"timeStamp": -1})
        if doc:
            for rs in doc:
                rs['_id'] = str(rs['_id'])
                dt_object = datetime.fromisoformat(str(rs['timeStamp']))
                rs['timeStamp'] = dt_object.strftime("%Y-%m-%d %H:%M")
                result.append(rs)
            return result
        else:
            raise HTTPException(status_code=404, detail=getMsg(40402))
    except HTTPException as httpErr:
        raise httpErr
    except Exception as err:
        print(err)
        raise HTTPException(status_code=500, detail=getMsg(50002))
    
# @router.get('/get/{id}')
# async def get(id: str):
#     try:
#         doc = db_intance.get_collection("Setting_Message").find_one({"_id": ObjectId(id)})
#         if doc:
#             doc['_id'] = str(doc['_id'])
#             return doc
#         else:
#             raise HTTPException(status_code=404, detail=getMsg(40402))
#     except HTTPException as httpErr:
#         raise httpErr
#     except Exception as err:
#         print(err)
#         raise HTTPException(status_code=500, detail=getMsg(50002))
    
# @router.post('/add')
# async def add(modelSignalReport : CreateSetting_Message):
#     try:
#         rs = {}
#         doc = db_intance.get_collection("Setting_Message").insert_one(modelSignalReport.dict())
#         rs['_id'] = str(doc.inserted_id)
#         result = rs | modelSignalReport.dict()
#         if result:
#             return result
#         else:
#             raise HTTPException(status_code=404, detail="setting_description")
#     except Exception as err:
#         print(err)
#         raise HTTPException(status_code=500, detail=getMsg(50003))

# @router.patch('/update/{id}')
# async def update(id: str, modelSignalReport : UpdateSetting_Message):
#     print(modelSignalReport.dict(exclude_unset=True))
#     try:
#         rs = {}
#         doc = db_intance.get_collection("Setting_Message").update_one(
#             {'_id':ObjectId(id)},
#             {'$set': modelSignalReport.dict(exclude_unset=True)}
#         )
#         print(doc)
#         if doc.modified_count == 1:
#             rs['_id'] = id
#             result = rs | modelSignalReport.dict(exclude_unset=True)
#             return result
#         else:
#             raise HTTPException(status_code=403, detail=getMsg(40300))
#     except HTTPException as httpErr:
#         raise httpErr
#     except Exception as err:
#         print(err)
#         raise HTTPException(status_code=500, detail=getMsg(50004))

# @router.delete('/delete/{id}')
# async def delete(id: str):
#     try:
#         doc = db_intance.get_collection("Setting_Message").delete_one({'_id':ObjectId(id)})
#         if doc.deleted_count == 1:
#             return {"status": id + " deleted"}
#         else:
#             raise HTTPException(status_code=404, detail=getMsg(40402))
#     except HTTPException as httpErr:
#         raise httpErr
#     except Exception as err:
#         print(err)
#         raise HTTPException(status_code=500, detail=getMsg(50005))

