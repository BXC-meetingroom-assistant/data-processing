from influxdb import InfluxDBClient
import hono, air, temperature

def dataprocessing(event): 

    #client = InfluxDBClient('bcx-workhorse.bosch-iot-suite.com', 8086, 'bcx2017', 'DeviceHub@BCX', 'bcx2017_telemetry')
    client = InfluxDBClient(hono.influx_server, hono.influx_port, hono.influx_user, hono.influx_password, hono.influx_topic)
    humidity_limit=[30,50] # under 30 turn it on and over50 turn it off 
# https://www.kane.co.uk/knowledge-centre/what-are-safe-levels-of-co-and-co2-in-rooms
    co2_limit=[500, 1000] # by turn it on and over 1000 shutting down  
    temp_limit=[17,22] #  below 17  nobody in the room  otherwise set temp to 22 
    
    variable=['humidity','co2level','temperature']
    #queries=[]
    values= list()
    for i in range(0,len(variable)):
       result  = client.query('SELECT MEAN("value.%s.properties.status.sensor_value") FROM "netatmo.IAQ02" WHERE time > now() - 10m GROUP BY *,time(10m)' %(variable[i]))
       for point in result.get_points():
    # print(point.keys())
            for item in point.items():
                values.append(item)
        #print(item)
    
    people= 0
    #for hunitidy 
    if people > 0 : 
        if temp_limit[1]>values[10][1]:
            temperature.set_manual_temperature(temp_limit[1])
            print('set te mperature to 22 degrees') 
            # check temp temp_limit  please
        
        if (humidity_limit[0]>values[2][1] or co2_limit[1]<values[6][1] )  :
            air.enable()
            print('set  turn on humidity device') 
            # check temp temp_limit  please
        else:
            print('ok')
        
    else: # everybody left the room 
        temperature.set_manual_temperature(temp_limit[0])
        air.disable()
        print('turn off  tempemostat/ Humidifier ') 

           
        
            
        
        
        
        
        
        
        
        
        
