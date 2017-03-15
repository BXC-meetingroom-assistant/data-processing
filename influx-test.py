from influxdb import InfluxDBClient
import json

with open('settings.json') as data_file:
    settings = json.load(data_file)


client = InfluxDBClient(
    settings['server'],
    settings['port'],
    settings['user'],
    settings['password'],
    settings['namespace']
)

result = client.query('SELECT * from "netatmo.IAQ02" order by time desc limit 10;')

for point in result.get_points():
    print(point.keys())
    for item in point.items():
        print(item)
