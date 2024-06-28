from fastapi import APIRouter, HTTPException
from bson.objectid import ObjectId
from app.database import db_instance
from app.models.modelAccessPoint import AccessPoint, UpdateAccessPoint
from app.message import getMsg

router = APIRouter()

@router.get('/gets')
async def gets():
    try:
        result = []
        doc = db_instance.get_collection("accessPoint").find({})
        if doc:
            for rs in doc:
                rs['_id'] = str(rs['_id'])
                result.append(rs)
            return result
        else:
            raise HTTPException(status_code=404, detail=getMsg(40402))
    except HTTPException as httpErr:
        raise httpErr
    except Exception as err:
        print(err)
        raise HTTPException(status_code=500, detail=getMsg(50002))
    
@router.get('/get/{id}')
async def get(id: str):
    try:
        doc = db_instance.get_collection("AccessPoint").find_one({"_id": ObjectId(id)})
        if doc:
            doc['_id'] = str(doc['_id'])
            return doc
        else:
            raise HTTPException(status_code=404, detail=getMsg(40402))
    except HTTPException as httpErr:
        raise httpErr
    except Exception as err:
        print(err)
        raise HTTPException(status_code=500, detail=getMsg(50002))
    
# @router.post('/add')
# async def add(modelAccessPoint : CreateAccessPoint):
#     try:
#         rs = {}
#         doc = db_instance.get_collection("AccessPoint").insert_one(modelAccessPoint.dict())
#         rs['_id'] = str(doc.inserted_id)
#         result = rs | modelAccessPoint.dict()
#         if result:
#             return result
#         else:
#             raise HTTPException(status_code=404, detail="setting_description")
#     except Exception as err:
#         print(err)
#         raise HTTPException(status_code=500, detail=getMsg(50003))

@router.patch('/update/{id}')
async def update(id: str, modelAccessPoint : UpdateAccessPoint):
    print(modelAccessPoint.dict(exclude_unset=True))
    try:
        rs = {}
        doc = db_instance.get_collection("AccessPoint").update_one(
            {'_id':ObjectId(id)},
            {'$set': modelAccessPoint.dict(exclude_unset=True)}
        )
        print(doc)
        if doc.modified_count == 1:
            rs['_id'] = id
            result = rs | modelAccessPoint.dict(exclude_unset=True)
            return result
        else:
            raise HTTPException(status_code=403, detail=getMsg(40300))
    except HTTPException as httpErr:
        raise httpErr
    except Exception as err:
        print(err)
        raise HTTPException(status_code=500, detail=getMsg(50004))

@router.delete('/delete/{id}')
async def delete(id: str):
    try:
        doc = db_instance.get_collection("AccessPoint").delete_one({'_id':ObjectId(id)})
        if doc.deleted_count == 1:
            return {"status": id + " deleted"}
        else:
            raise HTTPException(status_code=404, detail=getMsg(40402))
    except HTTPException as httpErr:
        raise httpErr
    except Exception as err:
        print(err)
        raise HTTPException(status_code=500, detail=getMsg(50005))

