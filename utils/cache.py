# utils/cache.py helper to manage cache access

# Add caching at the genre server level
# When a genre server receives a request,it:
    # returns data from the cache if availabe and not expired
    # Otherwise, queries the DB, caches the result, and returns it

# Use a python dictionary as the cache
# Store each genre-language pair as the key
# Add a TTL(Time-to-Live) for cache validity (e.g., 60 secs) 

import time

cache = {} # dictionary to be used as cache
CACHE_TTL = 60  # Time-To-Live 60 secs

def get_cache(key):
    """
    Returns the value if not expired, else returns None
    """
    if key in cache:
        data, expiry = cache[key]
        if time.time() < expiry:
            return data
        else:
            del cache[key] # expired       
    return None

def set_cache(key, value):
    """
    Caches a value v under key k for 60 seconds
    """
    cache[key] = (value, time.time() + CACHE_TTL)
