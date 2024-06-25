from fastapi import APIRouter, HTTPException
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from app.database import db_intance
from app.models.modelHistory import History
from app.message import getMsg

router = APIRouter()

@router.get('/gets')
async def gets():
    try:
        result = []
        doc = db_intance.get_collection("LocationHistory").find().sort({"timeStamp": -1})
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