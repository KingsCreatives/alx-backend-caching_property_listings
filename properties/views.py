from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import cache_page
from .utils import get_all_properties, get_redis_cache_metrics
from .utils import get_all_properties, logger
from .models import Property

@cache_page(60 * 15, key_prefix='property_list_view') 
def property_list(request):
    properties = get_all_properties()

    metrics = get_redis_cache_metrics() 
    
    context = {
        'properties': properties, 
        'metrics': metrics 
    }
    return render(request, 'properties/property_list.html', context)


def delete_property(request, pk):
     
    if request.method == 'POST':
        property_obj = get_object_or_404(Property, pk=pk)

        property_obj.delete() 
        
        logger.info(f"Property ID {pk} deleted. Cache invalidation signal triggered.")
    
        return redirect('property_list') 
    
    return redirect('property_list')