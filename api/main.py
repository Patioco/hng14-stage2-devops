import os
import time
import uuid
import redis
from fastapi import FastAPI, HTTPException


app = FastAPI()


# Environment variables
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
QUEUE_NAME = "jobs"


# Global Redis client (lazy init)
redis_client = None


def get_redis():
    global redis_client
    if redis_client:
        return redis_client

    for _ in range(10):
        try:
            redis_client = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                password=REDIS_PASSWORD,
                decode_responses=True
            )
            redis_client.ping()
            return redis_client
        except redis.exceptions.ConnectionError:
            time.sleep(2)

    raise Exception("Could not connect to Redis")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/jobs")
def create_job():
    try:
        r = get_redis()
        job_id = str(uuid.uuid4())

        r.lpush(QUEUE_NAME, job_id)
        r.hset(f"job:{job_id}", mapping={"status": "queued"})

        return {"job_id": job_id}

    except redis.exceptions.RedisError:
        raise HTTPException(status_code=500, detail="Redis error")


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    r = get_redis()

    status = r.hget(f"job:{job_id}", "status")

    if not status:
        raise HTTPException(status_code=404, detail="Job not found")

    return {"job_id": job_id, "status": status}
