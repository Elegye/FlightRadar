from FlightRadar24.api import FlightRadar24API
from pathlib import Path
import datetime
import json

fr_api = FlightRadar24API()

flights = fr_api.get_flights(bounds="49.152%2C43.595%2C-14.304%2C14.787")

filename = "data/{}.json".format(datetime.datetime.now().timestamp())
Path("./data").mkdir(parents=True, exist_ok=True)

with open(filename, "w") as file:
    json.dump(flights, file, default=lambda o: o.__dict__, sort_keys=True, indent=4)