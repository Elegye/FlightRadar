import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "<my-bucket>"
org = "<my-org>"
token = "<my-token>"
# Store the URL of your InfluxDB instance
url="http://bichette:8086"

client = influxdb_client.InfluxDBClient(
   url=url,
   token=token,
   org=org
)