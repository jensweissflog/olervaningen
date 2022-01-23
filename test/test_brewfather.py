from app import app
from app.models.brewfather import *
import pytest
import responses
import json

from datetime import datetime

def setup_module(brewfather):
    app.config['BREWFATHER_TOKEN'] = "token"
    app.config['BREWFATHER_URL'] = "http://url.local"

@responses.activate
def test_get_target_temp():
    responses.add(
        responses.GET,
        app.config['BREWFATHER_URL']+"batches",
        json=
[
    {
        "_id": "6E2lRljogqJDhRZlv3UXiN9ufhZCgc",
        "name": "Batch",
        "batchNo": 33,
        "status": "Fermenting",
        "brewer": "Olof Lennerstedt",
        "brewDate": 1632062934976,
        "recipe": {
            "name": "Budvar",
            "fermentation": {
                "name": "Imported",
                "_id": None,
                "steps": [
                    {
                        "actualTime": 1632088800000,
                        "stepTemp": 10,
                        "stepTime": 10,
                        "type": "Primary"
                    }
                ]
            }
        },
        "batchNotes": "Mäskhinken ökade i vikt från 6 till 9,7 kg dvs 3,7 liter vatten har absorberats\nWeissflog"
    },
    {
        "_id": "mE1tqLdJKbAmDTJeOgJ0wO44eyVtmB",
        "batchNotes": "Lars",
        "name": "Session",
        "batchNo": 32,
        "status": "Fermenting",
        "brewer": "Herman",
        "brewDate": 1631447014485,
        "recipe": {
            "name": "Super Simple Session Ale",
            "fermentation": {
                "name": "Ale",
                "_id": "default",
                "steps": [
                    {
                        "displayStepTemp": 15,
                        "actualTime": 1631447014485,
                        "type": "Primary",
                        "stepTemp": 15,
                        "displayPressure": None,
                        "ramp": None,
                        "pressure": None,
                        "stepTime": 10
                    }
                ]
            }
        }
    },
    {
        "_id": "WVHNRagAcfpvygvppeUibDMf2KYrbT",
        "name": "Batch",
        "batchNo": 13,
        "status": "Fermenting",
        "brewer": "Olof Lennerstedt",
        "brewDate": 1631824153964,
        "recipe": {
            "name": "Bryggeributikens California Common Lager",
            "fermentation": {
                "name": "Imported",
                "steps": [
                    {
                        "stepTemp": 17,
                        "actualTime": 1631824153964,
                        "type": "Primary",
                        "stepTime": 10
                    }
                ],
                "_id": None
            }
        }
    }
]
      )
    myResponse=get_request("batches","")
    assert myResponse[0]['batchNo']==33
    assert get_target_temp("Weissflog")==10
    assert get_target_temp("Lars") == 15
    assert get_target_temp("Göran") == app.config['DEFAULT_TEMP']

