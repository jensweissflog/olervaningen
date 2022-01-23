import requests
from datetime import datetime
import json

def post_request(endpoint,payload):
    url=app.config['HA_URL']+endpoint
    return request.post(
            url,
            headers = {
                "Authorization": "Bearer "+HA_TOKEN,
                "content-type": "application/json",
            },
            payload=payload
            )
