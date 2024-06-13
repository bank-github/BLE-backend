1. create venv "python -m venv venv"
2. activate "venv floder" to use 
[
    "windows : .\venv(floder name)\Scripts\activate"
    "mac, linux : source .\venv(floder name)/bin/activate"
]
3. install libary as you need in to it (I'll make list in requerements.txt ) use "pip install -r requirements.txt"
4. to start project in path BLE-v1 use "uvicorn app.main:app --reload" or "uvicorn app.main:app --reload --port ..."
5. if you install library more please use "pip freeze > requirements.txt" before push the code
6. for another time to use you just activate "venv" and then start project
