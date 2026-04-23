import redis
import time
import os
import signal


REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
QUEUE_NAME = "jobs"


# Redis connection with retry
def get_redis():
    for _ in range(10):
        try:
            r = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                password=REDIS_PASSWORD,
                decode_responses=True
            )
            r.ping()
            return r
        except redis.exceptions.ConnectionError:
            time.sleep(2)
    raise Exception("Could not connect to Redis")


r = get_redis()

running = True


def shutdown(sig, frame):
    global running
    print("Shutting down worker...")
    running = False


signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)


def process_job(job_id):
    print(f"Processing job {job_id}")
    try:
        time.sleep(2)  # simulate work
        r.hset(f"job:{job_id}", mapping={"status": "completed"})
        print(f"Done: {job_id}")
    except Exception as e:
        print(f"Error processing job {job_id}: {e}")


print("Worker started, waiting for jobs...")


while running:
    job = r.brpop(QUEUE_NAME, timeout=5)
    if job:
        _, job_id = job
        process_job(job_id)
        