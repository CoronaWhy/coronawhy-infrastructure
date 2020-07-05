from fastapi import FastAPI
from covid19dh import covid19
import json

app = FastAPI()

@app.get("/")
def read_root():
    return {"CoronaWhy Data API": "v0.1"}

#@app.get("/items/{item_id}")
#def read_item(item_id: int, q: str = None):
#    return {"item_id": item_id, "q": q}

@app.get("/country/{item_id}")
# http://api.apps.coronawhy.org/data/country/FRA
def data_item(item_id: str, q: str = None):
    dataset = covid19(item_id, verbose = False)
    data = json.loads(dataset.to_json())
    return json.dumps(data, sort_keys=True, indent=4)

@app.get("/data_by_pid/{item_id}")
def data_persistent(item_id: str, q: str = None):
    return {"PID": pid, "q": q}

