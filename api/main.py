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

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/jobs")
def create_job():
    try:
        job_id = str(uuid.uuid4())
        r.lpush(QUEUE_NAME, job_id)
        r.hset(f"job:{job_id}", mapping={"status": "queued"})
        return {"job_id": job_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    status = r.hget(f"job:{job_id}", "status")
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job_id, "status": status}