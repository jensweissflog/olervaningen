from app import app
import requests
from datetime import datetime
import json

now=datetime.now().timestamp()*1000

def time_(timestamp):
    return(datetime.fromtimestamp(timestamp/1000))

def get_request(url,params):
    url=app.config['BREWFATHER_URL']+url
    return requests.get(
        url,
        headers={
            "Authorization": app.config['BREWFATHER_TOKEN'],
            "Content-Type": "application/json",
        },
        params=params
    ).json()

def get_batches():
    params={
            "include": "recipe.fermentation,batchNotes",
            "complete": "True",
            "status": "Fermenting",
            }
    return(get_request("batches",params))

def get_target_temp(fridge):
    batches=get_batches()
    stepTemp=""
    for b in batches:
        try:
            bnote=b["batchNotes"]
        except KeyError:
            bnote=""
        if fridge in bnote and b["status"]=="Fermenting":
            try:
                steps=b["recipe"]["fermentation"]["steps"]
            except KeyError:
                print("No fermentation steps found")
                steps=[]
            for s in steps: 
                if now > s["actualTime"]: 
                    stepTemp=s["stepTemp"]
                else:
                    break
            if stepTemp=="":
                #set last temperature in list as target
                stepTemp=steps[len(steps)-1]["stepTemp"]
    if stepTemp != "":
        return(stepTemp)
    else:
        return(app.config['DEFAULT_TEMP'])



