from fastapi import APIRouter, HTTPException, Query
from bson.objectid import ObjectId
from app.database import db_instance
from app.models.modelTags import Tags, CreateTags, UpdateTags
from app.message import getMsg
from app.arrayTags import getTags_mac

router = APIRouter()

# get all tags in database
@router.get('/gets')
async def gets():
    try:
        result = []
        totalDoc = db_instance.get_collection("tags").count_documents({})
        doc = db_instance.get_collection("tags").find({})
        if doc:
            for rs in doc:
                rs['_id'] = str(rs['_id'])
                result.append(rs)
            return {
                'total': totalDoc,
                'data': result
            }
        else:
            raise HTTPException(status_code=404, detail=getMsg(40401))
    except HTTPException as httpErr:
        raise httpErr
    except Exception as err:
        print(err)
        raise HTTPException(status_code=500, detail=getMsg(50002))

# get with pagination
@router.get('/gets/pagination')
async def get(page: int = Query(1, ge=1), perPage: int = Query(10, ge=1)):
    try:
        result = []
        skip = (page - 1) * perPage
        totalDoc = db_instance.get_collection("tags").count_documents({})
        doc = db_instance.get_collection("tags").find({}).skip(skip).limit(perPage)
        if doc:
            for d in doc:
                d['_id'] = str(d['_id'])
                result.append(d)
            return {
                'total': totalDoc,
                'page': page,
                'perPage': perPage,
                'data': result
            }
        else:
            raise HTTPException(status_code=404, detail=getMsg(40401))
    except HTTPException as httpErr:
        raise httpErr
    except Exception as err:
        print(err)
        raise HTTPException(status_code=500, detail=getMsg(50002))
    
# get tags by mac address
@router.get('/getMac/{mac}')
async def getMac(mac: str):
    try:
        result = []
        query = {"tagMac": {"$regex": mac, "$options": "i"}}
        totalDoc = db_instance.get_collection("tags").count_documents(query)
        doc = db_instance.get_collection("tags").find(query)
        if doc:
            for rs in doc:
                rs['_id'] = str(rs['_id'])
                result.append(rs)
            return {
                'total': totalDoc,
                'data': result
            }
        else:
            raise HTTPException(status_code=404, detail=getMsg(40401))
    except HTTPException as httpErr:
        raise httpErr
    except Exception as err:
        print(err)
        raise HTTPException(status_code=500, detail=getMsg(50002))

# not in use now
@router.post('/add')
async def add(tags : CreateTags):
    try:
        rs = {}
        docTag = db_instance.get_collection("tags").find_one({"tagMac": tags.tagMac})
        if docTag:
            raise HTTPException(status_code=403, detail=getMsg(40301))
        doc = db_instance.get_collection("tags").insert_one(tags.dict())
        rs['_id'] = str(doc.inserted_id)
        result = rs | tags.dict()
        if result:
            getTags_mac()
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
        if not len(id)== 24:
            raise HTTPException(status_code=403, detail=getMsg(40300))
        rs = {}
        doc = db_instance.get_collection("tags").update_one(
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
async def delete(id: str, updateTags : UpdateTags):
    try:
        if not len(id) == 24:
            raise HTTPException(status_code=403, detail=getMsg(40300))
        doc = db_instance.get_collection("tags").delete_one({'_id':ObjectId(id)})
        if doc.deleted_count == 1:
            getTags_mac()
            db_instance.get_collection("LocationHistory").delete_many(updateTags.dict(exclude_unset=True))
            db_instance.get_collection("CurrentLocation").delete_many(updateTags.dict(exclude_unset=True))
            return {"detail": id + " deleted"}
        else:
            raise HTTPException(status_code=404, detail=getMsg(40401))
    except HTTPException as httpErr:
        raise httpErr
    except Exception as err:
        print(err)
        raise HTTPException(status_code=500, detail=getMsg(50005))

