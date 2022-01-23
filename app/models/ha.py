from app import app
import requests
from datetime import datetime
import json

def post_request(endpoint,payload):
    url=app.config['HA_URL']+endpoint
    return (requests.request("POST",
            url,
            headers = {
                "Authorization": "Bearer "+app.config['HA_TOKEN'],
                "content-type": "application/json",
            },
            data=json.dumps(payload)
            )
            )

def get_request_ha(url):
    url=app.config['HA_URL']+url
    return requests.get(
        url,
        headers={
            "Authorization": "Bearer "+app.config['HA_TOKEN'],
            "Content-Type": "application/json",
        },
    ).json()


def get_sensor_value(sensorid):
    data=get_request_ha("states/"+sensorid)
    try:
        return data['state']
    except KeyError:
        return None

def set_sensor_value(sensorid,value,attributes=""):
    payload={
            "state": value,
            "attributes": attributes
            }
    return post_request("states/"+sensorid,payload)
    
def update_target_temp(endpoint,target_temp):
    payload={
            "state": target_temp,
            }
    post_request(endpoint,payload)
