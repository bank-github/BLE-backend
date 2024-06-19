from fastapi import APIRouter, HTTPException
from bson.objectid import ObjectId
from app.database import db_intance
from app.models.modelTags import Tags, CreateTags, UpdateTags
from app.message import getMsg

router = APIRouter()

# get all tags in database
@router.get('/gets')
async def gets():
    try:
        result = []
        doc = db_intance.get_collection("tags").find({})
        if doc:
            for rs in doc:
                rs['_id'] = str(rs['_id'])
                result.append(rs)
            return result
        else:
            raise HTTPException(status_code=404, detail=getMsg(40401))
    except HTTPException as httpErr:
        raise httpErr
    except Exception as err:
        print(err)
        raise HTTPException(status_code=500, detail=getMsg(50002))

# get specific data tags by id
@router.get('/get/{id}')
async def get(id: str):
    try:
        doc = db_intance.get_collection("tags").find_one({"_id": ObjectId(id)})
        if doc:
            doc['_id'] = str(doc['_id'])
            return doc
        else:
            raise HTTPException(status_code=404, detail=getMsg(40401))
    except HTTPException as httpErr:
        raise httpErr
    except Exception as err:
        print(err)
        raise HTTPException(status_code=500, detail=getMsg(50002))
    
# get tags by mac address
@router.get('/getMac/{mac}')
async def get(mac: str):
    try:
        result = []
        query = {"tagMac": {"$regex": mac, "$options": "i"}}
        doc = db_intance.get_collection("tags").find(query)
        if doc:
            for rs in doc:
                rs['_id'] = str(rs['_id'])
                result.append(rs)
            return result
        else:
            raise HTTPException(status_code=404, detail=getMsg(40401))
    except HTTPException as httpErr:
        raise httpErr
    except Exception as err:
        print(err)
        raise HTTPException(status_code=500, detail=getMsg(50002))

# not in use now
@router.post('/add')
async def add(tags : Tags):
    try:
        rs = {}
        doc = db_intance.get_collection("Setting_Message").insert_one(tags.dict())
        rs['_id'] = str(doc.inserted_id)
        result = rs | tags.dict()
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="setting_description")
    except Exception as err:
        print(err)
        raise HTTPException(status_code=500, detail=getMsg(50003))

# update specific tags
@router.patch('/update/{id}')
async def update(id: str, updateTags : UpdateTags):
    try:
        rs = {}
        doc = db_intance.get_collection("tags").update_one(
            {'_id':ObjectId(id)},
            {'$set': updateTags.dict(exclude_unset=True)}
        )
        if doc.matched_count == 0:
            raise HTTPException(status_code=404, detail=getMsg(40401))
        if doc.modified_count == 1:
            rs['_id'] = id
            result = rs | updateTags.dict(exclude_unset=True)
            return result
        if doc.matched_count == 1 and doc.modified_count == 0:
            raise HTTPException(status_code=403, detail=getMsg(40301))
        else:
            raise HTTPException(status_code=403, detail=getMsg(40300))
    except HTTPException as httpErr:
        raise httpErr
    except Exception as err:
        print(err)
        raise HTTPException(status_code=500, detail=getMsg(50004))

# delete specific tag
@router.delete('/delete/{id}')
async def delete(id: str):
    try:
        doc = db_intance.get_collection("tags").delete_one({'_id':ObjectId(id)})
        if doc.deleted_count == 1:
            return {"status": id + " deleted"}
        else:
            raise HTTPException(status_code=404, detail=getMsg(40401))
    except HTTPException as httpErr:
        raise httpErr
    except Exception as err:
        print(err)
        raise HTTPException(status_code=500, detail=getMsg(50005))

