from fastapi import FastAPI
from app.routes import manageTags
from app.routes import manageUser
from datetime import datetime
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# app.include_router(setting_message.router, prefix='/settings', tags=['settings']) #can use
app.include_router(manageTags.router, prefix='/tags', tags=['tags'])
app.include_router(manageUser.router, prefix='/user', tags=['user'])

@app.get('/')
async def root():
    return datetime.now()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1",port=8000, log_level="info")
