from flask import Flask, request, jsonify
import json, requests, fake_headers

proxy = Flask(__name__)

@proxy.route('/', methods=['GET'])
def root():
    return 'Proxy is running.'

fh = fake_headers.Headers()

@proxy.route('/task', methods=['POST'])
def task():
    json_data = request.json
    if json_data is None:
        return jsonify({'errorCode': '1', 'errorMessage': 'No json to process.'}), 400
    
    url = json_data.get('url')
    method = json_data.get('method')
    request_json = json_data.get('json', {})
    request_data = json_data.get('data', {})
    headers = json_data.get('headers') or {}
    ua = fh.generate()
    ua_value = None
    for k, v in ua.items():
        if k.lower() == 'user-agent':
            ua_value = v
            break
    headers.setdefault('user-agent', ua_value)

    return_statuscode = json_data.get('return_statuscode', True)
    return_text = json_data.get('return_text', True)
    return_json = json_data.get('return_json', True)
    return_headers = json_data.get('return_headers', True)

    if None in [url, method]:
        return jsonify({'errorCode': '2', 'errorMessage': 'Missing required parameter.'}), 400

    method = method.upper()
    headers.setdefault('Content-Type', '*/*' if method == 'POST' else 'application/json')

    if not (url.startswith('http://') or url.startswith('https://')):
        url = f'https://{url}'

    try:
        response = requests.request(method, url, json=request_json, data=request_data, headers=headers)
    except Exception as e:
        return jsonify({'errorCode': '3', 'errorMessage': f'An error occurred: {e}'}), 500

    payload = {}

    if return_statuscode:
        payload['status_code'] = response.status_code

    if return_headers:
        payload['headers'] = dict(response.headers)

    if return_text:
        content_type = response.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            try:
                payload['text'] = json.dumps(response.json(), indent=2)
            except Exception:
                payload['text'] = response.text
        else:
            payload['text'] = response.text

    if return_json:
        try:
            payload['json'] = response.json()
        except Exception:
            payload['json'] = None

    return jsonify(payload)

if __name__ == '__main__':
    proxy.run(host='0.0.0.0', port=2555)
