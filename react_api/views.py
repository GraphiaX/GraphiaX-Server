from django.shortcuts import render
from .utils import get_project_structure
from django.http import JsonResponse
from django.http import HttpResponse
import json

# Create your views here.

def say_hello_view(request):
    return HttpResponse('Hello World')

def project_structure_view(request):
    structure = get_project_structure()
    
    if structure is not None:
        data = json.loads(structure)
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'Failed to retrieve project structure.'})


