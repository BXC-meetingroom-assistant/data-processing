import requests

urls = {
    'on': 'https://maker.ifttt.com/trigger/bad_air/with/key/nTlnK3gknAAXc0meB96ot1hidkPnyEJnuX2BrSO6CXz',
    'off': 'https://maker.ifttt.com/trigger/good_air/with/key/nTlnK3gknAAXc0meB96ot1hidkPnyEJnuX2BrSO6CXz'
}


def check_status_code(url):
    request = requests.get(url)
    if request.status_code == '200':
        return True
    else:
        return False


def enable():
    return(check_status_code(urls['on']))


def disable():
    return(check_status_code(urls['off']))
