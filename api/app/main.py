from fastapi import FastAPI
from covid19dh import covid19, cite
from config import covid19datahub_goal, covid19datahub_authors
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
    jsondataset = covid19(item_id, verbose = False)
    data = {}
    datapoints = json.loads(jsondataset.to_json())
    data['authors'] = str(covid19datahub_authors)
    data['goal'] = str(covid19datahub_goal)
    data['data'] = datapoints
    data['citations'] = cite(jsondataset)
    #return json.dumps(data, sort_keys=True, indent=4)
    return data

@app.get("/data_by_pid/{item_id}")
def data_persistent(item_id: str, q: str = None):
    return {"PID": pid, "q": q}

