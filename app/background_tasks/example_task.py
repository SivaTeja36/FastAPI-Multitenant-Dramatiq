import dramatiq

@dramatiq.actor(max_retries=3)
def example_task():
    print("Background tas executed in dramatiq")