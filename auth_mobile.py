import uuid, time, os, requests

AUTH_KEY = "MDE5ZTRmY2EtMzhmMy03OTkzLWE1YjItNWQyNmI4N2NiODQ5OjI3YWRiZTg3LTk4NmUtNDM4OS1iYTk4LWU5ODAwMWMwNjU2Mg=="

TOKEN_CACHE = {'token': None, 'expires': 0}

def get_token():
    if TOKEN_CACHE['token'] and time.time() < TOKEN_CACHE['expires']:
        return TOKEN_CACHE['token']
    try:
        r = requests.post(
            'https://ngw.devices.sberbank.ru:9443/api/v2/oauth',
            headers={'RqUID': str(uuid.uuid4()),
                     'Content-Type': 'application/x-www-form-urlencoded',
                     'Authorization': f'Basic {AUTH_KEY}'},
            data={'scope': 'GIGACHAT_API_PERS'},
            verify=False, timeout=10)
        token = r.json().get('access_token')
        TOKEN_CACHE['token'] = token
        TOKEN_CACHE['expires'] = time.time() + 1500
        return token
    except:
        return None
