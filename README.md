# PyAPI - Task Distribution System with Redis and FastAPI

**PyAPI** is a Python SDK designed to streamline the creation of task distribution systems using Redis for messaging and FastAPI (or any API framework) for HTTP request handling. The package allows developers to create an API that publishes tasks to Redis, processes them asynchronously with worker processes, and retrieves results back via Redis Pub/Sub.

## Features

- **FastAPI Integration**: Quickly set up an API to submit tasks to Redis for processing.
- **Redis Pub/Sub**: Utilize Redis as a message broker to distribute tasks and collect results.
- **Asynchronous Task Processing**: Tasks are processed asynchronously by worker processes.
- **Easy Integration**: Can be used with FastAPI or any other Python API framework.
- **Custom Worker Logic**: Workers can process tasks and push results back to Redis.

## Installation

clone the repo and follow the commands:

```bash
python setup.py sdist bdist_wheel  
cd ./dist 
pip install PyAPI-0.0.1-py3-none-any.whl
```

## Redis configuration
supply the redis credentials in init of APIGateway and Worker or as env vars\
REDIS_HOST\
REDIS_PORT\
REDIS_DB
## Example Usage on server
task_id = str(uuid.uuid4())\
task_payload = {TASK_ID: task_id,
                TASK_DATA: task.task_data.model_dump()}\
results = APIGateway(TASK_QUEUE_CHANNEL).publish_task(GenericRequest(**task_payload), task_id)
## Example Usage on worker
def calculate(task_data: Dict[str, Any]) -> int:\
    results = task_data['param1'] / task_data['param2']\
    return results


if __name__ == "__main__":\
    worker = Worker(TASK_QUEUE_CHANNEL,work_function=calculate)\
    worker.start_worker()

