from kombu import Exchange, Queue, Connection

task_exchange = Exchange('tasks', type="direct")

task_queues = [
    Queue('numbers', task_exchange, routing_key='numbers'),
]
