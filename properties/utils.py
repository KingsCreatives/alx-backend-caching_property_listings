from django.core.cache import cache
from .models import Property 
import logging

logger = logging.getLogger(__name__)

PROPERTIES_CACHE_KEY = 'all_properties'

def get_all_properties():
    """
    Implements low-level caching for the Property queryset.
    """
    CACHE_TIMEOUT = 3600 
    properties_queryset = cache.get(PROPERTIES_CACHE_KEY)

    if properties_queryset is None:
        logger.info(f"--- LOW-LEVEL CACHE MISS: Fetching properties from DB. ---")
        
        properties_queryset = Property.objects.all().order_by('-created_at')
 
        cache.set(PROPERTIES_CACHE_KEY, properties_queryset, CACHE_TIMEOUT)
        logger.info(f"--- LOW-LEVEL CACHE SET: Properties stored for 1 hour. ---")
    else:
        logger.info(f"--- LOW-LEVEL CACHE HIT: Serving properties from Redis. ---")

    return properties_queryset


def get_redis_cache_metrics():
    """
    Retrieves cache metrics (hits, misses, and hit ratio) from the default Redis instance.
    """
    try:
        redis_client = cache.client.get_client(None)

        redis_info = redis_client.info('stats')
   
        keyspace_hits = redis_info.get('keyspace_hits', 0)
        keyspace_misses = redis_info.get('keyspace_misses', 0)

        total_lookups = keyspace_hits + keyspace_misses
        
        hit_ratio = 0.0
        if total_lookups > 0:
            hit_ratio = (keyspace_hits / total_lookups) * 100
        
        metrics = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'total_lookups': total_lookups,
            'hit_ratio': round(hit_ratio, 2)
        }
        
        logger.info("--- REDIS CACHE METRICS ---")
        logger.info(f"Hits: {keyspace_hits}, Misses: {keyspace_misses}, Ratio: {metrics['hit_ratio']}%")
        logger.info("--------------------------")

        # 5. Return the dictionary
        return metrics

    except Exception as e:
        logger.error(f"Failed to retrieve Redis metrics: {e}")
        return {}