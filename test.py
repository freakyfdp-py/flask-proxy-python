import requests, json, os

os.system('cls' if os.name == 'nt' else 'clear')

with open('./url', 'r') as f:
    BASE_URL = f'{f.read()}'

tests = [
    {
        'name': 'GET with JSON response',
        'payload': {
            'method': 'GET',
            'url': 'api.ipify.org?format=json',
            'return_headers': True,
            'return_statuscode': True,
            'return_text': True,
            'return_json': True
        }
    },
    {
        'name': 'GET with TEXT response fallback',
        'payload': {
            'method': 'GET',
            'url': 'api.ipify.org?format=text',
            'return_headers': True,
            'return_statuscode': True,
            'return_text': True,
            'return_json': True
        }
    },
    {
        'name': 'GET with no return_headers',
        'payload': {
            'method': 'GET',
            'url': 'api.ipify.org?format=json',
            'return_headers': False
        }
    },
    {
        'name': 'GET with no return_statuscode',
        'payload': {
            'method': 'GET',
            'url': 'api.ipify.org?format=json',
            'return_statuscode': False
        }
    },
    {
        'name': 'GET with no return_text',
        'payload': {
            'method': 'GET',
            'url': 'api.ipify.org?format=json',
            'return_text': False
        }
    },
    {
        'name': 'GET with no return_json',
        'payload': {
            'method': 'GET',
            'url': 'api.ipify.org?format=json',
            'return_json': False
        }
    },
    {
        'name': 'POST with JSON payload',
        'payload': {
            'method': 'POST',
            'url': 'postman-echo.com/post',
            'json': {'test': 'value'},
            'return_headers': True,
            'return_statuscode': True,
            'return_text': True,
            'return_json': True
        }
    },
    {
        'name': 'POST with data payload',
        'payload': {
            'method': 'POST',
            'url': 'postman-echo.com/post',
            'data': {'key': 'value'},
            'return_headers': True,
            'return_statuscode': True,
            'return_text': True,
            'return_json': True
        }
    },
]

for test in tests:
    print(f"=== {test['name']} ===")
    response = requests.post(
        BASE_URL,
        headers={'Content-Type': 'application/json'},
        json=test['payload']
    )
    proxy_response = response.json()

    text_field = proxy_response.get('text')
    if text_field is not None:
        try:
            parsed_text = json.loads(text_field)
            proxy_response['text'] = parsed_text
        except Exception:
            pass

    print(json.dumps(proxy_response, indent=2, ensure_ascii=False))
