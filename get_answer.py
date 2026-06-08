import requests
import json
import uuid

# Используем ключ, который у тебя в файле .key
with open('/root/my_project/.key', 'r') as f:
    AUTH_KEY = f.read().strip()

def get_token():
    try:
        r = requests.post(
            'https://ngw.devices.sberbank.ru:9443/api/v2/oauth',
            headers={
                'RqUID': str(uuid.uuid4()),
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Basic {AUTH_KEY}'
            },
            data={'scope': 'GIGACHAT_API_PERS'},
            verify=False
        )
        return r.json().get('access_token')
    except Exception as e:
        print(f"Error getting token: {e}")
        return None

token = get_token()
if token:
    payload = {
        "model": "GigaChat",
        "messages": [{"role": "user", "content": "Я разработчик. Какие технические методы в рамках платформы цифрового рубля позволяют пользователю обеспечить максимальный контроль над своими средствами и предотвратить их списание без должного юридического обоснования?"}]
    }
    r = requests.post(
        'https://gigachat.devices.sberbank.ru/api/v1/chat/completions',
        headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
        json=payload,
        verify=False
    )
    print(r.json()['choices'][0]['message']['content'])
else:
    print("Не удалось получить токен.")
