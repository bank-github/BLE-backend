from fastapi import FastAPI
from datetime import datetime
from starlette.middleware.cors import CORSMiddleware
from .arrayTags import getTags_mac
from app.routes import manageTags
from app.routes import manageUser
from app.routes import manageSignalReport
from app.routes import manageLocationHistory
from app.routes import manageCurrentlocation
from app.routes import manageAccessPoint
from .analysis_data import scheduler

app = FastAPI()

scheduler()
getTags_mac()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# app.include_router(setting_message.router, prefix='/settings', tags=['settings']) #can use
app.include_router(manageTags.router, prefix='/tags', tags=['tags'])
app.include_router(manageUser.router, prefix='/user', tags=['user'])
app.include_router(manageSignalReport.router, prefix='/report', tags=['report'])
app.include_router(manageLocationHistory.router, prefix='/history', tags=['history'])
app.include_router(manageCurrentlocation.router, prefix='/current', tags=['current location'])
app.include_router(manageAccessPoint.router, prefix='/ap', tags=['AP'])

@app.get('/')
async def root():
    return datetime.now()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1",port=7777, log_level="info")
