import time
import redis
import requests
from loguru import logger


def get_ip():
    while True:
        try:
            res = requests.get(f'http://192.168.20.104:19999/rand-ip')
            data = res.json()
            proxy = f'http://{data["host"]}:{data["port"]}'
            # print(proxy)
            proxies = {'http': proxy, 'https': proxy}
            res1 = requests.get("https://task.bsquared.network/points/", proxies=proxies, timeout=3)
            if res1.status_code == 200:
                return proxy
            # return 'http://127.0.0.1:10809'
        except:
            pass


def get_proxies():
    try:
        proxy = get_ip()
        proxies = {"http": proxy, "https": proxy}
        # proxies = {"http": "http://127.0.0.1:10809", "https": "http://127.0.0.1:10809"}
        return proxies
        # return {}
    except:
        pass


# proxies=get_proxies()

# 设置请求的URL和Redis连接信息
BINANCE_BASE_URL = "https://api.binance.com"
TICKER_ENDPOINT = "/api/v3/ticker/price"
SYMBOLS = '["ETHUSDT","BTCUSDT","BNBUSDT","SOLUSDT","ARBUSDT","MEMEUSDT"]'

# Redis连接配置
REDIS_HOST = 'redis'  # 修改为你的Redis服务器地址
REDIS_PORT = 6379
REDIS_DB = 5


def update_data(redis_conn, key, value):
    """更新Redis中的价格数据，保留最近的5条记录"""
    redis_conn.lpush(key, value)
    redis_conn.ltrim(key, 0, 4)  # 只保留最新的5条记录


def fetch_and_store_data(redis_conn):
    """从Binance API获取最新的价格并存储到Redis"""
    url = f"{BINANCE_BASE_URL}{TICKER_ENDPOINT}?symbols={SYMBOLS}"
    # response = requests.get(url, proxies=proxies)
    response = requests.get(url)

    if response.status_code == 200:
        prices = response.json()
        for price_info in prices:
            symbol = price_info['symbol'].replace('USDT', '')
            price = float(price_info['price'])
            key = f"{symbol}_values"
            update_data(redis_conn, key, price)
            data = redis_conn.lrange(key, 0, 2)
            logger.info(f'{symbol}:{data}')
    else:
        logger.error(f"Failed to fetch prices. Status Code: {response.status_code}")


def main_loop():
    """主循环，从Binance API定期获取数据并存储到Redis"""
    try:
        with redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB) as redis_conn:
            while True:
                fetch_and_store_data(redis_conn)
                time.sleep(6)  # 等待1分钟后再次循环
    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main_loop()
