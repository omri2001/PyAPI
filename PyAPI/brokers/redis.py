import os
import json
import redis
from typing import Union
from PyAPI.common.generic_models import GenericRequest, GenericResults


class RedisClient:

    def __init__(self, host: str = None, port: int = None, db: int = None):
        """
            Initialize the RedisClient with the host port and db
            :param host: host str
            :param port: port int
            :param db: db int
        """
        self.redis_client = redis.Redis(host=os.getenv("REDIS_HOST", default=host),
                                        port=os.getenv("REDIS_PORT", default=port),
                                        db=os.getenv("REDIS_DB", default=db))
        self.is_connected()

    def is_connected(self) -> bool:
        """
            check if redis is reachable
        """
        try:
            return self.redis_client.ping()
        except redis.ConnectionError as e:
            print(e)

    def publish(self, task_queue: str, task: Union[GenericRequest, GenericResults]):
        """
            publish task to the given task queue
        """
        self.redis_client.publish(task_queue, json.dumps(task.model_dump()))

    def subscribe(self, queue: str):
        """
            return a redis pubsub for the given queue
        """
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe(queue)
        return pubsub
