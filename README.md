1. create venv "python -m venv venv"
2. activate "venv floder" to use 
[
    "windows : venv\Scripts\activate"
    "max, linux : source venv/bin/activate"
]
3. install libary as you need in to it (I'll make list in requerements.txt )
   use "pip install -r requirements.txt"
   
4.to start project in path BLE-v1 use "uvicorn app.main:app --reload" or "uvicorn app.main:app --reload --port ..."

if you install library more please use "pip freeze > requirements.txt" before push the code
