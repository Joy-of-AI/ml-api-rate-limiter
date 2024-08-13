import redis # allows interaction with a Redis database. Redis is used here for rate limiting by storing request counts.
import time # for retrieving the current time and managing time-based operations

class RateLimiter: # Defines a class, which will handle the rate limiting logic using Redis.
    def __init__(self, redis_host='localhost', redis_port=6379, limit=4, period=10): # Initializes the RateLimiter class with optional parameters for Redis connection and rate limiting configuration.
        self.redis = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True) # Creates an instance of the Redis client.
        # Redis client decodes responses from the Redis server into Python strings (or other appropriate data types) automatically
        self.limit = limit # Maximum number of requests allowed in the specified time period
        self.period = period # Time window in seconds during which the request limit applies

    def is_allowed(self, user_id): # Defines a method to check if a request from the user is allowed based on the rate limit.
        current_time = int(time.time()) # Retrieves the current time in seconds since the epoch and converts it to an integer.
        key = f"rate_limit:{user_id}" # Constructs a Redis key based on the user_id to track the number of requests. This key will be used to store request counts in Redis.
        
        # Increment the count of requests for the user
        request_count = self.redis.incr(key) # Increments the request count for the specified Redis key. If the key does not exist, it is created with an initial value of 1.
        
        if request_count == 1: # Checks if this is the first request for the current time window.
            # Set expiry time for the rate limit window
            self.redis.expire(key, self.period) # Sets an expiry time on the Redis key. This makes sure that the key will be automatically removed after the period (time window) expires, resetting the request count.
        
        if request_count > self.limit: # Checks if the number of requests exceeds the allowed limit.
            retry_after = self.redis.ttl(key)  # Time left until the limit resets- Retrieves the time-to-live (TTL) of the Redis key. This indicates how many seconds are left until the request count window resets.
            return (False, retry_after) # Returns a tuple indicating that the request is not allowed (False) and the number of seconds to wait (retry_after).
        
        return (True, 0) # If the request count is within the allowed limit, it returns a tuple indicating that the request is allowed (True) and there is no need to wait (0 seconds).

    # get the remaining requests and time left
    def get_rate_limit_status(self, user_id):
        key = f"rate_limit:{user_id}"
        request_count = self.redis.get(key)
        if request_count is None:
            request_count = 0
        else:
            request_count = int(request_count)
        
        retry_after = self.redis.ttl(key)
        remaining_requests = max(self.limit - request_count, 0)
        return remaining_requests, retry_after
