## How to use

# Import 

All variables are set in the environment. To run the script, you need to pass the file name as an argument:
```
python3 import.py ingredients.json
```

# FastAPI
To run fastapi.py use the follow command:
```
uvicorn main:app --reload
```

To check GET request:
```
curl -H 'Accept: application/json; indent=4'  http://127.0.0.1:8000/prediction/?ing=rise,something_else
```

To check POST request:
```
curl -X POST -H "Content-Type: application/json" "http://127.0.0.1:8000/feedback/" -d '{"ingredients":"rise,something_else", "time": 100}'
```
