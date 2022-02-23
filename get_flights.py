from FlightRadar24.api import FlightRadar24API
from influxdb_client import InfluxDBClient, Point
from influxdb_client.domain.write_precision import WritePrecision
from pathlib import Path
import datetime
import json

username = 'pi'
password = 'dwioalex'

database = 'flight_radar'
retention_policy = 'a_year'
bucket = f'{database}/{retention_policy}'

fr_api = FlightRadar24API()

flights = fr_api.get_flights(bounds="49.152%2C43.595%2C-14.304%2C14.787")

filename = "data/{}.json".format(datetime.datetime.now().timestamp())
Path("./data").mkdir(parents=True, exist_ok=True)

with open(filename, "w") as file:
    json.dump(flights, file, default=lambda o: o.__dict__, sort_keys=True, indent=4)

with InfluxDBClient(url='http://192.168.1.38:8086', token=f'{username}:{password}', org='-') as client:
    with client.write_api() as write_api:
        print('*** Write Points ***')
        with open(filename, "r") as file:
            flights = json.load(file)

            for flight in flights:
                point = Point("position")
                point = point.tag("aircraft_code", flight["aircraft_code"])
                point = point.tag("airline_iata", flight["airline_iata"])
                point = point.tag("origin_airport_iata", flight["origin_airport_iata"])
                point = point.tag("destination_airport_iata", flight["destination_airport_iata"])
                
                point = point.field("altitude", flight["altitude"])
                point = point.field("ground_speed", flight["ground_speed"])
                point = point.field("heading", flight["heading"])
                point = point.field("latitude", flight["latitude"])
                point = point.field("longitude", flight["longitude"])
                point = point.field("vertical_speed", flight["vertical_speed"])
                point = point.field("callsign", flight["callsign"])
                point = point.field("number", flight["number"])
                point = point.field("registration", flight["registration"])
                point = point.field("id", flight["id"])
                
                point = point.time(flight["time"] * 1000, write_precision=WritePrecision.MS)

                print(point.to_line_protocol())

                write_api.write(bucket=bucket, record=point)