from fastapi import FastAPI
from covid19dh import covid19
import json

app = FastAPI()

@app.get("/")
def read_root():
    return {"CoronaWhy API": "v0.1"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/data/{item_id}")
def data_item(item_id: str, q: str = None):
    dataset = covid19(item_id, verbose = False)
    #return { "data": dataset.to_json() }
    data = json.loads(dataset.to_json())
    return json.dumps(data, sort_keys=True, indent=4)


