import random
import redis
from flask import Flask, jsonify
from redis import ConnectionPool
from threading import Lock

app = Flask(__name__)

# 创建Redis连接池
pool = ConnectionPool(host='redis', port=6379, db=5)
redis_conn = redis.Redis(connection_pool=pool)

# 锁机制
lock = Lock()


class NodeValue:
    def __init__(self, worker, value):
        self.worker = worker
        self.value = value


def get_data_from_redis(token):
    with lock:
        data = redis_conn.get(f'{token}_range')
        if data:
            data = eval(data.decode('utf-8'))
        return data


@app.route('/', methods=['GET'])
def health():
    return "Hello, World, I'm alive!"


@app.route('/inference/<token>', methods=['GET'])
def get_inference(token):
    data = get_data_from_redis(token)
    if data:
        value = round(random.uniform(data[0], data[-1]), 12)
        return str(value)
    return "Error: No data available", 500


@app.route('/forecast', methods=['GET'])
def get_forecast():
    data = get_data_from_redis(token)
    if data:
        node_values = [
            NodeValue("Worker1", str(round(random.uniform(data[0], data[-1]), 12))),
            NodeValue("Worker2", str(round(random.uniform(data[0], data[-1]), 12))),
            NodeValue("Worker3", str(round(random.uniform(data[0], data[-1]), 12))),
        ]
        return jsonify([nv.__dict__ for nv in node_values])
    return "Error: No data available", 500


@app.route('/truth/<token>/<blockheight>', methods=['GET'])
def get_truth(token, blockheight):
    data = get_data_from_redis(token)
    if data:
        value = round(random.uniform(data[0], data[-1]), 12)
        return str(value)
    return "Error: No data available", 500


if __name__ == '__main__':
    from gevent.pywsgi import WSGIServer

    http_server = WSGIServer(('0.0.0.0', 6000), app)
    http_server.serve_forever()
