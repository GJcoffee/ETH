import requests

for _ in range(100):
    res = requests.get('http://5.104.86.219:9303/inference/ETH')
    print(res.text)
    res = requests.get('http://109.123.230.168:6000/inference/ETH')
    print(res.text)