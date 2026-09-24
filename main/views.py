from django.shortcuts import render
from .models import Annotation

def iliad_page(request):
    annotations = Annotation.objects.all()
    return render(request, 'index.html', {'annotations': annotations} )
