import dramatiq
import os
from dotenv import load_dotenv
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.brokers.stub import StubBroker
load_dotenv()
def set_host():
    broker = RabbitmqBroker(
        host=os.getenv("RABBITMQ_HOST"),
    )
    dramatiq.set_broker(broker)

set_host()

from app.background_tasks.example_task import example_task