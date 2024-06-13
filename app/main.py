from fastapi import FastAPI
from app.routes import setting_message
from datetime import datetime
app = FastAPI()

# app.include_router(setting_message.router, prefix='/settings', tags=['settings']) #can use
app.include_router(setting_message.router)

@app.get('/')
async def root():
    return datetime.now()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1",port=8000, log_level="info")
