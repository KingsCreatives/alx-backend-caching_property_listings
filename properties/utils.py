from django.core.cache import cache
from .models import Property 
import logging

logger = logging.getLogger(__name__)

def get_all_properties():

    CACHE_KEY = 'all_properties'
    CACHE_TIMEOUT = 3600 

   
    queryset = cache.get(CACHE_KEY)

    if queryset is None:
     
        logger.info(f"--- LOW-LEVEL CACHE MISS: Fetching properties from DB. ---")
        
        queryset = Property.objects.all().order_by('-created_at')
        
        cache.set(CACHE_KEY, queryset, CACHE_TIMEOUT)
        logger.info(f"--- LOW-LEVEL CACHE SET: Properties stored for 1 hour. ---")
    else:

        logger.info(f"--- LOW-LEVEL CACHE HIT: Serving properties from Redis. ---")

    return queryset