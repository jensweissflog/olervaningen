#from app.models.brewfather import *
import requests
from datetime import datetime
import json

BREWFATHER_URL ="https://api.brewfather.app/v1/"
BREWFATHER_TOKEN="Basic N3NQTlB3am1BY1JJTHFyMmhuNTA2NU91VzdzMTpuMDB2aFppQndYcnBnbWZTcmJhWVNWbjEwOXhrNnRjMWpLaXhST200UDlucnEzRm1hUGhhSnM5cXdLYVFsTjA5"
now=datetime.now().timestamp()*1000
HA_URL="http://localhost:8123/"
HA_TOKEN=""


def time_(timestamp):
    return(datetime.fromtimestamp(timestamp/1000))

def get_request(url,params):
    url=BREWFATHER_URL+url
    return requests.get(
        url,
        headers={
            "Authorization": BREWFATHER_TOKEN,
            "Content-Type": "application/json",
        },
        params=params
    ).json()

def post_request(endpoint,payload):
    url=HUBPLANNER_URL+endpoint
    return request.post(
            url,
            headers = {
                "Authorization": "Bearer "+HA_TOKEN,
                "content-type": "application/json",
            },
            payload=payload
            )

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
        return(5)

def update_target_temp(endpoint,target_temp):
    payload={
            "state": target_temp,
            }
    post_request(endpoint,payload)


