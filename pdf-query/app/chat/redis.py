import os
import redis


client = redis.Redis.from_url(
  os.environ('REDIS_URI'),
  decode_response=True  # byte based data from Redis will be converted to Python strings
)