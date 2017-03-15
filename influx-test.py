from influxdb import InfluxDBClient

client = InfluxDBClient('bcx-workhorse.bosch-iot-suite.com', 8086, '', '', 'bcx2017_telemetry')

result = client.query('SELECT * from "netatmo.IAQ02" order by time desc limit 10;')

# print(result)

# print("Result: {0}".format(result))
print("Result: {0}".format(result.get_points()))

for point in result.get_points():
    # print(point.keys())
    for item in point.items():
        print(item)
        # if key == 'value.dashboard_data.properties.CO2':
            # print(point.items()['value.dashboard_data.properties.CO2'])
    exit(0)
