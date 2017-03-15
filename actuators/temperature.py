import requests

import json

with open('../settings.json') as data_file:
    settings = json.load(data_file)

base_url = settings['base_url']
device_id = settings['device_id']
token = settings['token']


def device_put(endpoint, json_data):
    url = '{}/{}/{}'.format(base_url, device_id, endpoint)
    headers = {'Authorization': 'Bearer {}'.format(token)}
    return requests.put(url, headers=headers, json=json_data)


def device_get(endpoint):
    url = '{}/{}/{}'.format(base_url, device_id, endpoint)
    headers = {'Authorization': 'Bearer {}'.format(token)}
    return requests.get(url, headers=headers)


def get_mode():
    return(device_get('heatingCircuits/hc1/usermode').json()['value'])


def set_manual():
    data = {'value': 'manual'}
    return(device_put('/heatingCircuits/hc1/usermode', data).status_code)


def get_room_temperature():
    return(device_get('heatingCircuits/hc1/roomtemperature').json()['value'])


def get_manual_temperature():
    return(device_get('heatingCircuits/hc1/temperatureRoomManual').json()['value'])
    pass


def set_manual_temperature(temperature):
    data = {"value": temperature}
    if get_mode() == 'clock':
        set_manual()
    return device_put('heatingCircuits/hc1/temperatureRoomManual', data).status_code


if __name__ == '__main__':
    print(set_manual_temperature(22.5))
    print(get_manual_temperature())
    print(get_room_temperature())
