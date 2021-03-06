import json
from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container


class HelloWorld(MessagingHandler):
    def __init__(self, server, telemetry, events, user, password):
        super(HelloWorld, self).__init__()
        self.server = server
        self.telemetry = telemetry
        self.events = events
        self.user = user
        self.password = password

    def on_start(self, event):
        conn = event.container.connect(
            self.server, user=self.user, password=self.password)
        event.container.create_receiver(conn, source=self.telemetry)
        event.container.create_receiver(conn, source=self.events)

    def on_message(self, event):
        try:
            body = json.loads(event.message.body)
            if 'topic' in body:
                if body['topic'] == 'meeting-room-assistant':
                    print('yay')
                if body['topic'] == 'bcx/xdk.7cec79d330df/things/twin/commands/modify':
                    print('yay')
        except json.decoder.JSONDecodeError as e:
            pass


with open('../settings.json') as data_file:
    settings = json.load(data_file)
hono = settings['hono']
Container(HelloWorld(hono['server'], hono['telemetry'], hono[
          'events'], hono['user'], hono['password'])).run()
