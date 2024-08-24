import random
import redis
from flask import Flask, jsonify
from redis import ConnectionPool
from threading import Lock

app = Flask(__name__)

# 创建Redis连接池
pool = ConnectionPool(host='redis', port=6379, db=5)
# pool = ConnectionPool(host='192.168.20.250', port=6379, db=5)
redis_conn = redis.Redis(connection_pool=pool)

# 锁机制
lock = Lock()


class NodeValue:
    def __init__(self, worker, value):
        self.worker = worker
        self.value = value


def get_data_from_redis(token):
    with lock:
        range_ = random.randint(50, 100)
        data = redis_conn.lrange(f'{token}_values', 0, range_)  # 获取最新的5条记录
        # print(data)
        if data:
            data = [float(item.decode('utf-8')) for item in data]
        return data


def calculate_value(data):
    if data:
        min_value = min(data)
        max_value = max(data)
        range_ = random.randint(2, 12)
        # print("max:", max_value, "min:", min_value)
        return round(random.uniform(min_value, max_value), range_)
    return None


@app.route('/', methods=['GET'])
def health():
    return "Hello, World, I'm alive!"


@app.route('/inference/<token>', methods=['GET'])
def get_inference(token):
    data = get_data_from_redis(token)
    value = calculate_value(data)
    if value is not None:
        return str(value)
    return "Error: No data available", 500


@app.route('/forecast', methods=['GET'])
def get_forecast():
    data = get_data_from_redis(token)
    if data:
        node_values = [
            NodeValue("Worker1", str(calculate_value(data))),
            NodeValue("Worker2", str(calculate_value(data))),
            NodeValue("Worker3", str(calculate_value(data))),
        ]
        return jsonify([nv.__dict__ for nv in node_values])
    return "Error: No data available", 500


@app.route('/truth/<token>/<blockheight>', methods=['GET'])
def get_truth(token, blockheight):
    data = get_data_from_redis(token)
    value = calculate_value(data)
    if value is not None:
        return str(value)
    return "Error: No data available", 500


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=6000)
