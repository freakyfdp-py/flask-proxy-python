# Python HTTP Proxy Using Flask & Requests

To test the proxy:
* Replace the url in the `url` file
* Make sure the proxy is online and the port is forwarded on the machine running it
* And just run the test

this proxy isnt an ordinary proxy that you would be using in for example in the requests module like this 
```python3
import requests

proxies = {
  'http': f'http://127.0.0.1:2555',
  'https': f'http://127.0.0.1:2555'
]

responce = requests.get('https://example.org/', proxies=proxies)
print(responce.text)
```

but its rather a proxy that you made an HTTP request to.
I suggest you to just look at the `test.py` code !
