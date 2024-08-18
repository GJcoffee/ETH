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


def update_data(redis_conn, key, value):
    redis_conn.lpush(key, value)
    redis_conn.ltrim(key, 0, 4)  # 保留最近的5条记录


def fetch_and_store_data(redis_conn, crypto_symbol, key):
    http = tls_client.Session(random_tls_extension_order=True)
    params = {
        'cryptoSymbol': crypto_symbol,
        'fiatSymbol': 'USD',
        'amount': '1',
        'reversed': 'false',
    }
    response = http.get('https://ticker-api.cointelegraph.com/converter/rate', params=params, headers=headers)
    value = float(response.json()['rate'])
    update_data(redis_conn, key, value)
    data = redis_conn.lrange(key, 0, 4)
    print(f'{crypto_symbol}:', data)
    time.sleep(5)


def main_loop():
    try:
        with redis.Redis(host='redis', port=6379, db=5) as redis_conn:
        # with redis.Redis(host='192.168.20.250', port=6379, db=5) as redis_conn:
            while True:
                fetch_and_store_data(redis_conn, 'ETH', 'ETH_values')
                fetch_and_store_data(redis_conn, 'BTC', 'BTC_values')
                fetch_and_store_data(redis_conn, 'BNB', 'BNB_values')
                fetch_and_store_data(redis_conn, 'SOL', 'SOL_values')
                fetch_and_store_data(redis_conn, 'ARB', 'ARB_values')
                fetch_and_store_data(redis_conn, 'MEME', 'MEME_values')

                time.sleep(1 * 60)  # 等待1分钟后再次循环
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main_loop()
