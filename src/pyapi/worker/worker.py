import json
from typing import Dict, Any, Tuple, Callable
from src.pyapi.brokers.redis import RedisClient
from src.pyapi.common.generic_models import GenericResults
from src.pyapi.common.consts import DATA, TASK_ID, TASK_DATA, TYPE, MESSAGE


class Worker:

    def __init__(self, task_queue: str, redis_client: RedisClient = None, work_function: Callable = None):
        """
            Initialize the Worker with the Redis client, task queue, and an optional custom _work function.
            :param task_queue: The task queue name
            :param redis_client: The Redis client instance can be defined as env vars
            :param work_function: A custom function to process task data. If None, the default _work method is used.
        """
        self.redis_client = redis_client if redis_client else RedisClient()
        self.task_queue = task_queue
        self._work = work_function or self._work

    def _work(self, task_data: Dict[str, Any]):
        """
            The default task processing method. Can be replaced by a user-defined function.
        """
        try:
            task_data = task_data
            results = task_data['param1'] + task_data['param2']
            return results
        except Exception as e:  # Handle exception in worker
            return str(e)

    def _parse_task(self, message) -> Tuple[str, Dict[str, Any]]:
        """
            Parses the incoming message from the Redis pub/sub and extracts the task ID and payload.
        """
        task_payload = json.loads(message[DATA])
        task_id = task_payload[TASK_ID]
        task_payload = task_payload[TASK_DATA]
        return task_id, task_payload

    def start_worker(self):
        """
            Starts the worker, subscribes to the task queue, and processes tasks.
            The worker will publish the results payload of the BaseModel GenericResults
        """
        print("Worker started")
        pubsub = self.redis_client.subscribe(self.task_queue)
        for message in pubsub.listen():
            if message[TYPE] == MESSAGE:
                task_id, task_payload = self._parse_task(message)
                print(f"Processing task {task_id} with data: {task_payload}")
                result = self._work(task_payload)
                self.redis_client.publish(task_id, GenericResults(**{"results": result}))
                print(f"Task {task_id} processed, result sent.")
        pubsub.close()
