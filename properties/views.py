from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .models import Property

@cache_page(60 * 15)
def property_list(request):
    properties = Property.objects.all().order_by('-created_at')
 
    context = {
        'properties': properties,
        'cached': True, 
    }
    return render(request, 'properties/property_list.html', context)