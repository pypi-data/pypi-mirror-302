import requests

r = requests.get('http://ipinfo.io')
with open('/root/ttt.txt', 'w') as f:
    f.write(r.text)
