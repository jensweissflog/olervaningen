from app.models.ha import *
from app.models.brewfather import *
fridges = [
            ["weissflog", "Weissflog"],
            ["kasai", "Kasai"],
            ["nykanen", "Nykanen"],
        ]
for f in fridges:
    attributes={
        "state_class": "measurement",
        "unit_of_measurement": "°C",
        "friendly_name": "Target temp "+f[1],
        "device_class": "temperature",
        }
    set_sensor_value("sensor.target_temp_"+f[0],get_target_temp(f[1]),attributes)
