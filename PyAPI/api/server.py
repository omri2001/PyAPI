import json
from PyAPI.brokers.redis import RedisClient
from PyAPI.common.consts import DATA, TYPE, MESSAGE
from PyAPI.common.generic_models import GenericResults, GenericRequest


class APIGateway:
    def __init__(self, task_queue: str, redis_client: RedisClient = None):
        """
            Initialize the server with the Redis client and task queue
            :param task_queue: The task queue name
            :param redis_client: The Redis client instance can be defined as env vars
        """
        self.redis_client = redis_client if redis_client else RedisClient()
        self.task_queue = task_queue

    def publish_task(self, task_payload: GenericRequest, task_id: str) -> GenericResults:
        """
            ! The task payload should be GenericRequest model
            publish task to the given task queue
            param: task_payload: the task
            param: task_id: unique id for the client session like uuid4() string
        """
        self.redis_client.publish(self.task_queue, task_payload)
        result = self._listen_for_result(task_id)
        return result

    def _listen_for_result(self, task_id: str) -> GenericResults:
        """
            wait for the results
            param: task_id: the unique task_id
            return: payload from the format -> {'results':your results}
        """
        pubsub = self.redis_client.subscribe(task_id)
        for message in pubsub.listen():
            if message and message[TYPE] == MESSAGE:
                result = json.loads(message[DATA])
                pubsub.close()
                return result
