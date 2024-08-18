import random
import time

import redis
import tls_client

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'origin': 'https://cn.cointelegraph.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://cn.cointelegraph.com/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}
"""https://cn.cointelegraph.com/ethereum-price?fiatSymbol=USD"""
while True:
    try:
        # with redis.Redis(host='192.168.20.250', port=6379, db=5) as redis_conn:
        with redis.Redis(host='redis', port=6379, db=5) as redis_conn:
            http = tls_client.Session(random_tls_extension_order=True)
            """ETH"""
            params = {
                'cryptoSymbol': 'ETH',
                'fiatSymbol': 'USD',
                'amount': '1',
                'reversed': 'false',
            }
            response = http.get('https://ticker-api.cointelegraph.com/converter/rate', params=params, headers=headers)
            value = response.json()['rate']
            data_range = (float(value) + 2, float(value) - 2)
            print(data_range)
            # 将范围存入redis
            redis_conn.set('ETH_range', str(data_range))
            data = eval(str(redis_conn.get('data_range')).replace("b'", '').replace("'", ''))
            print('ETH:', data)
            time.sleep(5)

            """BTC"""
            params = {
                'cryptoSymbol': 'BTC',
                'fiatSymbol': 'USD',
                'amount': '1',
                'reversed': 'false',
            }
            response = http.get('https://ticker-api.cointelegraph.com/converter/rate', params=params, headers=headers)
            value = response.json()['rate']
            data_range = (float(value) + 2, float(value) - 2)
            print(data_range)
            # 将范围存入redis
            redis_conn.set('BTC_range', str(data_range))
            data = eval(str(redis_conn.get('BTC_range')).replace("b'", '').replace("'", ''))
            print('BTC:', data)
            time.sleep(5)

            """BNB"""
            params = {
                'cryptoSymbol': 'BNB',
                'fiatSymbol': 'USD',
                'amount': '1',
                'reversed': 'false',
            }
            response = http.get('https://ticker-api.cointelegraph.com/converter/rate', params=params, headers=headers)
            value = response.json()['rate']
            data_range = (float(value) + 1, float(value) - 1)
            print(data_range)
            # 将范围存入redis
            redis_conn.set('BNB_range', str(data_range))
            data = eval(str(redis_conn.get('BNB_range')).replace("b'", '').replace("'", ''))
            print('BNB:', data)
            time.sleep(5)

            """SOL"""
            params = {
                'cryptoSymbol': 'SOL',
                'fiatSymbol': 'USD',
                'amount': '1',
                'reversed': 'false',
            }
            response = http.get('https://ticker-api.cointelegraph.com/converter/rate', params=params, headers=headers)
            value = response.json()['rate']
            data_range = (float(value) + 1, float(value) - 1)
            print(data_range)
            # 将范围存入redis
            redis_conn.set('SOL_range', str(data_range))
            data = eval(str(redis_conn.get('SOL_range')).replace("b'", '').replace("'", ''))
            print('SOL:', data)
            time.sleep(5)

            """ARB"""
            params = {
                'cryptoSymbol': 'ARB',
                'fiatSymbol': 'USD',
                'amount': '1',
                'reversed': 'false',
            }
            response = http.get('https://ticker-api.cointelegraph.com/converter/rate', params=params, headers=headers)
            value = response.json()['rate']
            data_range = (float(value) + 0.01, float(value) - 0.01)
            print(data_range)
            # 将范围存入redis
            redis_conn.set('ARB_range', str(data_range))
            data = eval(str(redis_conn.get('ARB_range')).replace("b'", '').replace("'", ''))
            print('ARB:', data)
            time.sleep(5)

            """MEME"""
            params = {
                'cryptoSymbol': 'MEME',
                'fiatSymbol': 'USD',
                'amount': '1',
                'reversed': 'false',
            }
            response = http.get('https://ticker-api.cointelegraph.com/converter/rate', params=params, headers=headers)
            value = response.json()['rate']
            data_range = (float(value) + 0.0001, float(value) - 0.0001)
            print(data_range)
            # 将范围存入redis
            redis_conn.set('MEME_range', str(data_range))
            data = eval(str(redis_conn.get('MEME_range')).replace("b'", '').replace("'", ''))
            print('MEME:', data)

            time.sleep(3 * 60)

    except Exception as e:
        print(e)
