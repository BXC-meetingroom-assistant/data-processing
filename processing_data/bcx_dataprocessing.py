import json
from influxdb import InfluxDBClient
import air
import temperature
with open('../settings.json') as data_file:
    settings = json.load(data_file)
# hono = settings['hono']
influx = settings['influx']


def dataprocessing(people):

    client = InfluxDBClient(influx["server"], influx["port"], influx[
                            "user"], influx["password"], influx["topic"])
    humidity_limit = [30, 50]  # under 30 turn it on and over50 turn it off
    co2_limit = [500, 1000]  # by turn it on and over 1000 shutting down
    temp_limit = [17, 22]

    variable = ['humidity', 'co2level', 'temperature']
    # queries=[]
    values = list()
    for i in range(0, len(variable)):
        result = client.query(
            'SELECT MEAN("value.%s.properties.status.sensor_value") FROM "netatmo.IAQ02" WHERE time > now() - 10m GROUP BY *,time(10m)' % (variable[i]))
        for point in result.get_points():
            for item in point.items():
                values.append(item)

    if people > 0:
        if temp_limit[1] > float(values[11][1]):
            temperature.set_manual_temperature(temp_limit[1])
            print('set te mperature to 22 degrees')
            # check temp temp_limit  please

        if (humidity_limit[0] > float(values[3][1]) or co2_limit[1] < float(values[7][1])):
            air.enable()
            print('set  turn on humidity device')
            # check temp temp_limit  please
        else:
            print('ok')

    else:  # everybody left the room
        temperature.set_manual_temperature(temp_limit[0])
        air.disable()
        print('turn off  tempemostat/ Humidifier ')
