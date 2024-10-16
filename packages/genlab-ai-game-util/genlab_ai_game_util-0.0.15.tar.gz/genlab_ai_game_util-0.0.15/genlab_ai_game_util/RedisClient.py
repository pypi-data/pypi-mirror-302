import atexit
import redis


class RedisClient:
    # 单例
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(RedisClient, cls).__new__(cls)
        return cls._instance

    def __init__(self, host, port, password, socket_timeout=3, socket_connect_timeout=3):
        self.redis_client = None
        # 注册退出钩子
        atexit.register(self.graceful_exit)
        try:
            self.connect(host, port, password, socket_timeout, socket_connect_timeout)
        except Exception as e:
            print(f'redis connect failed.{e}')

    def graceful_exit(self):
        print("start Closing Redis connection...")
        self.disconnect()
        print("finish Closing Redis connection...")

    def connect(self, host, port, password, socket_timeout, socket_connect_timeout):
        if self.redis_client is None:
            self.redis_client = redis.Redis(
                host=host,
                port=port,
                password=password,
                socket_timeout=socket_timeout,
                socket_connect_timeout=socket_connect_timeout)
            pong = self.redis_client.ping()
            print(f"redis connect ok:{pong}")

    def disconnect(self):
        try:
            if self.redis_client is not None:
                self.redis_client.close()
                self.redis_client = None
                print("redis disconnect")
        except Exception as e:
            print(f"redis disconnect:{e}")

    # redis中是否存在某个key
    def exists(self, key):
        try:
            return {'code': 0, 'result': self.redis_client.exists(key)}
        except Exception as e:
            print(f"exists:{e}")
            return {'code': 1, 'result': e}

    # redis让某个key自增
    def inc(self, key):
        try:
            return {'code': 0, 'result': self.redis_client.incr(key)}
        except Exception as e:
            print(f"inc:{e}")
            return {'code': 1, 'result': e}

    # 写入kv
    def set_kv(self, key, value, expire_second=0):
        try:
            if expire_second == 0:
                return {'code': 0, 'result':self.redis_client.set(key, value)}
            return {'code': 0, 'result': self.redis_client.set(key, value, ex=expire_second)}
        except Exception as e:
            print(f"set_kv:{e}")
            return {'code': 1, 'result': e}

    # 读取kv
    def get_kv(self, key):
        try:
            value = self.redis_client.get(key)
            # 如果返回的是字节类型，转换为字符串
            if value:
                return {'code': 0, 'result': value.decode('utf-8')}
            else:
                return {'code': 0, 'result': None}
        except Exception as e:
            print(f"get_kv:{e}")
            return {'code': 1, 'result': e}

    # 删除某个key
    def del_key(self, key):
        try:
            return {'code': 0, 'result': self.redis_client.delete(key)}
        except Exception as e:
            print(f"del_key:{e}")
            return {'code': 1, 'result': e}

    # 写入hash
    def set_hash(self, name, hash):
        try:
            return {'code': 0, 'result': self.redis_client.hset(name, mapping=hash)}
        except Exception as e:
            print(f"set_hash:{e}")
            return {'code': 1, 'result': e}

    # 读取全部hash
    def get_hash_all(self, name):
        try:
            hash_data = self.redis_client.hgetall(name)
            if hash_data is None:
                return {'code': 0, 'result': None}
            else:
                return {'code': 0, 'result': {key.decode('utf-8'): value.decode('utf-8') for key, value in hash_data.items()}}
        except Exception as e:
            print(f"get_hash_all:{e}")
            return {'code': 1, 'result': e}

    # 读取hash某个key
    def get_hash_by_key(self, name, key):
        try:
            hash_data = self.redis_client.hget(name, key)
            if hash_data is None:
                return {'code': 0, 'result': None}
            else:
                return {'code': 0, 'result': hash_data.decode('utf-8')}
        except Exception as e:
            print(f"get_hash_by_key:{e}")
            return {'code': 1, 'result': e}

    # 删除hash某个key
    def del_hash_by_key(self, name, key):
        try:
            return {'code': 0, 'result': self.redis_client.hdel(name, key)}
        except Exception as e:
            print(f"del_hash_by_key:{e}")
            return {'code': 1, 'result': e}
