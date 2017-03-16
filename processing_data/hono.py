import json
from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container
import bcx_dataprocessing 

class HelloWorld(MessagingHandler):
    def __init__(self, server, telemetry, events, user, password, influx_server, influx_port, influx_user, influx_password, influx_topic):
        super(HelloWorld, self).__init__()
        self.server = server
        self.telemetry = telemetry
        self.events = events
        self.user = user
        self.password = password
        self.influx_server = influx_server
        self.influx_port = influx_port
        self.influx_user = influx_user
        self.influx_password = influx_password
        self.influx_topic = influx_topic

    def on_start(self, event):
        conn = event.container.connect(
            self.server, user=self.user, password=self.password)
        event.container.create_receiver(conn, source=self.telemetry)
        event.container.create_receiver(conn, source=self.events)

    def on_message(self, event):
        try:
            # print(event.message.properties['device_id'])
                  # : 'meeting-room-assistant'}'])
            if 'device_id' in event.message.properties and event.message.properties['device_id'] == "meeting-room-assistant":
                body = json.loads(event.message.body.decode("utf-8"))
                people = int(body['count'])
                bcx_dataprocessing.dataprocessing(people)
            # if body:
            #     pass
            # if 'topic' in body:
            #     if body['topic'] == 'bcx/meeting-room-assistant':
            #         print('yay')
            #     if body['topic'] == 'bcx/xdk.7cec79d330df/things/twin/commands/modify':
            #         # here pass to the procesessing function
            #             people = 0
        except json.decoder.JSONDecodeError as e:
            pass


with open('../settings.json') as data_file:
    settings = json.load(data_file)
hono = settings['hono']
influx = settings['influx']
Container(HelloWorld(hono['server'], hono['telemetry'], hono['events'], hono['user'], hono['password'], influx['server'], influx['port'], influx['user'], influx['password'], influx['topic'])).run()