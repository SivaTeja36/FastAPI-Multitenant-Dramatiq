import os
from dotenv import load_dotenv
import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker

load_dotenv()


def set_host():
    broker = RabbitmqBroker(
        host=os.getenv("RABBITMQ_HOST"),
    )
    dramatiq.set_broker(broker)

set_host()

from app.background_tasks.example_task import example_task