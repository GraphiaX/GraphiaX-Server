from django.shortcuts import render
from .utils import get_project_structure
from django.http import JsonResponse
from django.http import HttpResponse
import json
import requests

def say_hello_view(request):
    return HttpResponse('Hello World')

def project_structure_view(request):
    structure = get_project_structure()
    if structure is not None:
        data = json.loads(structure)
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'Failed to retrieve project structure.'})

def github_repo_info(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            repo_url = data.get('repoUrl')  # Assuming the URL is sent in the 'repoUrl' field
            repo_url = convert_to_api_url(repo_url)
            if repo_url:

                response = requests.get(repo_url)

                if response.status_code == 200:
                    repo_info = get_project_structure(repo_url)
                    return JsonResponse(repo_info, safe=False)
                else:
                    error_message = {'error': 'Failed to fetch repository information.'}
                    return JsonResponse(error_message, status=500)
            else:
                error_message = {'error': 'Invalid request data. Missing repoUrl field.'}
                return JsonResponse(error_message, status=400)

        except json.JSONDecodeError:
            error_message = {'error': 'Invalid request data. Unable to parse JSON.'}
            return JsonResponse(error_message, status=400)

    # Return an error response for other request methods
    error_message = {'error': 'Invalid request method.'}
    return JsonResponse(error_message, status=400)

def convert_to_api_url(github_url):
    parts = github_url.strip().split('/')
    username = parts[3]
    repo_name = parts[4].replace('.git', '')
    api_url = f"https://api.github.com/repos/{username}/{repo_name}/contents"
    return api_url
