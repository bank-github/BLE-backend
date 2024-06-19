from fastapi import FastAPI
from app.routes import manageTags
from app.routes import manageUser
from datetime import datetime
app = FastAPI()

# app.include_router(setting_message.router, prefix='/settings', tags=['settings']) #can use
app.include_router(manageTags.router, prefix='/tags', tags=['tags'])
app.include_router(manageUser.router, prefix='/user', tags=['user'])

@app.get('/')
async def root():
    return datetime.now()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1",port=8000, log_level="info")
