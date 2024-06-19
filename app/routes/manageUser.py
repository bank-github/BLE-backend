from fastapi import APIRouter, HTTPException
from bson.objectid import ObjectId
from app.database import db_intance
from app.models.modelUser import User, CreateUser, UpdateUser
from app.message import getMsg
from passlib.context import CryptContext
# Create an instance of CryptContext with bcrypt algorithm
enCode = CryptContext(schemes=["bcrypt"], deprecated="auto")


router = APIRouter()

@router.get('/gets')
async def gets():
    try:
        result = []
        doc = db_intance.get_collection("user").find({})
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
        doc = db_intance.get_collection("user").find_one({"_id": ObjectId(id)})
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
    
@router.post('/register')
async def add(user : CreateUser):
    try:
        docUser = db_intance.get_collection("user").find_one({"username": user.username})
        if docUser:
            raise HTTPException(status_code=403, detail=getMsg(40301))
        user.password = enCode.hash(user.password)
        rs = {}
        doc = db_intance.get_collection("user").insert_one(user.dict())
        rs['_id'] = str(doc.inserted_id)
        result = rs | user.dict()
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="setting_description")
    except HTTPException as httpErr:
        raise httpErr
    except Exception as err:
        print(err)
        raise HTTPException(status_code=500, detail=getMsg(50003))
    

@router.post('/login')
async def add(user : User):
    try:
        doc = db_intance.get_collection("user").find_one({"username": user.username})
        if doc:
            deCode = enCode.verify(user.password, doc["password"])
            if not deCode:
                raise HTTPException(status_code=401, detail="Incorrect password")
            doc['_id'] = str(doc['_id'])
            return doc
        else:
            raise HTTPException(status_code=404, detail=getMsg(40402))
    except HTTPException as httpErr:
        raise httpErr
    except Exception as err:
        print(err)
        raise HTTPException(status_code=500, detail=getMsg(50003))
    
    

@router.patch('/update/{id}')
async def update(id: str, user : UpdateUser):
    print(user.dict(exclude_unset=True))
    try:
        rs = {}
        doc = db_intance.get_collection("Setting_Message").update_one(
            {'_id':ObjectId(id)},
            {'$set': user.dict(exclude_unset=True)}
        )
        print(doc)
        if doc.modified_count == 1:
            rs['_id'] = id
            result = rs | user.dict(exclude_unset=True)
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
        doc = db_intance.get_collection("user").delete_one({'_id':ObjectId(id)})
        if doc.deleted_count == 1:
            return {"status": id + " deleted"}
        else:
            raise HTTPException(status_code=404, detail=getMsg(40402))
    except HTTPException as httpErr:
        raise httpErr
    except Exception as err:
        print(err)
        raise HTTPException(status_code=500, detail=getMsg(50005))

