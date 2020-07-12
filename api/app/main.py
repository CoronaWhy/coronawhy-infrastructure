# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from elasticsearch import helpers, Elasticsearch
from covid19dh import covid19, cite
from config import search_host, search_username, search_password, search_port, search_index_name, covid19datahub_title, covid19datahub_citation, covid19datahub_licence, covid19datahub_goal, covid19datahub_authors, mongohost, mongouser, mongopassword, mongodatabase, cordversion
from config import DV_ALIAS, BASE_URL, API_TOKEN, PARSABLE_EXTENSIONS_PY, PARSABLE_EXTENSIONS, gitroot
from pymongo import MongoClient
from pyDataverse.api import Api, NativeApi
import pandas as pd
import json

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="CoronaWhy Data API",
        description="CoronaWhy is globally distributed, volunteer-powered research organisation. We're trying to assist the medical community's ability to answer key questions related to COVID-19.",
        version="0.1",
        routes=app.routes,
    )

    openapi_schema['tags'] = tags_metadata

    app.openapi_schema = openapi_schema
    return app.openapi_schema

tags_metadata = [
    {
        "name": "country",
        "externalDocs": {
            "description": "Put this citation in working papers and published papers that use this dataset: %s" % covid19datahub_citation,
            "authors": covid19datahub_authors,
            "url": "https://covid19datahub.io",
        },
    },
    {
        "name": "dataverse",
        "externalDocs": {
            "description": "Dataverse integration by API. Available actions: [showfiles, getfile]",
        },
    },
    {
        "name": "cord",
        "description": "Metadata by cord_id",
        "externalDocs": {
            "description": "CORD-19 collection access by cord_id",
            "url": "https://api.apps.coronawhy.org/",
        },
    },
    {
        "name": "altmetrics",
        "description": "Altmetrics by DOI or cord_id",
        "externalDocs": {
            "description": "CORD-19 papers Altmetrics",
            "url": "https://api.apps.coronawhy.org/",
        },
    },
    {
        "name": "search",
        "description": "CORD-19 search",
        "externalDocs": {
            "description": "CORD-19 papers search",
            "url": "https://api.apps.coronawhy.org/",
        },
    }
]

app = FastAPI(
    openapi_tags=tags_metadata
)
app.openapi = custom_openapi

#@app.get("/items/{item_id}")
#def read_item(item_id: int, q: str = None):
#    return {"item_id": item_id, "q": q}

@app.get("/country/{item_id}", tags=["country"])
# http://api.apps.coronawhy.org/data/country/FRA
def data_item(item_id: str, q: str = None):
    jsondataset = covid19(item_id, verbose = False)
    data = {}
    datapoints = json.loads(jsondataset.to_json(orient='records'))
    data['authors'] = str(covid19datahub_authors)
    data['goal'] = str(covid19datahub_goal)
    data['licence'] = covid19datahub_licence
    data['citation'] = covid19datahub_citation
    data['downloads'] = 0
    data['data'] = datapoints
    data['citations'] = cite(jsondataset)
    #return json.dumps(data, sort_keys=True, indent=4)
    return data

@app.get("/dataverse/{action}", tags=["dataverse"])
def dataverse(action: str, doi: str = None, fileid: str = None):
    api = NativeApi(BASE_URL, API_TOKEN)
    PID = 'doi:10.5072/FK2/3OZLV6'
    if doi:
        PID = doi
    if action == 'showfiles':
        files = api.get_datafiles(PID, ':latest').json()
        if not fileid:
            return files
    if action == 'getfile':
        if not fileid:
            df = pd.DataFrame(files['data'])
            filesindex = {}
            for i in df.index:
                filesindex[df.iloc[i].label] = df.iloc[i].dataFile 
            pdfiles = pd.DataFrame(filesindex)
            FILEID=pdfiles.loc['id'][0]
            return pdfiles
        else:
            FILEID=fileid
            fileURL = "%s/api/access/datafile/%s" % (BASE_URL, FILEID)
            df = pd.read_csv(fileURL) 
            data = {}
            datapoints = json.loads(df.to_json(orient='records'))
            data['data'] = datapoints
            return data 

@app.get("/cordsearch/", tags=["search"])
def search_cord(fieldname: str = None, q: str = None):
    if not fieldname:
        fieldname = 'title'
    # search_host, search_username, search_password, search_port, search_index_name
    es = Elasticsearch("http://%s:%s@%s:%s/" % (search_username, search_password, search_host, search_port), Port=search_port)
    if es is not None:
        search_object = {'query': {'match': {fieldname: q}}}
        res = es.search(index=search_index_name, body=json.dumps(search_object))
        return res
    return { 'q': 'no data' }

@app.get("/cord/", tags=["cord"])
def read_cord(cord_uid: str = None, pid: str = None):
    client = MongoClient("mongodb://%s:%s@%s" % (mongouser, mongopassword, mongohost))
    db = client.get_database(mongodatabase)
    collection = db[cordversion]
    PaperByCordID = {'cord_uid': {"$in": [cord_uid]}}
    if pid:
        PaperByCordID = {'doi': {"$in": [pid]}}
    dbdata = collection.find(PaperByCordID)
    df = pd.DataFrame(dbdata)
    df = df[['cord_uid','title','authors','abstract','path']]
    datapoints = df
    data = {}
    data['data'] = datapoints
    return data

@app.get("/altmetrics/", tags=["altmetrics"])
def read_altmetrics(cord_uid: str = None, pid: str = None):
    client = MongoClient("mongodb://%s:%s@%s" % (mongouser, mongopassword, mongohost))
    altmetricsdb = client.get_database('altmetrics')
    cordversion = 'v19'
    altcollection = altmetricsdb[cordversion]
    PaperByCordID = {'cord_uid': {"$in": [cord_uid]}}
    if pid:
        PaperByCordID = {'doi': {"$in": [pid]}}
    data = {}
    dbdata = altcollection.find(PaperByCordID)
    metadata = []
    for item in dbdata:
        metadata.append(item['title'])
    data['data'] = metadata
    return data
