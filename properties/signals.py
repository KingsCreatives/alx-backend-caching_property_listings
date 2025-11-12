from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property 
import logging

logger = logging.getLogger(__name__)
CACHE_KEY = 'all_properties'

@receiver(post_save, sender=Property)
def invalidate_property_cache_on_save(sender, instance, created, **kwargs):
    """
    Handler to invalidate the low-level 'all_properties' cache key
    whenever a Property object is created or updated.
    """
    cache.delete(CACHE_KEY)
    logger.info(f"Signal: post_save fired for Property ID {instance.pk}. Low-level cache '{CACHE_KEY}' invalidated.")

@receiver(post_delete, sender=Property)
def invalidate_property_cache_on_delete(sender, instance, **kwargs):
    """
    Handler to invalidate the low-level 'all_properties' cache key
    whenever a Property object is deleted.
    """
    cache.delete(CACHE_KEY)
    logger.info(f"Signal: post_delete fired for Property ID {instance.pk}. Low-level cache '{CACHE_KEY}' invalidated.")

