import redis
import json
from datetime import datetime
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

class RedisSessionMemoryManager:
    def __init__(self, host='localhost', port=6379, db=0,
                 max_history=3, session_ttl=3600*24*30):
        """
        host, port, db       : Redis 连接参数
        max_history          : 每个会话最多保留消息条数
        session_ttl          : 会话过期时间，单位秒
        """
        self.r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        self.max_history = max_history
        self.session_ttl = session_ttl

    def _key(self, user_id):
        return f"chat:{user_id}"

    def get_context(self, user_id, limit=None):
        """获取最近 limit 条消息"""
        key = self._key(user_id)
        start = -limit if limit else -self.max_history
        msgs = self.r.lrange(key, start, -1)
        return [json.loads(m) for m in msgs]

    def save_message(self, user_id, role, content):
        """保存一条消息，同时更新 TTL 并截断历史"""
        key = self._key(user_id)
        entry = json.dumps({
            "role": role,
            "content": content
        })
        self.r.rpush(key, entry)
        self.r.ltrim(key, -self.max_history, -1)
        self.r.expire(key, self.session_ttl)

    def delete_session(self, user_id):
        """删除指定会话"""
        key = self._key(user_id)
        return self.r.delete(key) > 0

